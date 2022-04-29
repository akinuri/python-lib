@echo off

if [%1]==[] (
    echo Drop a .py file on this file.
    echo.
    pause
) else (
    python %1
    if %ERRORLEVEL% NEQ 0 pause
)

REM pause
