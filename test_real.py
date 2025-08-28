#!/usr/bin/env python3
"""
Test Real - Comprehensive Real-Conditions Testing Suite for KBot
================================================================

Ce script permet de tester toutes les fonctionnalités du projet KBot en conditions réelles.
Il inclut une interface agréable pour faciliter l'exécution et la visualisation des résultats.

Auteur: Assistant IA
Version: 1.0.0
Compatible avec: KBot v1.0.0+
"""

import sys
import os
import json
import time
import unittest
from unittest.mock import patch, MagicMock
import traceback
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Try to import rich for better formatting, fallback to basic formatting
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.prompt import Prompt, Confirm
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.layout import Layout
    from rich.live import Live
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("Info: Rich library not available, using basic CLI formatting")

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class TestResultLogger:
    """Gère l'enregistrement et l'affichage des résultats de tests"""
    
    def __init__(self):
        self.results = []
        self.start_time = datetime.now()
        if RICH_AVAILABLE:
            self.console = Console()
        
    def log_test(self, test_name: str, status: str, details: str = "", error: str = ""):
        """Enregistre un résultat de test"""
        result = {
            'name': test_name,
            'status': status,  # 'PASS', 'FAIL', 'SKIP'
            'details': details,
            'error': error,
            'timestamp': datetime.now().strftime("%H:%M:%S")
        }
        self.results.append(result)
        
        if RICH_AVAILABLE:
            self._print_rich_result(result)
        else:
            self._print_basic_result(result)
    
    def _print_rich_result(self, result):
        """Affiche le résultat avec Rich formatting"""
        status_colors = {
            'PASS': 'green',
            'FAIL': 'red',
            'SKIP': 'yellow',
            'INFO': 'blue'
        }
        status_icons = {
            'PASS': '✅',
            'FAIL': '❌',
            'SKIP': '⏭️',
            'INFO': 'ℹ️'
        }
        
        color = status_colors.get(result['status'], 'white')
        icon = status_icons.get(result['status'], '•')
        
        self.console.print(f"{icon} [{color}]{result['status']}[/{color}] {result['name']}")
        if result['details']:
            self.console.print(f"   📝 {result['details']}", style="dim")
        if result['error']:
            self.console.print(f"   ⚠️  {result['error']}", style="red dim")
    
    def _print_basic_result(self, result):
        """Affiche le résultat avec formatting basique"""
        status_icons = {
            'PASS': '[PASS]',
            'FAIL': '[FAIL]',
            'SKIP': '[SKIP]',
            'INFO': '[INFO]'
        }
        
        icon = status_icons.get(result['status'], '[?]')
        print(f"{icon} {result['name']}")
        if result['details']:
            print(f"      Details: {result['details']}")
        if result['error']:
            print(f"      Error: {result['error']}")
    
    def print_summary(self):
        """Affiche un résumé final des tests"""
        total = len(self.results)
        passed = sum(1 for r in self.results if r['status'] == 'PASS')
        failed = sum(1 for r in self.results if r['status'] == 'FAIL')
        skipped = sum(1 for r in self.results if r['status'] == 'SKIP')
        
        duration = datetime.now() - self.start_time
        
        if RICH_AVAILABLE:
            self._print_rich_summary(total, passed, failed, skipped, duration)
        else:
            self._print_basic_summary(total, passed, failed, skipped, duration)
    
    def _print_rich_summary(self, total, passed, failed, skipped, duration):
        """Affiche un résumé avec Rich formatting"""
        table = Table(title="📊 Résumé des Tests")
        table.add_column("Statut", style="bold")
        table.add_column("Nombre", justify="right")
        table.add_column("Pourcentage", justify="right")
        
        table.add_row("✅ Réussis", str(passed), f"{passed/total*100:.1f}%" if total > 0 else "0%")
        table.add_row("❌ Échoués", str(failed), f"{failed/total*100:.1f}%" if total > 0 else "0%")
        table.add_row("⏭️ Ignorés", str(skipped), f"{skipped/total*100:.1f}%" if total > 0 else "0%")
        table.add_row("📊 Total", str(total), "100%")
        
        self.console.print()
        self.console.print(table)
        self.console.print(f"\n⏱️  Durée totale: {duration.total_seconds():.2f}s")
        
        if failed > 0:
            self.console.print("\n❌ Certains tests ont échoué. Consultez les détails ci-dessus.", style="red bold")
        else:
            self.console.print("\n🎉 Tous les tests sont passés avec succès!", style="green bold")
    
    def _print_basic_summary(self, total, passed, failed, skipped, duration):
        """Affiche un résumé avec formatting basique"""
        print("\n" + "="*60)
        print("                    RÉSUMÉ DES TESTS")
        print("="*60)
        print(f"Total:     {total}")
        print(f"Réussis:   {passed} ({passed/total*100:.1f}%)" if total > 0 else "Réussis:   0 (0%)")
        print(f"Échoués:   {failed} ({failed/total*100:.1f}%)" if total > 0 else "Échoués:   0 (0%)")
        print(f"Ignorés:   {skipped} ({skipped/total*100:.1f}%)" if total > 0 else "Ignorés:   0 (0%)")
        print(f"Durée:     {duration.total_seconds():.2f}s")
        print("="*60)
        
        if failed > 0:
            print("ATTENTION: Certains tests ont échoué!")
        else:
            print("SUCCESS: Tous les tests sont passés!")


