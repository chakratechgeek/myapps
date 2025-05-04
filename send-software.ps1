# send-software.ps1
$serverUrl = "http://your-server:8000/software/api/collect/"
$hostname = $env:COMPUTERNAME

$registryPaths = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
    "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"
)

$softwareList = @()

foreach ($path in $registryPaths) {
    $apps = Get-ItemProperty $path -ErrorAction SilentlyContinue | Where-Object { $_.DisplayName } | Select-Object DisplayName, DisplayVersion
    foreach ($app in $apps) {
        $softwareList += [PSCustomObject]@{
            hostname       = $hostname
            software_name  = $app.DisplayName
            version        = $app.DisplayVersion
            license_key    = ""
            is_valid       = $true
        }
    }
}

# Convert to JSON and send all in one request
$json = $softwareList | ConvertTo-Json -Depth 2 -Compress
curl -X POST $serverUrl -H "Content-Type: application/json" -d $json | Out-Null
