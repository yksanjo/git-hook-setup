# git-hook-setup

Simplify git hook management for code quality. One-command setup for pre-commit hooks, commit message validation, and more.

## Features

- 🚀 One-command setup for git hooks
- 📝 Pre-commit hooks for linting, formatting, and testing
- ✅ Commit message validation (conventional commits)
- 🔧 Support for multiple languages (Python, JavaScript, etc.)
- 🎨 Multiple linter/formatter options
- 🔄 Easy hook management (install, list, remove)

## Installation

```bash
pip install -e .
```

Or install globally:
```bash
pip install .
```

## Usage

### Install Pre-commit Hook

```bash
git-hook-setup install pre-commit --linter ruff
```

### Install Commit Message Hook

```bash
git-hook-setup install commit-msg
```

### List Installed Hooks

```bash
git-hook-setup list
```

### Remove Hooks

```bash
git-hook-setup remove pre-commit
```

## Supported Linters/Formatters

### Python
- **ruff** - Fast Python linter
- **black** - Python code formatter
- **pylint** - Python linter
- **flake8** - Python style checker

### JavaScript/TypeScript
- **eslint** - JavaScript linter
- **prettier** - Code formatter

### General
- **shellcheck** - Shell script linter
- **custom** - Your own script

## Examples

### Python Project with Ruff

```bash
git-hook-setup install pre-commit --linter ruff
```

### JavaScript Project with ESLint

```bash
git-hook-setup install pre-commit --linter eslint
```

### Multiple Hooks

```bash
# Install linting
git-hook-setup install pre-commit --linter ruff

# Install commit message validation
git-hook-setup install commit-msg

# Install testing hook
git-hook-setup install pre-commit --test
```

## Hook Types

### Pre-commit
Runs before each commit to check code quality:
- Linting
- Formatting
- Testing
- Type checking

### Commit-msg
Validates commit messages follow conventional commit format:
- `feat:`, `fix:`, `docs:`, `style:`, `refactor:`, `test:`, `chore:`

## License

MIT License - see LICENSE file for details

## Contributing

Contributions welcome! Please open an issue or submit a pull request.


