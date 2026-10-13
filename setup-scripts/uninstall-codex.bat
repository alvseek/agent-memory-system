@echo off
REM uninstall-codex.bat - Remove the agent-memory CORE markdown install for Codex
REM (calls uninstall-codex.py directly; no Git Bash required).
echo Running Codex core uninstall...
echo.
where py >nul 2>&1
if %ERRORLEVEL%==0 (
    py -3 "%~dp0uninstall-codex.py" %*
) else (
    python "%~dp0uninstall-codex.py" %*
)
echo.
pause