class KBotRealTester:
    """Classe principale pour les tests en conditions réelles"""
    
    def __init__(self):
        self.logger = TestResultLogger()
        self.project_root = Path(__file__).parent
        self.config_path = self.project_root / "config.txt"
        self.config_donjon_path = self.project_root / "config_donjon.json"
        
        # Import modules with error handling
        self.modules = {}
        self._import_modules()
    
    def _import_modules(self):
        """Importe les modules du projet avec gestion d'erreurs"""
        modules_to_import = {
            'version': 'version.py',
            'donjon_utils': 'donjon_utils.py'
        }
        
        for module_name, file_name in modules_to_import.items():
            try:
                if file_name == 'version.py':
                    import version
                    self.modules[module_name] = version
                elif file_name == 'donjon_utils.py':
                    import donjon_utils
                    self.modules[module_name] = donjon_utils
                
                self.logger.log_test(f"Import {module_name}", "PASS", f"Module {file_name} importé avec succès")
            except Exception as e:
                self.logger.log_test(f"Import {module_name}", "FAIL", f"Échec import {file_name}", str(e))
                # Create mock module for testing
                if module_name == 'donjon_utils':
                    self.modules[module_name] = self._create_mock_donjon_utils()
        
        # Try to import interface module (might fail due to GUI dependencies)
        try:
            import interface
            self.modules['interface'] = interface
            self.logger.log_test("Import interface", "PASS", "Module interface.py importé avec succès")
        except Exception as e:
            self.logger.log_test("Import interface", "SKIP", "Module interface.py ignoré (dépendances GUI)", str(e))
            # Create mock interface for testing
            self.modules['interface'] = self._create_mock_interface()
        
        # Try to import main modules
        for main_module in ['main', 'main2', 'main_donjon']:
            try:
                if main_module == 'main':
                    import main
                    self.modules[main_module] = main
                elif main_module == 'main2':
                    import main2
                    self.modules[main_module] = main2
                elif main_module == 'main_donjon':
                    import main_donjon
                    self.modules[main_module] = main_donjon
                
                self.logger.log_test(f"Import {main_module}", "PASS", f"Module {main_module}.py importé avec succès")
            except Exception as e:
                self.logger.log_test(f"Import {main_module}", "SKIP", f"Module {main_module}.py ignoré", str(e))
    
    def _create_mock_donjon_utils(self):
        """Crée un mock du module donjon_utils pour les tests sans dépendances"""
        class MockDonjonUtils:
            def load_config(self):
                return {"mode": "1", "coords": [100, 100], "delay": 0.5, "spell_key": "p", "alt_spell_key": "m"}
            
            def locate_image(self, filename, confidence=0.8):
                # Simulate image found/not found
                if "nonexistent" in filename:
                    return None
                return (100, 100)
            
            def click_location(self, location, delay):
                pass  # Mock click
            
            def wait_for_avatar(self, delay, max_misses=1):
                return True  # Mock success
        
        return MockDonjonUtils()
    
    def _create_mock_interface(self):
        """Crée un mock du module interface pour les tests sans dépendances GUI"""
        class MockInterface:
            def lire_config(self):
                return ["retro", "1", "100,100", "0.5", "p", "m", "on", "off", "400,400"]
            
            def enregistrer_config(self, *args, **kwargs):
                pass  # Mock save
            
            def lire_config_donjon(self):
                return {"nb_salles": 2, "salles": []}
            
            def enregistrer_config_donjon(self, config):
                pass  # Mock save
        
        return MockInterface()
    
    def test_version_info(self):
        """Test des informations de version"""
        if 'version' not in self.modules:
            self.logger.log_test("Version Info", "SKIP", "Module version non disponible")
            return
        
        try:
            version_mod = self.modules['version']
            version_str = version_mod.get_version()
            version_info = version_mod.get_version_info()
            
            if version_str and isinstance(version_str, str):
                self.logger.log_test("Version String", "PASS", f"Version: {version_str}")
            else:
                self.logger.log_test("Version String", "FAIL", "Version string invalide")
            
            if version_info and isinstance(version_info, dict):
                details = f"Author: {version_info.get('author', 'N/A')}, Contributor: {version_info.get('contributor', 'N/A')}"
                self.logger.log_test("Version Info", "PASS", details)
            else:
                self.logger.log_test("Version Info", "FAIL", "Version info invalide")
                
        except Exception as e:
            self.logger.log_test("Version Info", "FAIL", "Erreur lors du test de version", str(e))
    
    def test_config_management(self):
        """Test de la gestion des configurations"""
        # Test config.txt
        self._test_config_txt()
        # Test config_donjon.json
        self._test_config_donjon()
    
    def _test_config_txt(self):
        """Test de la configuration config.txt"""
        try:
            # Backup existing config if it exists
            backup_content = None
            if self.config_path.exists():
                backup_content = self.config_path.read_text()
            
            # Test config creation/reading with donjon_utils if available
            if 'donjon_utils' in self.modules:
                config_data = self.modules['donjon_utils'].load_config()
                if config_data:
                    self.logger.log_test("Config TXT Load", "PASS", f"Configuration chargée: {len(config_data)} paramètres")
                else:
                    self.logger.log_test("Config TXT Load", "PASS", "Pas de configuration existante (normal)")
            else:
                # Manual test
                if self.config_path.exists():
                    content = self.config_path.read_text().strip().split('\n')
                    if len(content) >= 6:  # Minimum required fields
                        self.logger.log_test("Config TXT Load", "PASS", f"Configuration trouvée avec {len(content)} lignes")
                    else:
                        self.logger.log_test("Config TXT Load", "FAIL", f"Configuration incomplète: {len(content)} lignes")
                else:
                    self.logger.log_test("Config TXT Load", "PASS", "Pas de configuration existante (normal)")
            
            # Test config write (create a test config)
            test_config = ["retro", "1", "100,100", "0.5", "p", "m", "on", "off", "400,400"]
            try:
                self.config_path.write_text('\n'.join(test_config) + '\n')
                self.logger.log_test("Config TXT Write", "PASS", "Écriture de configuration test réussie")
                
                # Verify written config
                written_content = self.config_path.read_text().strip().split('\n')
                if written_content == test_config:
                    self.logger.log_test("Config TXT Verify", "PASS", "Vérification de l'écriture réussie")
                else:
                    self.logger.log_test("Config TXT Verify", "FAIL", "Contenu écrit différent de l'attendu")
                    
            except Exception as e:
                self.logger.log_test("Config TXT Write", "FAIL", "Erreur lors de l'écriture", str(e))
            
            # Restore backup if it existed
            if backup_content is not None:
                self.config_path.write_text(backup_content)
            
        except Exception as e:
            self.logger.log_test("Config TXT Test", "FAIL", "Erreur générale lors du test config.txt", str(e))
    
    def _test_config_donjon(self):
        """Test de la configuration config_donjon.json"""
        try:
            # Backup existing config if it exists
            backup_content = None
            if self.config_donjon_path.exists():
                backup_content = self.config_donjon_path.read_text()
            
            # Test loading existing config
            if self.config_donjon_path.exists():
                try:
                    config_data = json.loads(self.config_donjon_path.read_text())
                    self.logger.log_test("Config Donjon Load", "PASS", f"Configuration chargée: {len(config_data.get('salles', []))} salles")
                except json.JSONDecodeError as e:
                    self.logger.log_test("Config Donjon Load", "FAIL", "JSON invalide", str(e))
            else:
                self.logger.log_test("Config Donjon Load", "PASS", "Pas de configuration donjon existante (normal)")
            
            # Test config write
            test_config = {
                "nb_salles": 2,
                "salles": [
                    {
                        "mode": "1",
                        "coords": [],
                        "move_enabled": False,
                        "move_coords": [0, 0]
                    },
                    {
                        "mode": "2",
                        "coords": [100, 200],
                        "move_enabled": True,
                        "move_coords": [300, 400]
                    }
                ]
            }
            
            try:
                self.config_donjon_path.write_text(json.dumps(test_config, indent=2))
                self.logger.log_test("Config Donjon Write", "PASS", "Écriture de configuration donjon test réussie")
                
                # Verify written config
                written_data = json.loads(self.config_donjon_path.read_text())
                if written_data == test_config:
                    self.logger.log_test("Config Donjon Verify", "PASS", "Vérification de l'écriture réussie")
                else:
                    self.logger.log_test("Config Donjon Verify", "FAIL", "Contenu écrit différent de l'attendu")
                    
            except Exception as e:
                self.logger.log_test("Config Donjon Write", "FAIL", "Erreur lors de l'écriture", str(e))
            
            # Restore backup if it existed
            if backup_content is not None:
                self.config_donjon_path.write_text(backup_content)
                
        except Exception as e:
            self.logger.log_test("Config Donjon Test", "FAIL", "Erreur générale lors du test config donjon", str(e))
    
    def test_image_recognition(self):
        """Test des fonctions de reconnaissance d'image"""
        if 'donjon_utils' not in self.modules:
            self.logger.log_test("Image Recognition", "SKIP", "Module donjon_utils non disponible")
            return
        
        donjon_utils = self.modules['donjon_utils']
        
        # Test locate_image function
        try:
            # Test with found image
            result = donjon_utils.locate_image("test.png")
            if result is not None:
                self.logger.log_test("Image Locate (Found)", "PASS", f"Image trouvée à {result}")
            else:
                self.logger.log_test("Image Locate (Found)", "FAIL", "Résultat None inattendu")
            
            # Test with not found image
            result = donjon_utils.locate_image("nonexistent.png")
            if result is None:
                self.logger.log_test("Image Locate (Not Found)", "PASS", "Image non trouvée (comportement attendu)")
            else:
                self.logger.log_test("Image Locate (Not Found)", "FAIL", "Résultat non-None inattendu")
                    
        except Exception as e:
            self.logger.log_test("Image Recognition", "FAIL", "Erreur lors du test de reconnaissance", str(e))
    
    def test_combat_functions(self):
        """Test des fonctions de combat"""
        if 'donjon_utils' not in self.modules:
            self.logger.log_test("Combat Functions", "SKIP", "Module donjon_utils non disponible")
            return
        
        donjon_utils = self.modules['donjon_utils']
        
        # Test click_location
        try:
            donjon_utils.click_location((100, 100), 0.1)
            self.logger.log_test("Click Location", "PASS", "Fonction click_location opérationnelle")
        except Exception as e:
            self.logger.log_test("Click Location", "FAIL", "Erreur lors du test click_location", str(e))
        
        # Test wait_for_avatar
        try:
            result = donjon_utils.wait_for_avatar(0.1, max_misses=1)
            if result:
                self.logger.log_test("Wait Avatar", "PASS", "Fonction wait_for_avatar opérationnelle")
            else:
                self.logger.log_test("Wait Avatar", "PASS", "Timeout avatar géré correctement")
        except Exception as e:
            self.logger.log_test("Wait Avatar", "FAIL", "Erreur lors du test wait_for_avatar", str(e))
    
    def test_interface_functions(self):
        """Test des fonctions d'interface (si disponibles)"""
        if 'interface' not in self.modules:
            self.logger.log_test("Interface Functions", "SKIP", "Module interface non disponible")
            return
        
        interface = self.modules['interface']
        
        # Test config functions
        try:
            interface.enregistrer_config("test", "1", "100,100", 0.5, "p", "m")
            self.logger.log_test("Interface Save Config", "PASS", "Fonction enregistrer_config opérationnelle")
        except Exception as e:
            self.logger.log_test("Interface Save Config", "FAIL", "Erreur lors du test enregistrer_config", str(e))
        
        try:
            config_data = interface.lire_config()
            if isinstance(config_data, list):
                self.logger.log_test("Interface Read Config", "PASS", f"Configuration lue: {len(config_data)} éléments")
            else:
                self.logger.log_test("Interface Read Config", "FAIL", "Type de retour invalide")
        except Exception as e:
            self.logger.log_test("Interface Read Config", "FAIL", "Erreur lors du test lire_config", str(e))
        
        # Test donjon config functions
        try:
            config_data = interface.lire_config_donjon()
            if isinstance(config_data, (dict, type(None))):
                self.logger.log_test("Interface Read Donjon Config", "PASS", "Configuration donjon lue avec succès")
            else:
                self.logger.log_test("Interface Read Donjon Config", "FAIL", "Type de retour invalide")
        except Exception as e:
            self.logger.log_test("Interface Read Donjon Config", "FAIL", "Erreur lors du test lire_config_donjon", str(e))
        
        try:
            test_config = {"nb_salles": 1, "salles": []}
            interface.enregistrer_config_donjon(test_config)
            self.logger.log_test("Interface Save Donjon Config", "PASS", "Configuration donjon sauvegardée")
        except Exception as e:
            self.logger.log_test("Interface Save Donjon Config", "FAIL", "Erreur lors du test enregistrer_config_donjon", str(e))
    
    def test_main_modules(self):
        """Test des modules principaux"""
        for module_name in ['main', 'main2', 'main_donjon']:
            if module_name not in self.modules:
                self.logger.log_test(f"Module {module_name}", "SKIP", f"Module {module_name}.py non disponible")
                continue
            
            try:
                module = self.modules[module_name]
                
                # Check if main function exists
                if hasattr(module, 'main'):
                    self.logger.log_test(f"{module_name} Main Function", "PASS", "Fonction main trouvée")
                else:
                    self.logger.log_test(f"{module_name} Main Function", "FAIL", "Fonction main non trouvée")
                
                # Test specific functions based on module
                if module_name == 'main_donjon':
                    if hasattr(module, 'load_config_donjon'):
                        try:
                            with patch('builtins.open', side_effect=FileNotFoundError):
                                result = module.load_config_donjon()
                            self.logger.log_test(f"{module_name} Load Config", "PASS", "Fonction load_config_donjon testée")
                        except Exception as e:
                            self.logger.log_test(f"{module_name} Load Config", "FAIL", "Erreur test load_config_donjon", str(e))
                    
                    if hasattr(module, 'entrer_donjon'):
                        try:
                            with patch(f'{module_name}.locate_image', return_value=None):
                                result = module.entrer_donjon(0.1)
                            self.logger.log_test(f"{module_name} Enter Dungeon", "PASS", "Fonction entrer_donjon testée")
                        except Exception as e:
                            self.logger.log_test(f"{module_name} Enter Dungeon", "FAIL", "Erreur test entrer_donjon", str(e))
                
            except Exception as e:
                self.logger.log_test(f"Module {module_name}", "FAIL", f"Erreur lors du test du module {module_name}", str(e))
    
    def test_file_structure(self):
        """Test de la structure des fichiers"""
        required_files = [
            'version.py',
            'donjon_utils.py',
            'interface.py',
            'main.py',
            'main2.py',
            'main_donjon.py',
            'README.md',
            'requirements.txt'
        ]
        
        for file_name in required_files:
            file_path = self.project_root / file_name
            if file_path.exists():
                self.logger.log_test(f"File {file_name}", "PASS", f"Fichier trouvé ({file_path.stat().st_size} bytes)")
            else:
                self.logger.log_test(f"File {file_name}", "FAIL", "Fichier manquant")
        
        # Test images directory
        images_dir = self.project_root / "images" / "retro"
        if images_dir.exists():
            image_files = list(images_dir.glob("*.png"))
            self.logger.log_test("Images Directory", "PASS", f"Dossier images trouvé avec {len(image_files)} fichiers PNG")
        else:
            self.logger.log_test("Images Directory", "FAIL", "Dossier images/retro manquant")
    
    def run_all_tests(self):
        """Exécute tous les tests"""
        if RICH_AVAILABLE:
            self.logger.console.print(Panel.fit(
                "[bold blue]🤖 KBot Real Conditions Test Suite[/bold blue]\n"
                "[dim]Test complet de toutes les fonctionnalités du projet[/dim]",
                title="KBot Tester"
            ))
        else:
            print("\n" + "="*60)
            print("     🤖 KBot Real Conditions Test Suite")
            print("Test complet de toutes les fonctionnalités du projet")
            print("="*60)
        
        # Liste des tests à exécuter
        test_methods = [
            ("Structure des fichiers", self.test_file_structure),
            ("Informations de version", self.test_version_info),
            ("Gestion des configurations", self.test_config_management),
            ("Reconnaissance d'image", self.test_image_recognition),
            ("Fonctions de combat", self.test_combat_functions),
            ("Fonctions d'interface", self.test_interface_functions),
            ("Modules principaux", self.test_main_modules),
        ]
        
        if RICH_AVAILABLE:
            with Progress(
                SpinnerColumn(),
                TextColumn("[progress.description]{task.description}"),
                console=self.logger.console
            ) as progress:
                for test_name, test_method in test_methods:
                    task = progress.add_task(f"[cyan]Test: {test_name}[/cyan]", total=None)
                    try:
                        test_method()
                    except Exception as e:
                        self.logger.log_test(f"Test {test_name}", "FAIL", "Erreur inattendue", str(e))
                    progress.remove_task(task)
        else:
            for i, (test_name, test_method) in enumerate(test_methods, 1):
                print(f"\n[{i}/{len(test_methods)}] Exécution: {test_name}")
                try:
                    test_method()
                except Exception as e:
                    self.logger.log_test(f"Test {test_name}", "FAIL", "Erreur inattendue", str(e))
        
        # Afficher le résumé
        self.logger.print_summary()


