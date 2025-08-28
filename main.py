import pyautogui
import time
import os

from donjon_utils import (
    load_config,
    locate_image,
    click_location,
    fight_loop,
    wait_for_avatar  # 👈 ajoute cette ligne
)
CONFIG_PATH = "config.txt"
IMAGE_PATH = os.path.join("images", "retro")

pyautogui.USE_IMAGE_NOT_FOUND_EXCEPTION = False


def main():
    while True:
        config = load_config()
        if not config:
            time.sleep(1)
            continue

        mob = locate_image("mob.png")
        if mob:
            click_location(mob, config["delay"])
            time.sleep(config["delay"])

            # On attend l’apparition du premier avatar (début du combat)
            if not wait_for_avatar(config["delay"], max_misses=5):
                continue

            # On entre dans la boucle de combat
            fight_loop(config)
        else:
            time.sleep(0.5)


if __name__ == "__main__":
    main()
