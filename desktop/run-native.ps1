$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

$Root = (Get-Location).Path
$V11 = Join-Path $Root 'assets\kingdom-rush-frontiers-v11.swf'
$V10 = Join-Path $Root 'assets\kingdom-rush-frontiers-v10.swf'
$V9 = Join-Path $Root 'assets\kingdom-rush-frontiers-v9.swf'
$V8 = Join-Path $Root 'assets\kingdom-rush-frontiers-v8.swf'
$V7 = Join-Path $Root 'assets\kingdom-rush-frontiers-v5.swf'
$Swf = if (Test-Path $V11) { $V11 } elseif (Test-Path $V10) { $V10 } elseif (Test-Path $V9) { $V9 } elseif (Test-Path $V8) { $V8 } else { $V7 }
if (-not (Test-Path $Swf)) { throw "Missing game SWF: $Swf" }

$Cache = Join-Path $Root '.native\ruffle'
$Exe = Join-Path $Cache 'ruffle.exe'
$Refresh = $args -contains '--refresh'
$Stable = $args -contains '--stable'

if ($Refresh -and (Test-Path $Cache)) { Remove-Item $Cache -Recurse -Force }

if (-not (Test-Path $Exe)) {
    New-Item -ItemType Directory -Force -Path $Cache | Out-Null
    $headers = @{ 'User-Agent' = 'krf-native-launcher'; 'Accept' = 'application/vnd.github+json' }
    $releases = Invoke-RestMethod -Headers $headers -Uri 'https://api.github.com/repos/ruffle-rs/ruffle/releases?per_page=30'
    if ($Stable) {
        $release = $releases | Where-Object { -not $_.draft -and -not $_.prerelease } | Select-Object -First 1
    } else {
        $release = $releases | Where-Object { -not $_.draft -and $_.prerelease } | Select-Object -First 1
    }
    if (-not $release) { throw 'Could not find a suitable Ruffle release.' }

    $asset = $release.assets | Where-Object {
        $n = $_.name.ToLowerInvariant()
        ($n -match 'windows') -and ($n -match 'x86_64|x64|64') -and ($n.EndsWith('.zip')) -and ($n -notmatch 'extension|web')
    } | Sort-Object @{Expression={ if ($_.name.ToLowerInvariant() -match 'desktop') { 0 } else { 1 } }} | Select-Object -First 1
    if (-not $asset) { throw 'Could not find the Windows desktop Ruffle archive.' }

    $tmp = Join-Path $env:TEMP ('krf-ruffle-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $tmp | Out-Null
    try {
        $zip = Join-Path $tmp 'ruffle.zip'
        Invoke-WebRequest -Headers @{ 'User-Agent' = 'krf-native-launcher' } -Uri $asset.browser_download_url -OutFile $zip
        Expand-Archive -Path $zip -DestinationPath $Cache -Force
        $found = Get-ChildItem -Path $Cache -Recurse -Filter 'ruffle.exe' | Select-Object -First 1
        if (-not $found) { throw 'Downloaded archive did not contain ruffle.exe.' }
        if ($found.FullName -ne $Exe) { Copy-Item $found.FullName $Exe -Force }
        Set-Content -Path (Join-Path $Cache 'VERSION') -Value $release.tag_name -Encoding ascii
    }
    finally {
        if (Test-Path $tmp) { Remove-Item $tmp -Recurse -Force }
    }
}

$label = if ($Swf -eq $V11) { 'V11 sandbox' } elseif ($Swf -eq $V10) { 'V10 complete' } elseif ($Swf -eq $V9) { 'V9 complete' } elseif ($Swf -eq $V8) { 'V8 optimized' } else { 'V7 fallback' }
Write-Host "Launching Kingdom Rush Frontiers $label with native Ruffle"
Write-Host "Game: $Swf"
& $Exe $Swf
exit $LASTEXITCODE
