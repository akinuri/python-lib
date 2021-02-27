@echo off

python "%~dp0\merge-css.py" %*

IF %ERRORLEVEL% NEQ 0 PAUSE