"""Tests for the main module."""

from src import __version__


def test_version():
    """Test that the version is correct."""

    assert __version__ == "0.1.0"
