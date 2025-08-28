import json
import time
import os
import pyautogui

from donjon_utils import (
    load_config,
    locate_image,
    click_location,
    fight_loop,
    wait_for_avatar  # 👈 ajoute cette ligne
)



script_dir = os.path.dirname(os.path.abspath(__file__))
CONFIG_DONJON_PATH = os.path.join(script_dir, "config_donjon.json")

def load_config_donjon(path=CONFIG_DONJON_PATH):
    print(f"Tentative d'ouverture du fichier : {path}")
    print(f"Fichier existe ? : {os.path.isfile(path)}")
    with open(path, "r") as f:
        return json.load(f)

def entrer_donjon(delay=0.5):
    print("🚪 Entrée dans le donjon...")

    try:
        # 1) pnj_entree
        pnj_entree = locate_image("pnj_entree.png", confidence=0.8)
        if not pnj_entree:
            print("❌ PNJ d'entrée non trouvé.")
            return False
        pyautogui.moveTo(pnj_entree)
        pyautogui.click()
        time.sleep(delay)

        # 2) parler 
        parler = locate_image("parler.png", confidence=0.8)
        if not parler:
            print("❌ Bouton 'Parler' non trouvé.")
            return False
        pyautogui.moveTo(parler)
        pyautogui.click()
        time.sleep(delay)

        # 3) donner_clef 
        donner_clef = locate_image("donner_clef.png", confidence=0.8)
        if not donner_clef:
            print("❌ Bouton 'Donner clef' non trouvé.")
            return False
        pyautogui.moveTo(donner_clef)
        pyautogui.click()
        time.sleep(delay)

        print("✅ Entrée réussie.")
        return True
    except Exception as e:
        print(f"❌ Échec de l'entrée dans le donjon : {e}")
        return False



def sortir_donjon(delay=0.5):
    print("🚪 Sortie du donjon...")

    try:
        # 1) Trouver et cliquer sur le PNJ sortie
        pnj_sortie = locate_image("pnj_sortie.png", confidence=0.8)
        if not pnj_sortie:
            print("❌ PNJ de sortie non trouvé.")
            return False
        pyautogui.moveTo(pnj_sortie)
        pyautogui.click()
        time.sleep(delay)

        # 2) Trouver et cliquer sur "parler"
        parler = locate_image("parler.png", confidence=0.8)
        if not parler:
            print("❌ Bouton 'Parler' non trouvé.")
            return False
        pyautogui.moveTo(parler)
        pyautogui.click()
        time.sleep(delay)

        # 3) Trouver et cliquer sur "sortir"
        sortir = locate_image("sortir.png", confidence=0.8)
        if not sortir:
            print("❌ Bouton 'Sortir' non trouvé.")
            return False
        pyautogui.moveTo(sortir)
        pyautogui.click()
        time.sleep(delay)

        print("✅ Sortie réussie.")
        return True
    except Exception as e:
        print(f"❌ Échec de sortie : {e}")
        return False


def main():
    salle = 0

    while True:
        config_global = load_config()
        if not config_global:
            time.sleep(1)
            continue

        delay = config_global["delay"]
        spell_key = config_global["spell_key"]
        alt_spell_key = config_global["alt_spell_key"]

        config_donjon = load_config_donjon()
        nb_salles = config_donjon["nb_salles"]
        salles_config = config_donjon["salles"]

        if salle == 0:
            # On entre dans le donjon (clé)
            if entrer_donjon(delay):
                salle = 1
            else:
                print("Erreur à l'entrée du donjon, retry...")
                time.sleep(delay)
                continue

        elif 1 <= salle <= nb_salles:
            print(f"⚔️ En attente d'un groupe pour salle {salle} / {nb_salles}")

            mob = locate_image("mob.png", confidence=0.8)
            if mob:
                click_location(mob, delay)
                time.sleep(delay)

                if not wait_for_avatar(delay, max_misses=2):
                    print("Avatar non détecté, attente du prochain mob...")
                    continue

                # Configuration de la salle actuelle
                salle_config = salles_config[salle - 1]
                
                    # 🐞 Débogage ici
                print(f"Coordonnées salle {salle}:", salle_config["coords"])
                print(f"Déplacement activé ? {salle_config['move_enabled']}, coords déplacement:", salle_config["move_coords"])


                combat_config = {
                    "version": config_global["version"],
                    "mode": salle_config["mode"],
                    "coords": tuple(map(int, salle_config["coords"])),
                    "delay": delay,
                    "spell_key": spell_key,
                    "alt_spell_key": alt_spell_key,
                    "move_enabled": salle_config["move_enabled"],
                    "move_coords": tuple(map(int, salle_config["move_coords"]))
                }

                print(f"⚔️ Combat salle {salle} / {nb_salles} lancé.")
                fight_loop(combat_config)
                salle += 1
                time.sleep(delay)

            else:
                # Pas de mob détecté, on attend un peu et on cherche encore
                time.sleep(0.5)

        elif salle > nb_salles:
            print("Dernière salle terminée, sortie du donjon...")
            if sortir_donjon(delay):
                salle = 0
            else:
                print("Erreur lors de la sortie, retry...")
                time.sleep(delay)

        else:
            # Sécurité : reset si valeur inattendue
            salle = 0
            time.sleep(delay)


if __name__ == "__main__":
    main()
