# ClinePass Usage Logger
# Appends a usage snapshot to a persistent log file, independent of Cline's own logs.
# Run daily (via Task Scheduler or manually) to build trend data.
# Usage: .\Log-ClineUsage.ps1
#
# Output: _Per_Cline_Chat/usage_log.csv
# Each row: timestamp, sessions, total_in, total_out, total_cache, total_cost, by_model_json

$homeDir = [Environment]::GetFolderPath("UserProfile")
$sessionsDir = Join-Path $homeDir ".cline\data\sessions"
$logDir = Join-Path $PSScriptRoot "..\_Per_Cline_Chat"
$logFile = Join-Path $logDir "usage_log.csv"

# Ensure log directory exists
if (-not (Test-Path $logDir)) {
    New-Item -ItemType Directory -Path $logDir -Force | Out-Null
}

# Initialize CSV with headers if missing
if (-not (Test-Path $logFile)) {
    "timestamp,total_sessions,total_input_tokens,total_output_tokens,total_cache_tokens,total_reference_cost,clinepass_sessions,clinepass_cost,model_breakdown" | Out-File $logFile -Encoding UTF8
}

# Parse all sessions
$sessions = Get-ChildItem $sessionsDir -Directory -ErrorAction SilentlyContinue
$report = @{
    totalSessions = 0
    totalInput = 0
    totalOutput = 0
    totalCache = 0
    totalCost = 0
    clinePassSessions = 0
    clinePassCost = 0
    byModel = @{}
}

foreach ($s in sessions) {
    $jsonPath = Join-Path $s.FullName "$($s.Name).json"
    if (-not (Test-Path $jsonPath)) { continue }

    try {
        $json = Get-Content $jsonPath -Raw | ConvertFrom-Json
    } catch { continue }

    if (-not $json.metadata.usage) { continue }

    $u = $json.metadata.usage
    $model = $json.model

    $report.totalSessions++
    $report.totalInput += $u.inputTokens
    $report.totalOutput += $u.outputTokens
    $report.totalCache += $u.cacheReadTokens
    $report.totalCost += $u.totalCost

    if (-not $report.byModel[$model]) {
        $report.byModel[$model] = @{ input = 0; output = 0; cache = 0; cost = 0; count = 0 }
    }
    $report.byModel[$model].input += $u.inputTokens
    $report.byModel[$model].output += $u.outputTokens
    $report.byModel[$model].cache += $u.cacheReadTokens
    $report.byModel[$model].cost += $u.totalCost
    $report.byModel[$model].count++

    if ($model -like "cline-pass/*") {
        $report.clinePassSessions++
        $report.clinePassCost += $u.totalCost
    }
}

# Build model breakdown JSON
$modelBreakdown = @{}
foreach ($m in $report.byModel.Keys) {
    $v = $report.byModel[$m]
    $modelBreakdown[$m] = @{
        sessions = $v.count
        input = $v.input
        output = $v.output
        cache = $v.cache
        cost = [math]::Round($v.cost, 6)
    }
}
$breakdownJson = ($modelBreakdown | ConvertTo-Json -Compress)

# Append to CSV
$timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$row = "$timestamp,$($report.totalSessions),$($report.totalInput),$($report.totalOutput),$($report.totalCache),$([math]::Round($report.totalCost, 6)),$($report.clinePassSessions),$([math]::Round($report.clinePassCost, 6)),`"$breakdownJson`""
$row | Out-File $logFile -Append -Encoding UTF8

# Console summary
Write-Output "=== Usage Snapshot Logged ==="
Write-Output "Timestamp:  $timestamp"
Write-Output "Sessions:   $($report.totalSessions)"
Write-Output "Input:      $([math]::Round($report.totalInput / 1e6, 2))M tokens"
Write-Output "Output:     $([math]::Round($report.totalOutput / 1e6, 2))M tokens"
Write-Output "Cache:      $([math]::Round($report.totalCache / 1e6, 2))M tokens"
Write-Output "Cost:       `$$([math]::Round($report.totalCost, 4))"
Write-Output "ClinePass:  $($report.clinePassSessions) sessions / `$$([math]::Round($report.clinePassCost, 4))"
Write-Output ""
Write-Output "Log saved: $logFile"
Write-Output ""
Write-Output "=== Trend (last 10 snapshots) ==="
if (Test-Path $logFile) {
    $allRows = Get-Content $logFile | Select-Object -Skip 1 | Select-Object -Last 10
    foreach ($r in $allRows) {
        $parts = $r.Split(',')
        $ts = $parts[0]
        $sess = $parts[1]
        $cost = $parts[5]
        $cpSess = $parts[6]
        Write-Output "  $ts | $sess sessions | `$$cost | ClinePass: $cpSess"
    }
}

