@echo off
REM setup-opencode.bat - Complete OpenCode setup (calls setup-opencode.py directly)
REM No Git Bash required for the orchestrator itself; steps 0-1 locate Git Bash automatically.
echo Running OpenCode setup...
echo.
where py >nul 2>&1
if %ERRORLEVEL%==0 (
    py -3 "%~dp0setup-opencode.py" %*
) else (
    python "%~dp0setup-opencode.py" %*
)
echo.
pause
