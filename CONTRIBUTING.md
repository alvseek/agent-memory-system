# Contributing

Thank you for your interest in the Agent Memory System! This project is a methodology framework for building AI agents with persistent memory, and contributions of all kinds are welcome.

## Table of Contents
- [Ways to Contribute](#ways-to-contribute)
- [Guidelines](#guidelines)
- [Scope](#scope)
- [License](#license)

## Ways to Contribute

### Suggest Improvements
- Open an issue describing the improvement you'd like to see
- Include context on why the change would be valuable
- Reference specific files or procedures if applicable

### Report Problems
- If you find errors in procedures, templates, or documentation, open an issue
- Include the file path and a description of the problem
- If possible, suggest a correction

### Share Your Experience
- If you've built agents using this framework, we'd love to hear about it
- Open a discussion or issue describing your use case and any lessons learned

### Submit Changes
1. Fork the repository
2. Create a branch for your changes
3. Make your modifications
4. Submit a pull request with a clear description of what you changed and why

## Guidelines

- **Keep procedures consistent** — follow the existing structure and formatting patterns used across procedure files
- **Respect the architecture** — changes should align with the 5-layer memory system design (see [ARCHITECTURE.md](ARCHITECTURE.md))
- **Test your templates** — if modifying procedure or plan templates, verify they work with Claude Code's slash command system
- **Cross-platform** — ensure any scripts or paths work on Windows, Linux, and macOS

## Scope

This repository contains the **public control files** (procedures, templates, scripts, and documentation). Agent-specific memory data (episodes, knowledge bases, emotional memories) is private and not part of this repository.

## License

By contributing, you agree that your contributions will be licensed under the [Apache License 2.0](LICENSE) — the same licence as the rest of the repository, procedures and templates included, since an agent executes them the way a runtime executes code.
