# RAWSync

A small Windows desktop tool for photographers: point it at a folder of a
client's selected JPEG previews and the RAW folder they came from, and it
copies every RAW file with a matching filename into a destination folder --
ready to import into Lightroom.

## Features

- Matches RAW files to JPEGs by filename (case-insensitive, ignoring
  extension), so `IMG_0231.jpg` matches `IMG_0231.CR3`.
- Supports CR3, CR2, ARW, NEF, DNG, TIFF/TIF, RAF, ORF and RW2 RAW formats.
- Threaded copy with live progress, so the UI never freezes.
- Clean, macOS-inspired interface with light/dark/system appearance.
- Single-file Windows executable via PyInstaller, plus an optional NSIS
  installer.

## Quick start

```powershell
pip install -r requirements.txt
python main.py
```

## Project layout

```
main.py            Entry point
rawsync/
  core.py           Matching + copy logic (no UI dependencies)
  theme.py           Color palette, fonts, spacing tokens
  ui.py               Splash screen, main window, settings, widgets
icon.ico            App icon, used for the window and the built .exe
```

## Building a Windows executable

```powershell
.\build.ps1
```

This runs PyInstaller and produces `dist\RAWSync.exe` (single file,
windowed, using `icon.ico`).

## Building an installer (optional)

Requires [NSIS](https://nsis.sourceforge.io/) (`makensis` on PATH -- e.g.
`choco install nsis -y`).

```powershell
.\build.ps1
.\create_installer.ps1
```

Produces `RAWSync_Installer_2.0.exe` in the project folder, which installs
to Program Files with Start Menu and desktop shortcuts.

## Notes

- If you shoot on a RAW format not already listed, add its extension to
  `RAW_EXTENSIONS` in `rawsync/core.py`.
- The app icon is `icon.ico` in the project root; replace it and rebuild to
  change the app's icon everywhere (window, taskbar, built exe, installer
  shortcuts).

License: MIT-style (copy/modify as you like).