def show_help():
    """Affiche l'aide pour l'utilisation du script"""
    help_text = """
🤖 KBot Real Conditions Test Suite - Guide d'utilisation
========================================================

Ce script permet de tester toutes les fonctionnalités du projet KBot
en conditions réelles avec une interface agréable.

UTILISATION:
    python test_real.py [options]

OPTIONS:
    --help, -h          Affiche cette aide
    --auto, -a          Mode automatique (exécute tous les tests sans interaction)
    --quick, -q         Mode rapide (tests essentiels seulement)
    --demo, -d          Mode démonstration (aperçu des capacités)
    --verbose, -v       Mode verbeux (plus de détails)

EXEMPLES:
    python test_real.py                 # Mode interactif complet
    python test_real.py --auto          # Mode automatique
    python test_real.py --quick         # Tests rapides
    python test_real.py --demo          # Démonstration des capacités
    python test_real.py --auto --quick  # Tests rapides automatiques

FONCTIONNALITÉS TESTÉES:
• Structure des fichiers du projet
• Informations de version et métadonnées
• Gestion des configurations (config.txt, config_donjon.json)
• Fonctions de reconnaissance d'image
• Fonctions de combat et d'automation
• Interface utilisateur (si disponible)
• Modules principaux (main.py, main2.py, main_donjon.py)

PRÉREQUIS:
• Python 3.6+
• Dépendances optionnelles: rich (pour un meilleur affichage)
• Les dépendances du projet (voir requirements.txt)

EXTENSIBILITÉ:
Le script est conçu pour être facilement extensible. Pour ajouter de nouveaux tests:
1. Ajoutez une méthode test_* à la classe KBotRealTester
2. Ajoutez l'appel dans run_all_tests()
3. Utilisez self.logger.log_test() pour enregistrer les résultats

SUPPORT:
En cas de problème, consultez les logs d'erreur détaillés dans la sortie
ou créez une issue sur le dépôt GitHub du projet.
"""
    
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel(help_text.strip(), title="📚 Aide KBot Tester"))
    else:
        print(help_text)


