# ClinePass Auth Status Check
# Verifies current login state and token health
# Usage: .\Check-ClineAuth.ps1
#
# Token lifecycle:
#   - Access token (JWT): 1-hour TTL, auto-refreshed by Cline via refresh token
#   - Refresh token: long-lived, only expires if unused for extended period
#   - You should NEVER need to re-auth manually unless refresh token expires

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

    # Decode JWT to get actual token TTL
    $accessToken = $auth.accessToken -replace '^workos:', ''
    $jwtExpired = $true
    $jwtTtl = "unknown"
    $jwtRemaining = "unknown"
    $jwtRemainingMinutes = 0
    try {
        $parts = $accessToken.Split('.')
        if ($parts.Count -eq 3) {
            $payload = $parts[1]
            $payload = $payload.Replace('-','+').Replace('_','/')
            switch ($payload.Length % 4) {
                2 { $payload += '==' }
                3 { $payload += '=' }
            }
            $decoded = [System.Text.Encoding]::UTF8.GetString([Convert]::FromBase64String($payload))
            $claims = $decoded | ConvertFrom-Json
            $jwtExp = [DateTimeOffset]::FromUnixTimeSeconds($claims.exp).DateTime
            $jwtIat = [DateTimeOffset]::FromUnixTimeSeconds($claims.iat).DateTime
            $jwtRemainingMinutes = [math]::Round(($jwtExp - [DateTime]::Now).TotalMinutes)
            $jwtTtl = "{0:N0} minutes" -f ($jwtExp - $jwtIat).TotalMinutes
            $jwtRemaining = "{0:N0} minutes" -f $jwtRemainingMinutes
            $jwtExpired = [double]::Parse((Get-Date -UFormat %s)) -gt $claims.exp
        }
    } catch { }

    # Token age
    $createdAt = $auth.metadata.sessionStartedAtMs
    if ($createdAt) {
        $tokenAge = [DateTime]::Now - [DateTimeOffset]::FromUnixTimeMilliseconds($createdAt).DateTime
        $ageStr = "{0}d {1}h" -f $tokenAge.Days, $tokenAge.Hours
    } else {
        $ageStr = "unknown"
    }

    $status = if ($jwtExpired) { "EXPIRED - run 'cline auth'" }
              elseif ($jwtRemainingMinutes -le 5) { "REFRESHING (auto)" }
              else { "ACTIVE" }
    $model = $provider.settings.model

    Write-Output "--- Provider: $providerName ---"
    Write-Output "  Model:        $model"
    Write-Output "  Account:      $($auth.metadata.userInfo.email)"
    Write-Output "  User:         $($auth.metadata.userInfo.firstName) $($auth.metadata.userInfo.lastName)"
    Write-Output "  Token Source: $($provider.tokenSource)"
    Write-Output "  Token Age:    $ageStr"
    Write-Output "  JWT TTL:      $jwtTtl (refreshes automatically via refresh token)"
    Write-Output "  JWT Status:   $status"
    Write-Output "  Config Refresh: $expiresDate ($([math]::Round($remaining.TotalHours, 1))h remaining)"
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
    $hasRefreshToken = -not [string]::IsNullOrEmpty($active.settings.auth.refreshToken)
    Write-Output "Refresh Token:   $(if ($hasRefreshToken) { 'Present (auto-refresh enabled)' } else { 'MISSING — manual re-auth required' })"
    Write-Output ""
    if ($hasRefreshToken) {
        Write-Output "Cline handles token rotation automatically."
        Write-Output "You only need 'cline auth' if the refresh token expires (weeks/months)."
    } else {
        Write-Output "No refresh token found. Run 'cline auth' to get one."
    }
}
