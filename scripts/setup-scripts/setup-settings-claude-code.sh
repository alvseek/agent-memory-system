#!/bin/bash
# setup-settings-claude-code.sh - Configure ~/.claude/settings.json + ~/.claude.json
#
# Configures:
#   - Stop hook: Audio notification (stop.wav) when Claude finishes responding
#   - SessionStart:compact hook: Memory refresh after context compaction
#   - Bypass permissions: Skip permission prompts for tool executions (prompted)
#   - Disable attribution: Removes Co-Authored-By trailer from commits and PRs
#   - Disable Remote Control: Stops the bridge auto-connecting at every session start
#   - Read tool token limit: Increases from 10K to 64K in ~/.claude.json Statsig flag
#
# Uses Node.js for safe JSON merging (guaranteed available — Claude Code requires it)
#
# Usage: bash control-files/scripts/setup-scripts/setup-settings-claude-code.sh

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPTS_DIR="$(dirname "$SCRIPT_DIR")"  # control-files/scripts/

# Verify hook files exist
if [ ! -f "$SCRIPTS_DIR/stop.wav" ]; then
    echo "ERROR: stop.wav not found at $SCRIPTS_DIR/stop.wav"
    exit 1
fi

if [ ! -f "$SCRIPTS_DIR/claude-agent-refresh.sh" ]; then
    echo "ERROR: claude-agent-refresh.sh not found at $SCRIPTS_DIR/claude-agent-refresh.sh"
    exit 1
fi

# Verify Node.js is available
if ! command -v node &>/dev/null; then
    echo "ERROR: Node.js is required but not found. Claude Code requires Node.js — please install it first."
    exit 1
fi

# Detect bash full path for Windows hook commands
if [[ "$OSTYPE" == "msys" || "$OSTYPE" == "cygwin" ]]; then
    BASH_FULL_PATH=$(cygpath -w "$(which bash)")
else
    BASH_FULL_PATH="bash"
fi

# Prompt for bypass permissions (only if not already configured)
ENABLE_BYPASS=""
if node -e "const p=require('path').join(require('os').homedir(),'.claude','settings.json');try{const s=JSON.parse(require('fs').readFileSync(p,'utf8'));process.exit(s.permissions&&s.permissions.defaultMode?0:1)}catch(e){process.exit(1)}" 2>/dev/null; then
    ENABLE_BYPASS="skip"
else
    echo ""
    read -r -p "  Enable bypass permissions? Skips permission prompts for all tool executions. (Y/n) " bypass_answer
    if [[ -z "$bypass_answer" || "$bypass_answer" =~ ^[Yy] ]]; then
        ENABLE_BYPASS="yes"
    else
        ENABLE_BYPASS="no"
    fi
fi

# Export for Node.js
export SCRIPTS_DIR BASH_FULL_PATH ENABLE_BYPASS

node << 'NODEJS_SCRIPT'
const fs = require('fs');
const path = require('path');
const os = require('os');

const settingsPath = path.join(os.homedir(), '.claude', 'settings.json');
const scriptsDir = process.env.SCRIPTS_DIR;
const bashFullPath = process.env.BASH_FULL_PATH;
const enableBypass = process.env.ENABLE_BYPASS;
const isWindows = os.platform() === 'win32';

