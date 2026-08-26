@echo off
title Camera Diagnostic Test
cd /d "%~dp0"
echo ============================================================
echo   Running Camera Diagnostic Test...
echo ============================================================
echo.
python test_camera.py
pause
