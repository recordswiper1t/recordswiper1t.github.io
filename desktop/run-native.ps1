$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')

$Root = (Get-Location).Path
$KrfCandidates = @(
    (Join-Path $Root 'assets\kingdom-rush-frontiers-v12-1.swf'),
    (Join-Path $Root 'assets\kingdom-rush-frontiers-v12.swf'),
    (Join-Path $Root 'assets\kingdom-rush-frontiers-v11.swf'),
    (Join-Path $Root 'assets\kingdom-rush-frontiers-v10.swf'),
    (Join-Path $Root 'assets\kingdom-rush-frontiers-v9.swf'),
    (Join-Path $Root 'assets\kingdom-rush-frontiers-v8.swf'),
    (Join-Path $Root 'assets\kingdom-rush-frontiers-v5.swf')
)
$StickWar = Join-Path $Root 'assets\stick-war-complete-v1.swf'
$EpicWar5Stable = Join-Path $Root 'assets\epic-war-5-sandbox-v2.swf'
$EpicWar5Expansion = Join-Path $Root 'assets\epic-war-5-expansion-v34.swf'

$Game = 'krf'
$Refresh = $false
$Stable = $false
$ForceVulkan = $false
$ForceGl = $false
$ForceDx12 = $false
$ForwardArgs = New-Object System.Collections.Generic.List[string]
for ($i = 0; $i -lt $args.Count; $i++) {
    $arg = [string]$args[$i]
    switch ($arg) {
        '--refresh' { $Refresh = $true; continue }
        '--stable' { $Stable = $true; continue }
        '--vulkan' { $ForceVulkan = $true; continue }
        '--gl' { $ForceGl = $true; continue }
        '--dx12' { $ForceDx12 = $true; continue }
        '--game' {
            if ($i + 1 -ge $args.Count) { throw '--game requires krf, stickwar, epicwar5, or epicwar5-expansion.' }
            $i++
            $Game = ([string]$args[$i]).ToLowerInvariant()
            continue
        }
        '--stickwar' { $Game = 'stickwar'; continue }
        '--epicwar5' { $Game = 'epicwar5'; continue }
        '--epicwar5-expansion' { $Game = 'epicwar5-expansion'; continue }
        '--krf' { $Game = 'krf'; continue }
        default {
            if ($arg -like '--game=*') { $Game = $arg.Substring(7).ToLowerInvariant(); continue }
            $ForwardArgs.Add($arg)
        }
    }
}

switch ($Game) {
    { $_ -in @('krf','kingdom-rush','frontiers') } {
        $Game = 'krf'
        $Swf = $KrfCandidates | Where-Object { Test-Path $_ } | Select-Object -First 1
        $GameLabel = 'Kingdom Rush Frontiers'
        break
    }
    { $_ -in @('stickwar','stick-war','sw') } {
        $Game = 'stickwar'; $Swf = $StickWar; $GameLabel = 'Super Stick War (SW1 + SW2)'; break
    }
    { $_ -in @('epicwar5','epic-war-5','ew5') } {
        $Game = 'epicwar5'; $Swf = $EpicWar5Stable; $GameLabel = 'Epic War 5 (stable V1.05-based build)'; break
    }
    { $_ -in @('epicwar5-expansion','epic-war-5-expansion','ew5-expansion') } {
        $Game = 'epicwar5-expansion'; $Swf = $EpicWar5Expansion; $GameLabel = 'Epic War 5 Expansion V3.4'; break
    }
    default { throw "Unknown game '$Game'. Choose krf, stickwar, epicwar5, or epicwar5-expansion." }
}
if (-not $Swf -or -not (Test-Path $Swf)) { throw "Missing game SWF: $Swf" }

$Cache = Join-Path $Root '.native\ruffle'
$Exe = Join-Path $Cache 'ruffle.exe'
if ($Refresh -and (Test-Path $Cache)) { Remove-Item $Cache -Recurse -Force }

if (-not (Test-Path $Exe)) {
    New-Item -ItemType Directory -Force -Path $Cache | Out-Null
    $headers = @{ 'User-Agent' = 'strategy-mod-native-launcher'; 'Accept' = 'application/vnd.github+json' }
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

    $tmp = Join-Path $env:TEMP ('strategy-mod-ruffle-' + [guid]::NewGuid().ToString('N'))
    New-Item -ItemType Directory -Path $tmp | Out-Null
    try {
        $zip = Join-Path $tmp 'ruffle.zip'
        Invoke-WebRequest -Headers @{ 'User-Agent' = 'strategy-mod-native-launcher' } -Uri $asset.browser_download_url -OutFile $zip
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

$backend = if ($ForceVulkan) { 'vulkan' } elseif ($ForceGl) { 'gl' } else { 'dx12' }
if ($ForceDx12) { $backend = 'dx12' }

function Invoke-Ruffle([string]$GraphicsBackend) {
    $env:WGPU_BACKEND = $GraphicsBackend
    $ruffleArgs = @('--graphics', $GraphicsBackend, $Swf) + @($ForwardArgs)
    $proc = Start-Process -FilePath $Exe -ArgumentList $ruffleArgs -Wait -PassThru -NoNewWindow
    return [int]$proc.ExitCode
}

Write-Host "Launching $GameLabel with native Ruffle"
Write-Host "Game: $Swf"
Write-Host "Graphics backend: $backend"
$code = Invoke-Ruffle $backend

# Prefer DX12 on Windows. Only retry OpenGL if the actual Ruffle process exits
# with a non-zero code; do not treat a blank PowerShell $LASTEXITCODE as failure.
if ($code -ne 0 -and -not $ForceVulkan -and $backend -ne 'gl') {
    Write-Warning "Ruffle exited with code $code using $backend. Retrying with OpenGL."
    $code = Invoke-Ruffle 'gl'
}
exit $code