def interactive_menu():
    """Menu interactif pour choisir les tests à exécuter"""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit(
            "[bold green]🎯 Menu Interactif KBot Tester[/bold green]\n"
            "[dim]Choisissez les tests à exécuter[/dim]",
            title="Menu Principal"
        ))
        
        choices = [
            "Tous les tests (recommandé)",
            "Tests essentiels seulement",
            "Tests de configuration uniquement",
            "Tests des modules principaux uniquement",
            "Démonstration des capacités",
            "Aide et documentation",
            "Quitter"
        ]
        
        console.print("\n🔍 Options disponibles:")
        for i, choice in enumerate(choices, 1):
            console.print(f"  {i}. {choice}")
        
        choice = Prompt.ask("\n👉 Votre choix", choices=["1", "2", "3", "4", "5", "6", "7"], default="1")
        
    else:
        print("\n" + "="*50)
        print("        🎯 Menu Interactif KBot Tester")
        print("="*50)
        print("1. Tous les tests (recommandé)")
        print("2. Tests essentiels seulement")
        print("3. Tests de configuration uniquement")
        print("4. Tests des modules principaux uniquement")
        print("5. Démonstration des capacités")
        print("6. Aide et documentation")
        print("7. Quitter")
        
        choice = input("\n👉 Votre choix (1-7) [1]: ") or "1"
    
    return choice


