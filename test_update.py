import unittest
from unittest.mock import patch, MagicMock

# Mock dependencies before importing modules that require them
import sys
mock_modules = {
    'customtkinter': MagicMock(),
    'tkinter': MagicMock(),
    'tkinter.messagebox': MagicMock(),
    'PIL': MagicMock(),
    'PIL.Image': MagicMock(),
    'pyautogui': MagicMock(),
    'cv2': MagicMock(),
    'numpy': MagicMock(),
    'pytesseract': MagicMock(),
    'keyboard': MagicMock(),
}

for module_name, mock_module in mock_modules.items():
    sys.modules[module_name] = mock_module

import version
import interface
import donjon_utils
import main
import main_donjon

class TestVersion(unittest.TestCase):
    def test_get_version(self):
        self.assertIsInstance(version.get_version(), str)

    def test_get_version_info(self):
        info = version.get_version_info()
        self.assertIsInstance(info, dict)
        self.assertIn("version", info)
        self.assertIn("author", info)

class TestInterface(unittest.TestCase):
    def test_lire_config(self):
        result = interface.lire_config()
        self.assertIsInstance(result, list)

    def test_enregistrer_config(self):
        # Test call with minimal parameters, skip actual file writing
        with patch("builtins.open", new_callable=MagicMock()):
            interface.enregistrer_config("1.0", "combat", "100,100", 0.5, "A", "B")

    def test_arreter_bot(self):
        with patch("interface.lire_config", return_value=["1.0", "combat", "100,100", "0.5", "A", "B", "on", "off", "400,400"]):
            with patch("builtins.open", new_callable=MagicMock()):
                with patch("tkinter.messagebox.showinfo"), patch("tkinter.messagebox.showerror"):
                    interface.arreter_bot()

    def test_lire_config_donjon(self):
        result = interface.lire_config_donjon()
        self.assertTrue(isinstance(result, dict) or result is None)

    def test_enregistrer_config_donjon(self):
        config = {"test": 1}
        with patch("builtins.open", new_callable=MagicMock()):
            interface.enregistrer_config_donjon(config)

class TestDonjonUtils(unittest.TestCase):
    def test_load_config(self):
        # Should return a dict or None
        result = donjon_utils.load_config()
        self.assertTrue(isinstance(result, dict) or result is None)

    def test_locate_image(self):
        # Mock pyautogui
        with patch("donjon_utils.pyautogui.locateOnScreen", return_value=(10,10,10,10)):
            result = donjon_utils.locate_image("mob.png")
            self.assertTrue(result is None or isinstance(result, tuple))

    def test_click_location(self):
        # Should not throw
        with patch("donjon_utils.pyautogui.moveTo"), patch("donjon_utils.pyautogui.click"):
            donjon_utils.click_location((100, 100), 0.1)

    def test_fight_loop(self):
        # Only test call with minimal config, mock everything
        config = {
            "mode": "1", "coords": (100, 100), "delay": 0.1,
            "spell_key": "A", "alt_spell_key": "B", "move_enabled": False, "move_coords": (400,400), "etat":"on"
        }
        with patch("donjon_utils.locate_image", return_value=(10,10)), \
             patch("donjon_utils.pyautogui.moveTo"), patch("donjon_utils.pyautogui.click"), \
             patch("donjon_utils.pyautogui.press"), patch("donjon_utils.do_turn"), \
             patch("donjon_utils.do_turn_sadida_fourbe"), patch("donjon_utils.post_combat_cleanup"):
            donjon_utils.fight_loop(config)

class TestMainDonjon(unittest.TestCase):
    def test_load_config_donjon(self):
        result = main_donjon.load_config_donjon()
        self.assertTrue(isinstance(result, dict) or result is None)

    def test_entrer_donjon(self):
        with patch("main_donjon.locate_image", return_value=(10,10)), \
             patch("main_donjon.pyautogui.moveTo"), patch("main_donjon.pyautogui.click"):
            main_donjon.entrer_donjon(0.1)

    def test_sortir_donjon(self):
        with patch("main_donjon.locate_image", return_value=(10,10)), \
             patch("main_donjon.pyautogui.moveTo"), patch("main_donjon.pyautogui.click"):
            main_donjon.sortir_donjon(0.1)

if __name__ == "__main__":
    unittest.main()
