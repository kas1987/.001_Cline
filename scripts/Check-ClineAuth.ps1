# ClinePass Auth Status Check
# Verifies current login state and token health
# Usage: .\Check-ClineAuth.ps1

$settingsPath = "$env:USERPROFILE\.cline\data\settings\providers.json"

if (-not (Test-Path $settingsPath)) {
    Write-Output "ERROR: Cline settings not found at $settingsPath"
    exit 1
}

$settings = Get-Content $settingsPath -Raw | ConvertFrom-Json
$now = [DateTimeOffset]::Now.ToUnixTimeMilliseconds()

Write-Output "=== ClinePass Auth Status ==="
Write-Output "Checked: $(Get-Date -Format 'yyyy-MM-dd HH:mm')"
Write-Output ""

foreach ($providerName in $settings.providers.PSObject.Properties.Name) {
    $provider = $settings.providers.$providerName
    $auth = $provider.settings.auth
    if (-not $auth) { continue }

    $expiresAt = $auth.expiresAt
    $expiresDate = [DateTimeOffset]::FromUnixTimeMilliseconds($expiresAt).DateTime
    $remaining = $expiresDate - [DateTime]::Now
    $isExpired = $now -gt $expiresAt

    # Token age
    $createdAt = $auth.metadata.sessionStartedAtMs
    if ($createdAt) {
        $tokenAge = [DateTime]::Now - [DateTimeOffset]::FromUnixTimeMilliseconds($createdAt).DateTime
        $ageStr = "{0}d {1}h" -f $tokenAge.Days, $tokenAge.Hours
    } else {
        $ageStr = "unknown"
    }

    $status = if ($isExpired) { "EXPIRED" } elseif ($remaining.TotalHours -lt 24) { "EXPIRING SOON" } else { "VALID" }
    $model = $provider.settings.model

    Write-Output "--- Provider: $providerName ---"
    Write-Output "  Model:        $model"
    Write-Output "  Account:      $($auth.metadata.userInfo.email)"
    Write-Output "  User:         $($auth.metadata.userInfo.firstName) $($auth.metadata.userInfo.lastName)"
    Write-Output "  Token Source: $($provider.tokenSource)"
    Write-Output "  Token Age:    $ageStr"
    Write-Output "  Expires:      $expiresDate ($([math]::Round($remaining.TotalHours, 1))h remaining)"
    Write-Output "  Status:       $status"
    if ($provider.settings.reasoning) {
        Write-Output "  Reasoning:    effort=$($provider.settings.reasoning.effort)"
    }
    Write-Output ""
}

# Summary
$activeProvider = $settings.lastUsedProvider
Write-Output "=== Summary ==="
Write-Output "Active Provider: $activeProvider"
$active = $settings.providers.$activeProvider
if ($active) {
    $activeExpires = $active.settings.auth.expiresAt
    $activeExpired = $now -gt $activeExpires
    if ($activeExpired) {
        Write-Output "WARNING: Active provider token is EXPIRED. Run 'cline auth' to re-login."
    } else {
        $remaining = [DateTimeOffset]::FromUnixTimeMilliseconds($activeExpires).DateTime - [DateTime]::Now
        Write-Output "Active token is valid for $([math]::Round($remaining.TotalHours, 1)) more hours."
    }
}