// Convert Git Bash paths (/c/Users/...) to Windows paths (C:\Users\...)
function toNativePath(p) {
    if (isWindows && p.startsWith('/')) {
        return p.replace(/^\/([a-z])\//, (_, d) => d.toUpperCase() + ':\\').replace(/\//g, '\\');
    }
    return p;
}

const stopWavPath = toNativePath(scriptsDir + '/stop.wav');
const refreshPath = toNativePath(scriptsDir + '/claude-agent-refresh.sh');

// Read existing settings
let settings = {};
try {
    if (fs.existsSync(settingsPath)) {
        settings = JSON.parse(fs.readFileSync(settingsPath, 'utf8'));
    }
} catch (e) {
    console.error('  ERROR: Failed to parse settings.json: ' + e.message);
    process.exit(1);
}

// Ensure hooks object
if (!settings.hooks) settings.hooks = {};

let changed = false;

// --- Bypass permissions ---
if (enableBypass === 'yes') {
    if (!settings.permissions) settings.permissions = {};
    settings.permissions.defaultMode = 'bypassPermissions';
    console.log('  + Bypass permissions enabled');
    changed = true;
} else if (enableBypass === 'skip') {
    console.log('  = Bypass permissions already configured — skipping');
} else {
    console.log('  - Bypass permissions declined');
}

// --- Disable attribution (Co-Authored-By trailer) ---
if (!settings.attribution || settings.attribution.commit !== '' || settings.attribution.pr !== '') {
    settings.attribution = { commit: '', pr: '' };
    console.log('  + Attribution disabled (no Co-Authored-By in commits/PRs)');
    changed = true;
} else {
    console.log('  = Attribution already disabled — skipping');
}

// --- Remote Control (bridge that auto-connects at every session start) ---
if (settings.remoteControlAtStartup !== false) {
    settings.remoteControlAtStartup = false;
    console.log('  + Remote Control disabled (no bridge connects at session start)');
    changed = true;
} else {
    console.log('  = Remote Control already disabled — skipping');
}

// --- Stop hook (audio notification with stop.wav) ---
const hasStopHook = (settings.hooks.Stop || []).some(entry =>
    (entry.hooks || []).some(h => h.command && h.command.includes('stop.wav'))
);

if (!hasStopHook) {
    const stopCommand = isWindows
        ? "powershell -c (New-Object Media.SoundPlayer '" + stopWavPath + "').PlaySync()"
        : 'aplay ' + stopWavPath + ' || afplay ' + stopWavPath;

    if (!settings.hooks.Stop) settings.hooks.Stop = [];
    settings.hooks.Stop.push({
        hooks: [{ type: 'command', command: stopCommand }]
    });
    console.log('  + Stop hook added (audio notification)');
    changed = true;
} else {
    console.log('  = Stop hook already configured — skipping');
}

// --- SessionStart:compact hook (memory refresh) ---
const hasCompactHook = (settings.hooks.SessionStart || []).some(entry =>
    entry.matcher === 'compact'
);

if (!hasCompactHook) {
    const refreshCommand = isWindows
        ? '"' + bashFullPath + '" ' + refreshPath
        : 'bash ' + refreshPath;

    if (!settings.hooks.SessionStart) settings.hooks.SessionStart = [];
    settings.hooks.SessionStart.push({
        matcher: 'compact',
        hooks: [{ type: 'command', command: refreshCommand }]
    });
    console.log('  + SessionStart:compact hook added (memory refresh)');
    changed = true;
} else {
    console.log('  = SessionStart:compact hook already configured — skipping');
}

// Write back
if (changed) {
    const claudeDir = path.dirname(settingsPath);
    if (!fs.existsSync(claudeDir)) {
        fs.mkdirSync(claudeDir, { recursive: true });
    }
    fs.writeFileSync(settingsPath, JSON.stringify(settings, null, 2) + '\n');
    console.log('');
    console.log('  Settings written to ' + settingsPath);
} else {
    console.log('');
    console.log('  No changes needed — all settings already configured');
}
NODEJS_SCRIPT

settings_status=$?
if [ $settings_status -ne 0 ]; then
    echo ""
    echo "ERROR: Settings setup failed."
    exit $settings_status
fi

# --- Read tool token limit (64K) in ~/.claude.json ---
CLAUDE_JSON_PATH="$(node -e "console.log(require('path').join(require('os').homedir(), '.claude.json'))")"

if [ -f "$CLAUDE_JSON_PATH" ]; then
    node << 'NODEJS_READ_LIMIT'
const fs = require('fs');
const path = require('path');
const os = require('os');

const claudeJsonPath = path.join(os.homedir(), '.claude.json');
try {
    const data = JSON.parse(fs.readFileSync(claudeJsonPath, 'utf8'));
    const flags = data.statsigValues || data.overrides || {};

    // Find tengu_amber_wren in any nested location
    function findAndUpdate(obj) {
        for (const key of Object.keys(obj)) {
            if (key === 'tengu_amber_wren' && typeof obj[key] === 'object') {
                if (obj[key].maxTokens && obj[key].maxTokens < 64000) {
                    obj[key].maxTokens = 64000;
                    return true;
                } else if (obj[key].maxTokens >= 64000) {
                    return false; // already set
                }
            }
            if (typeof obj[key] === 'object' && obj[key] !== null) {
                if (findAndUpdate(obj[key])) return true;
            }
        }
        return false;
    }

    if (findAndUpdate(data)) {
        fs.writeFileSync(claudeJsonPath, JSON.stringify(data, null, 2) + '\n');
        console.log('  + Read tool token limit set to 64K (tengu_amber_wren in ~/.claude.json)');
    } else {
        console.log('  = Read tool token limit already >= 64K — skipping');
    }
} catch (e) {
    console.log('  ! Could not update Read tool limit: ' + e.message);
    console.log('    Manually edit ~/.claude.json → tengu_amber_wren.maxTokens to 64000');
}
NODEJS_READ_LIMIT
else
    echo "  ! ~/.claude.json not found — Read tool limit cannot be set before first Claude Code run."
    echo "    After first run, re-run this script or manually set tengu_amber_wren.maxTokens to 64000."
fi
