# ClinePass Usage Tracker
# Run this script to generate a usage report from Cline CLI sessions
# Usage: .\Track-ClineUsage.ps1

$sessions = Get-ChildItem "$env:USERPROFILE\.cline\data\sessions" -Directory
$report = @{
    totalSessions = 0
    totalInput = 0
    totalOutput = 0
    totalCacheRead = 0
    totalCacheWrite = 0
    totalCost = 0
    byModel = @{}
    byDate = @{}
    clinePassSessions = @()
}

foreach ($s in $sessions) {
    $jsonPath = "$($s.FullName)\$($s.Name).json"
    if (-not (Test-Path $jsonPath)) { continue }
    
    $json = Get-Content $jsonPath -Raw | ConvertFrom-Json
    if (-not $json.metadata.usage) { continue }
    
    $u = $json.metadata.usage
    $model = $json.model
    $date = $json.started_at.Substring(0, 10)
    
    # Update totals
    $report.totalSessions++
    $report.totalInput += $u.inputTokens
    $report.totalOutput += $u.outputTokens
    $report.totalCacheRead += $u.cacheReadTokens
    $report.totalCacheWrite += $u.cacheWriteTokens
    $report.totalCost += $u.totalCost
    
    # Track by model
    if (-not $report.byModel[$model]) {
        $report.byModel[$model] = @{ input = 0; output = 0; cache = 0; cost = 0; count = 0 }
    }
    $report.byModel[$model].input += $u.inputTokens
    $report.byModel[$model].output += $u.outputTokens
    $report.byModel[$model].cache += $u.cacheReadTokens
    $report.byModel[$model].cost += $u.totalCost
    $report.byModel[$model].count++
    
    # Track by date
    if (-not $report.byDate[$date]) {
        $report.byDate[$date] = @{ input = 0; output = 0; cache = 0; cost = 0 }
    }
    $report.byDate[$date].input += $u.inputTokens
    $report.byDate[$date].output += $u.outputTokens
    $report.byDate[$date].cache += $u.cacheReadTokens
    $report.byDate[$date].cost += $u.totalCost
    
    # Track ClinePass sessions
    if ($model -like "cline-pass/*") {
        $report.clinePassSessions += @{
            session = $s.Name
            model = $model
            input = $u.inputTokens
            output = $u.outputTokens
            cache = $u.cacheReadTokens
            cost = $u.totalCost
        }
    }
}

# Output summary
Write-Output "=== Cline CLI Usage Report ==="
Write-Output "Generated: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Output ""
Write-Output "Total Sessions: $($report.totalSessions)"
Write-Output "Total Input: $([math]::Round($report.totalInput / 1000000, 2))M tokens"
Write-Output "Total Output: $([math]::Round($report.totalOutput / 1000000, 2))M tokens"
Write-Output "Total Cache Read: $([math]::Round($report.totalCacheRead / 1000000, 2))M tokens"
Write-Output "Total Cost: `$$([math]::Round($report.totalCost, 4))"
Write-Output ""
Write-Output "=== By Model ==="
foreach ($model in $report.byModel.Keys | Sort-Object) {
    $m = $report.byModel[$model]
    Write-Output "$model | $($m.count) sessions | In: $([math]::Round($m.input / 1000000, 2))M | Out: $([math]::Round($m.output / 1000000, 2))M | Cost: `$$([math]::Round($m.cost, 4))"
}
Write-Output ""
Write-Output "=== ClinePass Sessions ==="
Write-Output "$($report.clinePassSessions.Count) sessions using ClinePass"
$clinePassTotal = 0
foreach ($cp in $report.clinePassSessions) {
    $clinePassTotal += $cp.cost
}
Write-Output "Total ClinePass Cost: `$$([math]::Round($clinePassTotal, 4))"
