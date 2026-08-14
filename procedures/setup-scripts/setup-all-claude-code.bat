@echo off
REM setup-all-claude-code.bat - Windows wrapper for setup-all-claude-code.py.
REM Installs the agent-memory CORE procedures as slash commands (compiles first, then copies
REM the self-contained output). Prefers the 'py' launcher, falls back to 'python'.
REM Set AGENT_MEMORY_TARGET_DIR to override the default ~/.claude/commands target.

setlocal
set "PY_SCRIPT=%~dp0setup-all-claude-code.py"

set "PYTHON="
for %%P in (py python) do if not defined PYTHON (where %%P >nul 2>nul && set "PYTHON=%%P")

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
