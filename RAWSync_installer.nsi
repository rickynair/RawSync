; NSIS installer script for RAWSync
; Packages dist\RAWSync.exe and README.md into a simple Windows installer.

!define APP_NAME "RAWSync"
!define APP_EXE "RAWSync.exe"
!define VERSION "2.0"
!define COMPANY_NAME "ImageGNation"

OutFile "RAWSync_Installer_${VERSION}.exe"
InstallDir "$PROGRAMFILES\${APP_NAME}"
ShowInstDetails show
ShowUnInstDetails show

RequestExecutionLevel admin

Section "Install"
  SetOutPath "$INSTDIR"
  File "dist\${APP_EXE}"
  File "README.md"
  File "icon.ico"

  WriteUninstaller "$INSTDIR\Uninstall.exe"

  CreateDirectory "$SMPROGRAMS\${APP_NAME}"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\icon.ico"
  CreateShortCut "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk" "$INSTDIR\Uninstall.exe"
  CreateShortCut "$DESKTOP\${APP_NAME}.lnk" "$INSTDIR\${APP_EXE}" "" "$INSTDIR\icon.ico"
SectionEnd

Section "Uninstall"
  Delete "$INSTDIR\${APP_EXE}"
  Delete "$INSTDIR\README.md"
  Delete "$INSTDIR\icon.ico"
  Delete "$INSTDIR\Uninstall.exe"
  RMDir "$INSTDIR"

  Delete "$SMPROGRAMS\${APP_NAME}\${APP_NAME}.lnk"
  Delete "$SMPROGRAMS\${APP_NAME}\Uninstall.lnk"
  RMDir "$SMPROGRAMS\${APP_NAME}"
  Delete "$DESKTOP\${APP_NAME}.lnk"
SectionEnd
