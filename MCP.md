# MCP Setup Guide

Guide for setting up MCP (Model Context Protocol) servers with the Agent Memory System. MCP gives your AI agents direct access to databases, APIs, and other tools.

## Database MCP (Google Toolbox)

The recommended database MCP server uses [Google's MCP Toolbox for Databases](https://github.com/googleapis/genai-toolbox) — a standalone binary with a prebuilt Postgres server that auto-connects on startup.

### 1. Download the toolbox binary

```bash
# Windows (PowerShell)
curl.exe -o toolbox.exe "https://storage.googleapis.com/genai-toolbox/v0.27.0/windows/amd64/toolbox.exe"

# Linux
curl -L -o toolbox https://storage.googleapis.com/genai-toolbox/v0.27.0/linux/amd64/toolbox && chmod +x toolbox

# macOS (Apple Silicon)
curl -L -o toolbox https://storage.googleapis.com/genai-toolbox/v0.27.0/darwin/arm64/toolbox && chmod +x toolbox
```

Place the binary somewhere permanent (e.g., `C:\tools\toolbox\toolbox.exe` on Windows).

### 2. Add to your AI agent config

**Global config (recommended)** — add to `~/.claude.json` under `mcpServers`:
```json
{
  "mcpServers": {
    "postgres": {
      "command": "C:\\tools\\toolbox\\toolbox.exe",
      "args": ["--prebuilt", "postgres", "--stdio"],
      "env": {
        "POSTGRES_HOST": "localhost",
        "POSTGRES_PORT": "5432",
        "POSTGRES_DATABASE": "your_database",
        "POSTGRES_USER": "your_user",
        "POSTGRES_PASSWORD": "your_password"
      }
    }
  }
}
```

**Project-level config** — add to `.mcp.json` in project root (same format, scoped to one project).

### 3. Restart your AI agent

Restart Claude Code / Cursor / your agent platform for the MCP to connect.

### Available Postgres MCP Tools

- `mcp__postgres__database_overview` — Server status, version, connections
- `mcp__postgres__list_tables` — Schema information
- `mcp__postgres__execute_sql` — Run SQL queries
- `mcp__postgres__list_indexes` — Index information
- `mcp__postgres__list_query_stats` — Query performance stats

## Docker MCP Toolkit (Optional)

Docker Desktop (v4.48+) includes an MCP Toolkit with a catalog of containerized MCP servers. This is separate from the Google Toolbox above.

### Setup

1. Open Docker Desktop > **Settings** > **Beta features** > Enable **Docker MCP Toolkit**
2. Enable servers: `docker mcp server enable <name>`
3. Connect to client: `docker mcp client connect vscode`

### CLI Reference

```bash
docker mcp catalog show docker-mcp          # Browse available servers
docker mcp server enable <name>              # Enable a server
docker mcp server disable <name>             # Disable a server
docker mcp server list                       # List enabled servers
docker mcp server inspect <name>             # Show server details and tools
docker mcp client connect <client>           # Connect to a client (vscode/cursor)
docker mcp client ls                         # List client status
docker mcp tools list                        # List all available tools
```

## Configuration Levels

| Level | Location | Scope |
|-------|----------|-------|
| Project | `.mcp.json` in project root | Only that project |
| Global (Claude Code) | `~/.claude.json` > `mcpServers` | All Claude Code sessions |
| Global (Claude Desktop) | `claude_desktop_config.json` | All Claude Desktop sessions |

## Troubleshooting

- **MCP not showing in `/mcp`**: Restart your AI agent / reload VSCode window
- **Postgres connection fails**: Ensure your PostgreSQL server is running and credentials are correct
- **Docker MCP servers**: Use `host.docker.internal` instead of `localhost` for host services (Docker containers can't reach host ports via localhost)
