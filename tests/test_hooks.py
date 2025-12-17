"""Tests for git hooks."""

import pytest
import os
import tempfile
from pathlib import Path
from src.hooks import (
    install_pre_commit_hook,
    install_commit_msg_hook,
    list_hooks,
    remove_hook,
    get_hook_path,
)


def test_get_hook_path():
    """Test getting hook path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        git_dir = Path('.git')
        git_dir.mkdir()
        hooks_dir = git_dir / 'hooks'
        hooks_dir.mkdir()
        
        hook_path = get_hook_path('pre-commit')
        assert hook_path == hooks_dir / 'pre-commit'


def test_install_pre_commit_hook():
    """Test installing pre-commit hook."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        git_dir = Path('.git')
        git_dir.mkdir()
        hooks_dir = git_dir / 'hooks'
        hooks_dir.mkdir()
        
        install_pre_commit_hook(hooks_dir, linter='ruff')
        
        hook_path = hooks_dir / 'pre-commit'
        assert hook_path.exists()
        assert 'ruff check' in hook_path.read_text()
        assert os.access(hook_path, os.X_OK)  # Check executable


def test_install_commit_msg_hook():
    """Test installing commit-msg hook."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        git_dir = Path('.git')
        git_dir.mkdir()
        hooks_dir = git_dir / 'hooks'
        hooks_dir.mkdir()
        
        install_commit_msg_hook(hooks_dir)
        
        hook_path = hooks_dir / 'commit-msg'
        assert hook_path.exists()
        assert 'conventional commit' in hook_path.read_text().lower()
        assert os.access(hook_path, os.X_OK)


def test_list_hooks():
    """Test listing hooks."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        git_dir = Path('.git')
        git_dir.mkdir()
        hooks_dir = git_dir / 'hooks'
        hooks_dir.mkdir()
        
        install_pre_commit_hook(hooks_dir)
        install_commit_msg_hook(hooks_dir)
        
        hooks = list_hooks()
        assert 'pre-commit' in hooks
        assert 'commit-msg' in hooks


def test_remove_hook():
    """Test removing a hook."""
    with tempfile.TemporaryDirectory() as tmpdir:
        os.chdir(tmpdir)
        git_dir = Path('.git')
        git_dir.mkdir()
        hooks_dir = git_dir / 'hooks'
        hooks_dir.mkdir()
        
        install_pre_commit_hook(hooks_dir)
        assert (hooks_dir / 'pre-commit').exists()
        
        assert remove_hook('pre-commit') is True
        assert not (hooks_dir / 'pre-commit').exists()
        
        assert remove_hook('nonexistent') is False

