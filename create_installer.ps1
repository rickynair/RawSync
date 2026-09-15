# create_installer.ps1
# Builds an NSIS installer for RAWSync using RAWSync_installer.nsi.
# Requires NSIS (makensis) to be installed and on PATH.

Set-Location -Path "${PSScriptRoot}"

$distExe = Join-Path $PWD 'dist\RAWSync.exe'
$nsiScript = Join-Path $PWD 'RAWSync_installer.nsi'
$outName = 'RAWSync_Installer_2.0.exe'

if (-not (Test-Path $distExe)) {
    Write-Error "Required file not found: $distExe`nPlease build the app first (run .\build.ps1) and ensure dist\RAWSync.exe exists."
    exit 1
}

if (-not (Test-Path $nsiScript)) {
    Write-Error "NSIS script not found: $nsiScript"
    exit 1
}

$makensis = Get-Command -Name makensis -ErrorAction SilentlyContinue
if (-not $makensis) {
    Write-Host 'makensis (NSIS) not found on PATH.' -ForegroundColor Yellow
    Write-Host 'Install it via Chocolatey: choco install nsis -y'
    Write-Host 'or download it from https://nsis.sourceforge.io/Download'
    exit 2
}

Write-Host 'Running makensis to create installer...'
& makensis $nsiScript

if ($LASTEXITCODE -ne 0) {
    Write-Error "makensis failed with exit code $LASTEXITCODE"
    exit $LASTEXITCODE
}

if (Test-Path $outName) {
    Write-Host "Installer built: $PWD\$outName"
} else {
    Write-Host 'Installer created - check the current folder for output.'
}
