"""Git hook management functions."""

import os
import stat
from pathlib import Path
from typing import Dict, Optional


def get_hook_path(hook_name: str) -> Optional[Path]:
    """Get the path to a git hook."""
    git_dir = Path('.git')
    if not git_dir.exists():
        return None
    
    hooks_dir = git_dir / 'hooks'
    return hooks_dir / hook_name


def make_executable(file_path: Path):
    """Make a file executable."""
    current_permissions = os.stat(file_path).st_mode
    os.chmod(file_path, current_permissions | stat.S_IEXEC)


def install_pre_commit_hook(
    hooks_dir: Path,
    linter: Optional[str] = None,
    formatter: Optional[str] = None,
    test: bool = False,
    custom: Optional[str] = None,
    hook_name: str = 'pre-commit'
):
    """Install a pre-commit hook."""
    hook_path = hooks_dir / hook_name
    
    # Build hook script
    script_parts = ["#!/bin/bash\n", "set -e\n\n"]
    
    if custom:
        # Use custom script
        custom_path = Path(custom)
        if custom_path.exists():
            script_parts.append(f"exec {custom_path.absolute()}\n")
        else:
            raise ValueError(f"Custom script not found: {custom}")
    else:
        # Build commands based on options
        commands = []
        
        # Linting
        if linter:
            if linter == 'ruff':
                commands.append("ruff check .")
            elif linter == 'black':
                commands.append("black --check .")
            elif linter == 'pylint':
                commands.append("pylint src/")
            elif linter == 'flake8':
                commands.append("flake8 .")
            elif linter == 'eslint':
                commands.append("npx eslint .")
            elif linter == 'shellcheck':
                commands.append("shellcheck **/*.sh")
        
        # Formatting
        if formatter:
            if formatter == 'black':
                commands.append("black .")
            elif formatter == 'prettier':
                commands.append("npx prettier --write .")
        
        # Testing
        if test:
            # Detect test framework
            if Path('pytest.ini').exists() or Path('pyproject.toml').exists():
                commands.append("pytest")
            elif Path('package.json').exists():
                commands.append("npm test")
            else:
                commands.append("python -m pytest")
        
        if not commands:
            # Default: just check for Python syntax errors
            commands.append("python -m py_compile $(git diff --cached --name-only --diff-filter=ACM | grep '\\.py$') || true")
        
        # Add commands to script
        for cmd in commands:
            script_parts.append(f"{cmd}\n")
    
    # Write hook file
    hook_path.write_text("".join(script_parts))
    make_executable(hook_path)


def install_commit_msg_hook(hooks_dir: Path):
    """Install a commit-msg hook for conventional commits."""
    hook_path = hooks_dir / 'commit-msg'
    
    script = """#!/bin/bash
# Validate commit message format (conventional commits)

commit_msg=$(cat "$1")
pattern="^(feat|fix|docs|style|refactor|test|chore)(\\(.+\\))?: .+"

if ! echo "$commit_msg" | grep -qE "$pattern"; then
    echo "Error: Commit message does not follow conventional commit format."
    echo ""
    echo "Format: <type>(<scope>): <subject>"
    echo ""
    echo "Types: feat, fix, docs, style, refactor, test, chore"
    echo ""
    echo "Example: feat(api): add user authentication"
    exit 1
fi
"""
    
    hook_path.write_text(script)
    make_executable(hook_path)


def list_hooks() -> Dict[str, Path]:
    """List all installed git hooks."""
    git_dir = Path('.git')
    if not git_dir.exists():
        return {}
    
    hooks_dir = git_dir / 'hooks'
    if not hooks_dir.exists():
        return {}
    
    hooks = {}
    common_hooks = ['pre-commit', 'commit-msg', 'pre-push', 'post-commit']
    
    for hook_name in common_hooks:
        hook_path = hooks_dir / hook_name
        if hook_path.exists() and hook_path.is_file():
            hooks[hook_name] = hook_path
    
    return hooks


def remove_hook(hook_name: str) -> bool:
    """Remove a git hook."""
    hook_path = get_hook_path(hook_name)
    
    if hook_path and hook_path.exists():
        hook_path.unlink()
        return True
    
    return False


