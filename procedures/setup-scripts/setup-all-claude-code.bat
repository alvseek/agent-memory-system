@echo off
REM setup-all-claude-code.bat - Windows wrapper for setup-all-claude-code.py.
REM Installs the agent-memory CORE procedures as slash commands (compiles first, then copies
REM the self-contained output). Prefers the 'py' launcher, falls back to 'python' on PATH.
REM Set AGENT_MEMORY_TARGET_DIR to override the default ~/.claude/commands target.

setlocal
set "PY_SCRIPT=%~dp0setup-all-claude-code.py"

REM Resolve a REAL interpreter, never the WindowsApps App Execution Alias. That "python.exe" is a
REM 0-byte reparse point: it satisfies `where`, so a name-based check reports success, but running
REM it just opens the Microsoft Store and installs nothing - the installer then appears to do
REM nothing at all. Same trap as the System32 WSL "bash" that used to break the overlay installer.
REM Keep the resolved full path, so the later call cannot re-resolve onto the alias.
set "PYTHON="
for /f "delims=" %%i in ('where py 2^>nul ^| findstr /v /i "WindowsApps"') do if not defined PYTHON set "PYTHON=%%i"
if not defined PYTHON for /f "delims=" %%i in ('where python 2^>nul ^| findstr /v /i "WindowsApps"') do if not defined PYTHON set "PYTHON=%%i"

if not defined PYTHON (
    echo ERROR: Python not found on PATH. Install Python 3.12+ ^(python.org^) and retry.
    echo %cmdcmdline% | find /i "%~nx0" >nul && pause
    exit /b 9
)

"%PYTHON%" "%PY_SCRIPT%" %*
set "RC=%ERRORLEVEL%"

REM Pause only when double-clicked, so the window doesn't flash shut on the result.
echo %cmdcmdline% | find /i "%~nx0" >nul && pause
exit /b %RC%
