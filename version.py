"""Version information for KBot."""

__version__ = "1.0.0"
__author__ = "Neresh"
__description__ = "Bot Dofus - Combats & Farming de Donjon Automatisés"


def get_version():
    """Return the current version."""
    return __version__


def get_version_info():
    """Return detailed version information."""
    return {
        "version": __version__,
        "author": __author__,
        "description": __description__
    }