@echo off
REM setup-all-claude-code.bat - Windows wrapper for setup-all-claude-code.py.
REM Installs the agent-memory CORE procedures as slash commands (compiles first, then copies
REM the self-contained output). Uses uv's project environment, including the composer.
REM Set AGENT_MEMORY_TARGET_DIR to override the default ~/.claude/commands target.

setlocal
set "PY_SCRIPT=%~dp0setup-all-claude-code.py"

set "UV="
for /f "delims=" %%i in ('where uv 2^>nul ^| findstr /v /i "WindowsApps"') do if not defined UV set "UV=%%i"

if not defined UV (
    echo ERROR: uv not found on PATH. Install uv and retry.
    echo %cmdcmdline% | find /i "%~nx0" >nul && pause
    exit /b 9
)

"%UV%" run --project "%~dp0..\.." python "%PY_SCRIPT%" %*
set "RC=%ERRORLEVEL%"

REM Pause only when double-clicked, so the window doesn't flash shut on the result.
echo %cmdcmdline% | find /i "%~nx0" >nul && pause
exit /b %RC%