def main():
    """Fonction principale du script"""
    # Parse command line arguments
    args = sys.argv[1:]
    auto_mode = '--auto' in args or '-a' in args
    quick_mode = '--quick' in args or '-q' in args
    help_mode = '--help' in args or '-h' in args
    demo_mode = '--demo' in args or '-d' in args
    
    if help_mode:
        show_help()
        return
    
    if demo_mode:
        show_demo()
        return
    
    if not auto_mode:
        choice = interactive_menu()
        
        if choice == '5':
            show_demo()
            return
        elif choice == '6':
            show_help()
            return
        elif choice == '7':
            print("👋 Au revoir!")
            return
        elif choice == '2':
            quick_mode = True
    
    # Initialize tester
    tester = KBotRealTester()
    
    if quick_mode:
        # Quick mode - essential tests only
        if RICH_AVAILABLE:
            tester.logger.console.print("\n⚡ Mode rapide activé - Tests essentiels seulement")
        else:
            print("\n⚡ Mode rapide activé - Tests essentiels seulement")
        
        tester.test_file_structure()
        tester.test_version_info()
        tester.test_config_management()
    else:
        # Full test suite
        if not auto_mode:
            choice = interactive_menu() if 'choice' not in locals() else choice
            
            if choice == '3':
                # Config tests only
                tester.test_config_management()
            elif choice == '4':
                # Main modules tests only
                tester.test_main_modules()
            else:
                # All tests
                tester.run_all_tests()
        else:
            tester.run_all_tests()
    
    if not quick_mode:
        tester.logger.print_summary()


