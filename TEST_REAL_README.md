# 🧪 Test Real - Guide d'utilisation

Ce fichier contient les instructions détaillées pour utiliser le script `test_real.py` qui permet de tester toutes les fonctionnalités du projet KBot en conditions réelles.

## 📋 Description

`test_real.py` est un script de test complet qui valide tous les composants du projet KBot :
- ✅ Structure des fichiers
- ✅ Informations de version
- ✅ Gestion des configurations
- ✅ Fonctions de reconnaissance d'image
- ✅ Fonctions de combat et d'automation
- ✅ Interface utilisateur
- ✅ Modules principaux

## 🚀 Installation et Prérequis

### Prérequis minimaux
```bash
Python 3.6+
```

### Prérequis optionnels pour un meilleur affichage
```bash
pip install rich
```

### Prérequis complets pour tous les tests
```bash
pip install -r requirements.txt
```

## 🎯 Utilisation

### Mode interactif (recommandé)
```bash
python test_real.py
```
Affiche un menu interactif pour choisir les tests à exécuter.

### Mode automatique
```bash
python test_real.py --auto
```
Exécute tous les tests automatiquement sans interaction.

### Mode rapide
```bash
python test_real.py --quick
```
Exécute uniquement les tests essentiels (structure, version, config).

### Mode rapide automatique
```bash
python test_real.py --auto --quick
```
Combine les modes automatique et rapide.

### Afficher l'aide
```bash
python test_real.py --help
```

## 📊 Types de tests

### 1. Tests de structure
- Vérification de la présence de tous les fichiers requis
- Validation de la structure des dossiers
- Contrôle des images nécessaires

### 2. Tests de version
- Validation des informations de version
- Vérification des métadonnées du projet

### 3. Tests de configuration
- Lecture/écriture de `config.txt`
- Gestion de `config_donjon.json`
- Validation des formats de configuration

### 4. Tests de reconnaissance d'image
- Test des fonctions `locate_image`
- Validation des fonctions de localisation

### 5. Tests de combat
- Fonctions de clic et de mouvement
- Gestion des avatars et du combat
- Automation des actions

### 6. Tests d'interface
- Fonctions de l'interface graphique
- Gestion des configurations via GUI

### 7. Tests des modules principaux
- Validation des modules `main.py`, `main2.py`, `main_donjon.py`
- Tests des fonctions principales

## 🎨 Interface utilisateur

Le script propose deux types d'affichage :

### Avec Rich (recommandé)
- Interface colorée et moderne
- Barres de progression
- Tableaux formatés
- Panneaux informatifs

### Sans Rich (fallback)
- Interface texte basique
- Compatible partout
- Fonctionnel sur tous les systèmes

## 📈 Interprétation des résultats

### Statuts des tests
- ✅ **PASS** : Test réussi
- ❌ **FAIL** : Test échoué (nécessite attention)
- ⏭️ **SKIP** : Test ignoré (dépendances manquantes)
- ℹ️ **INFO** : Information générale

### Résumé final
Le script affiche un tableau récapitulatif avec :
- Nombre total de tests
- Pourcentage de réussite
- Durée d'exécution
- Statut global

## 🔧 Extensibilité

### Ajouter un nouveau test

1. **Créer une méthode de test** dans la classe `KBotRealTester` :
```python
def test_ma_nouvelle_fonctionnalite(self):
    """Test de ma nouvelle fonctionnalité"""
    try:
        # Votre code de test ici
        result = ma_fonction_a_tester()
        if result:
            self.logger.log_test("Mon Test", "PASS", "Test réussi")
        else:
            self.logger.log_test("Mon Test", "FAIL", "Test échoué")
    except Exception as e:
        self.logger.log_test("Mon Test", "FAIL", "Erreur", str(e))
```

2. **Ajouter le test** dans `run_all_tests()` :
```python
test_methods = [
    # ... tests existants ...
    ("Ma nouvelle fonctionnalité", self.test_ma_nouvelle_fonctionnalite),
]
```

### Personnaliser l'affichage

Vous pouvez modifier les couleurs, icônes et formats dans la classe `TestResultLogger`.

## 🐛 Dépannage

### Problème : Modules non trouvés
**Solution** : Installez les dépendances requises :
```bash
pip install -r requirements.txt
```

### Problème : Tests ignorés
**Cause** : Dépendances manquantes (normal en environnement de développement)
**Solution** : Les tests essentiels fonctionnent sans dépendances complètes

### Problème : Interface basique
**Cause** : Library `rich` non installée
**Solution** : 
```bash
pip install rich
```

### Problème : Erreurs de configuration
**Cause** : Fichiers de configuration corrompus
**Solution** : Le script crée automatiquement des configurations de test

## 🎯 Cas d'usage

### Développement
```bash
python test_real.py --quick
```
Tests rapides pendant le développement.

### Intégration continue
```bash
python test_real.py --auto
```
Tests complets pour CI/CD.

### Débogage
```bash
python test_real.py
```
Mode interactif pour cibler des tests spécifiques.

### Production
```bash
python test_real.py --auto --quick
```
Validation rapide avant déploiement.

## 📝 Logs et historique

Le script génère des logs détaillés incluant :
- Timestamp de chaque test
- Détails des succès et échecs
- Messages d'erreur complets
- Durée d'exécution

## 🤝 Contribution

Pour contribuer au script de test :
1. Ajoutez vos tests selon le modèle existant
2. Testez avec et sans dépendances
3. Documentez vos nouvelles fonctionnalités
4. Assurez-vous de la compatibilité avec les deux modes d'affichage

## 📞 Support

En cas de problème :
1. Consultez les logs d'erreur détaillés
2. Vérifiez les prérequis
3. Testez en mode `--quick` d'abord
4. Créez une issue sur GitHub avec les logs d'erreur

---

*Ce script a été conçu pour être robuste, extensible et agréable à utiliser. Il constitue un outil essentiel pour valider le bon fonctionnement du projet KBot.*