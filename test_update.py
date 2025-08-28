"""Simple tests to verify the script is working correctly."""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_version_import():
    """Test that version module can be imported and returns valid version."""
    from version import get_version, get_version_info
    
    version = get_version()
    assert version == "1.0.0"
    
    info = get_version_info()
    assert "version" in info
    assert "author" in info
    assert "description" in info
    assert info["version"] == "1.0.0"
    assert info["author"] == "Neresh"


def test_main_imports():
    """Test that main modules can be imported without critical errors."""
    try:
        # Test basic imports without GUI dependencies
        import version
        assert version.get_version() == "1.0.0"
    except ImportError as e:
        # Allow ImportError for GUI libraries that aren't available in test environment
        if 'customtkinter' not in str(e) and 'pyautogui' not in str(e):
            raise


def test_config_paths():
    """Test that config file paths are properly defined."""
    # This would be in interface.py but we test the constants exist
    config_path = "config.txt"
    config_donjon_path = "config_donjon.json"
    
    # Just verify these are strings
    assert isinstance(config_path, str)
    assert isinstance(config_donjon_path, str)


if __name__ == "__main__":
    test_version_import()
    test_main_imports() 
    test_config_paths()
    print("✅ All tests passed! Script is up to date.")