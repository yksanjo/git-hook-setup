#!/usr/bin/env python3
"""CLI entry point for git-hook-setup."""

import os
import stat
from pathlib import Path
import click
from src.hooks import (
    install_pre_commit_hook,
    install_commit_msg_hook,
    list_hooks,
    remove_hook,
    get_hook_path,
)


@click.group()
def main():
    """Git Hook Setup - Manage git hooks easily."""
    pass


@main.command()
@click.argument('hook_type', type=click.Choice(['pre-commit', 'commit-msg', 'pre-push']))
@click.option('--linter', help='Linter to use (ruff, black, eslint, prettier, etc.)')
@click.option('--formatter', help='Formatter to use (black, prettier, etc.)')
@click.option('--test', is_flag=True, help='Run tests before commit')
@click.option('--custom', help='Path to custom hook script')
def install(hook_type, linter, formatter, test, custom):
    """Install a git hook."""
    
    git_dir = Path('.git')
    if not git_dir.exists():
        click.echo("Error: Not a git repository. Run 'git init' first.", err=True)
        return
    
    hooks_dir = git_dir / 'hooks'
    hooks_dir.mkdir(exist_ok=True)
    
    if hook_type == 'pre-commit':
        install_pre_commit_hook(hooks_dir, linter, formatter, test, custom)
        click.echo(f"✅ Pre-commit hook installed successfully!")
    elif hook_type == 'commit-msg':
        install_commit_msg_hook(hooks_dir)
        click.echo(f"✅ Commit-msg hook installed successfully!")
    elif hook_type == 'pre-push':
        if test:
            install_pre_commit_hook(hooks_dir, linter, formatter, test=True, custom=custom, hook_name='pre-push')
            click.echo(f"✅ Pre-push hook installed successfully!")
        else:
            click.echo("Error: Pre-push hook requires --test flag", err=True)
            return


@main.command()
def list():
    """List installed git hooks."""
    hooks = list_hooks()
    
    if not hooks:
        click.echo("No hooks installed.")
        return
    
    click.echo("Installed hooks:")
    for hook_name, hook_path in hooks.items():
        click.echo(f"  {hook_name}: {hook_path}")


@main.command()
@click.argument('hook_name')
def remove(hook_name):
    """Remove a git hook."""
    if remove_hook(hook_name):
        click.echo(f"✅ Hook '{hook_name}' removed successfully!")
    else:
        click.echo(f"Error: Hook '{hook_name}' not found.", err=True)


if __name__ == '__main__':
    main()


