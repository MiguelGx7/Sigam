@echo off
REM Atajo para arrancar SIGAM con doble clic o desde cmd.exe.
REM Acepta los mismos parametros que dev.ps1:  dev.bat -Stop  /  dev.bat -Setup
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0dev.ps1" %*
