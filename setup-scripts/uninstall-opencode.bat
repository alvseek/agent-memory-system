@echo off
REM uninstall-opencode.bat - Remove the agent-memory CORE markdown install for OpenCode
REM (calls uninstall-opencode.py directly; no Git Bash required).
echo Running OpenCode core uninstall...
echo.
where py >nul 2>&1
if %ERRORLEVEL%==0 (
    py -3 "%~dp0uninstall-opencode.py" %*
) else (
    python "%~dp0uninstall-opencode.py" %*
)
echo.
pause