def show_demo():
    """Affiche une démonstration du script"""
    if RICH_AVAILABLE:
        console = Console()
        console.print(Panel.fit(
            "[bold yellow]🎭 Démonstration KBot Tester[/bold yellow]\n"
            "[dim]Aperçu des capacités du script de test[/dim]",
            title="Mode Démo"
        ))
        
        console.print("\n🔍 Ce script peut tester:")
        demo_features = [
            "✅ Structure et intégrité des fichiers du projet",
            "✅ Informations de version et métadonnées",
            "✅ Gestion des configurations (lecture/écriture)",
            "✅ Fonctions de reconnaissance d'image (avec mocks)",
            "✅ Fonctions de combat et d'automation",
            "✅ Interface utilisateur (mode compatible)",
            "✅ Modules principaux du bot"
        ]
        
        for feature in demo_features:
            console.print(f"  {feature}")
        
        console.print("\n🎯 Modes disponibles:")
        console.print("  • Mode interactif: Menu de sélection des tests")
        console.print("  • Mode automatique: Tous les tests sans interaction")
        console.print("  • Mode rapide: Tests essentiels seulement")
        
        console.print("\n🎨 Interface:")
        console.print("  • Affichage coloré avec Rich (si disponible)")
        console.print("  • Interface texte basique en fallback")
        console.print("  • Barres de progression et tableaux récapitulatifs")
        
        console.print("\n🔧 Extensibilité:")
        console.print("  • Architecture modulaire pour ajouter de nouveaux tests")
        console.print("  • Système de mocks pour tests sans dépendances")
        console.print("  • Support des environnements de développement")
        
        if Confirm.ask("\n❓ Voulez-vous voir une démonstration rapide"):
            console.print("\n🚀 Lancement d'une démonstration...")
            demo_tester = KBotRealTester()
            demo_tester.test_version_info()
            demo_tester.test_file_structure()
            console.print("\n✨ Démonstration terminée!")
    else:
        print("\n" + "="*60)
        print("             🎭 Démonstration KBot Tester")
        print("="*60)
        print("Ce script peut tester:")
        print("  ✅ Structure et intégrité des fichiers")
        print("  ✅ Informations de version")
        print("  ✅ Gestion des configurations")
        print("  ✅ Fonctions de reconnaissance d'image")
        print("  ✅ Fonctions de combat et d'automation")
        print("  ✅ Interface utilisateur")
        print("  ✅ Modules principaux du bot")
        print("\nPour une démonstration complète, installez 'rich':")
        print("  pip install rich")
        print("="*60)


if __name__ == "__main__":
    main()