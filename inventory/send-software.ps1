$serverUrl = "http://localhost:8000/software/api/collect/"
$hostname = $env:COMPUTERNAME

$registryPaths = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"
)

$softwareList = @()

foreach ($path in $registryPaths) {
    $apps = Get-ItemProperty $path -ErrorAction SilentlyContinue |
        Where-Object { $_.DisplayName } |
        Select-Object DisplayName, DisplayVersion

    foreach ($app in $apps) {
        $softwareList += [PSCustomObject]@{
            hostname      = $hostname
            software_name = $app.DisplayName
            version       = $app.DisplayVersion
            license_key   = ""
            is_valid      = $true
        }
    }
}

# Convert to JSON
$json = $softwareList | ConvertTo-Json -Depth 2 -Compress

# ✅ Correct PowerShell-style HTTP POST (instead of curl)
Invoke-RestMethod -Method POST -Uri $serverUrl -Body $json -ContentType "application/json"
