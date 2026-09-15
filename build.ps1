# Build script for Windows (PowerShell)
# Usage: run this script from PowerShell in the project root.

Set-Location -Path "${PSScriptRoot}"

# Ensure dependencies are installed
pip install --upgrade -r requirements.txt

$iconPath = Join-Path -Path $PWD -ChildPath "icon.ico"

$pyArgs = @('--noconfirm', '--onefile', '--windowed', '--name', 'RAWSync')
if (Test-Path -Path $iconPath) {
	Write-Host "Found icon: $iconPath - including in build."
	$pyArgs += @('--icon', $iconPath)
} else {
	Write-Host "No icon.ico found in project root - building without custom icon."
}
# Make sure icon.ico ships alongside the exe's internals too (used at runtime
# for window/taskbar icon, not just the exe's own icon).
$pyArgs += @('--add-data', "icon.ico;.")

$pyArgs += 'main.py'

& pyinstaller @pyArgs

Write-Host "Build finished. Output is in the 'dist' folder."
