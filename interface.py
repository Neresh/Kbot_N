import customtkinter as ctk
from tkinter import messagebox
import subprocess
import os
from PIL import Image
import json
import tkinter as tk
from version import get_version


CONFIG_PATH = "config.txt"
CONFIG_DONJON_PATH = "config_donjon.json"

# === Fonctions utilitaires ===
def lire_config():
    if not os.path.exists(CONFIG_PATH):
        with open(CONFIG_PATH, "w") as f:
            f.write("retro\n1\n512,433\n0.5\np\nm\non\noff\n400,400\n")
        return []
    with open(CONFIG_PATH, "r") as f:
        lines = f.read().splitlines()
    # Remplir les lignes manquantes
    while len(lines) < 9:
        if len(lines) == 7:
            lines.append("on")
        else:
            lines.append("400,400")
    return lines

def enregistrer_config(version, mode, coords, delay, spell_key, alt_spell_key, etat="on", move_enabled=False, move_coords="400,400"):
    move_status = "on" if move_enabled else "off"
    lines = [version, mode, coords, str(delay), spell_key, alt_spell_key, etat, move_status, move_coords]
    with open(CONFIG_PATH, "w") as f:
        f.write("\n".join(lines) + "\n")

def enregistrer_et_lancer():
    version = version_var.get()
    mode = mode_var.get()
    coords = coord_var.get()
    delay = delay_var.get()
    spell_key = spell_key_var.get()
    alt_spell_key = alt_spell_key_var.get()
    move_enabled = move_enabled_var.get()
    move_coords = move_coords_var.get()

    if not coords or "," not in coords:
        messagebox.showerror("Erreur", "Coordonnées invalides. Format attendu : x,y")
        return

    try:
        float(delay)
    except ValueError:
        messagebox.showerror("Erreur", "La latence doit être un nombre (ex: 0.5)")
        return

    enregistrer_config(version, mode, coords, delay, spell_key, alt_spell_key, etat="on", move_enabled=move_enabled, move_coords=move_coords)
    messagebox.showinfo("Configuration", "✅ Configuration enregistrée.\nLe bot démarre...")
    script = "main2.py" if version == "2.0" else "main.py"
    subprocess.Popen(["python", script], creationflags=subprocess.CREATE_NEW_CONSOLE)

def arreter_bot():
    try:
        lines = lire_config()
        if not lines or len(lines) < 7:
            messagebox.showerror("Erreur", "Fichier config invalide ou incomplet.")
            return
        lines[6] = "off"
        with open(CONFIG_PATH, "w") as f:
            f.write("\n".join(lines) + "\n")
        messagebox.showinfo("Bot", "⛔ Le bot a été arrêté.")
    except Exception as e:
        messagebox.showerror("Erreur", f"Impossible d'arrêter le bot : {e}")

# === Config Donjon JSON ===
def lire_config_donjon():
    if not os.path.exists(CONFIG_DONJON_PATH):
        config = {
            "nb_salles": 3,
            "salles": [
                {"mode": "1", "move_enabled": False, "coords": "", "move_coords": ""}
                for _ in range(3)
            ]
        }
        with open(CONFIG_DONJON_PATH, "w") as f:
            json.dump(config, f, indent=4)
        return config
    with open(CONFIG_DONJON_PATH, "r") as f:
        return json.load(f)

def enregistrer_config_donjon(config):
    with open(CONFIG_DONJON_PATH, "w") as f:
        json.dump(config, f, indent=4)

# === Interface ===
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title(f"KBOT {get_version()}")
root.geometry("500x1100")
root.resizable(False, False)

default_font = ctk.CTkFont(family="Lato", size=14)
title_font = ctk.CTkFont(family="Lato", size=14, weight="bold")
small_font = ctk.CTkFont(family="Lato", size=12)

lines = lire_config()
version_var = ctk.StringVar(value=lines[0] if lines else "retro")
mode_var = ctk.StringVar(value=lines[1] if lines else "1")
coord_var = ctk.StringVar(value=lines[2] if lines else "512,433")
delay_var = ctk.StringVar(value=lines[3] if lines else "0.5")
spell_key_var = ctk.StringVar(value=lines[4] if lines else "p")
alt_spell_key_var = ctk.StringVar(value=lines[5] if lines else "m")
move_enabled_var = ctk.BooleanVar(value=(lines[7] == "on") if len(lines) >= 8 else False)
move_coords_var = ctk.StringVar(value=lines[8] if len(lines) >= 9 else "400,400")

# Logo
logo_img = ctk.CTkImage(light_image=Image.open("logo.png"), dark_image=Image.open("logo.png"), size=(406, 125))
logo_label = ctk.CTkLabel(root, image=logo_img, text="")
logo_label.pack(pady=(20, 10))

tabview = ctk.CTkTabview(root, width=460, height=860)
tabview.pack(padx=20, pady=10, fill="both", expand=True)

tabview.add("Farmer une map")
tabview.add("Farmer un donjon")

# Onglet Farmer une map
main_frame = tabview.tab("Farmer une map")

def section(title):
    return ctk.CTkLabel(main_frame, text=title.upper(), font=title_font, anchor="w")

def section_frame():
    f = ctk.CTkFrame(main_frame, corner_radius=10)
    f.pack(fill="x", padx=10, pady=10)
    return f

# Version
section("Version de Dofus").pack(anchor="w", padx=20)
f = section_frame()
ctk.CTkRadioButton(f, text="Dofus Retro", variable=version_var, value="retro", font=default_font).pack(anchor="w", padx=20, pady=2)
ctk.CTkRadioButton(f, text="Dofus 2.0", variable=version_var, value="2.0", font=default_font).pack(anchor="w", padx=20, pady=2)

# Mode
section("Mode de combat").pack(anchor="w", padx=20)
f = section_frame()
ctk.CTkRadioButton(f, text="Mode 1 - Attaque les mobs directement", variable=mode_var, value="1", font=default_font).pack(anchor="w", padx=20, pady=2)
ctk.CTkRadioButton(f, text="Mode 2 - Attaque une case spécifique", variable=mode_var, value="2", font=default_font).pack(anchor="w", padx=20, pady=2)
ctk.CTkRadioButton(f, text="Mode 3 - Sadida Fourbe (3 sorts auto)", variable=mode_var, value="3", font=default_font).pack(anchor="w", padx=20, pady=2)

# Coordonnées & Latence
section("Coordonnées & Latence").pack(anchor="w", padx=20)
f = section_frame()
ctk.CTkLabel(f, text="Coordonnées (x,y) :", font=default_font).pack(anchor="w", padx=20, pady=(5, 0))
ctk.CTkEntry(f, textvariable=coord_var, font=default_font).pack(padx=20, fill="x")
ctk.CTkLabel(f, text="Latence entre clics (sec) :", font=default_font).pack(anchor="w", padx=20, pady=(10, 0))
ctk.CTkEntry(f, textvariable=delay_var, font=default_font).pack(padx=20, fill="x")

# Sorts
section("Sorts").pack(anchor="w", padx=20)
f = section_frame()
ctk.CTkLabel(f, text="Touche pour lancer le sort principal :", font=default_font).pack(anchor="w", padx=20, pady=(5, 0))
ctk.CTkEntry(f, textvariable=spell_key_var, font=default_font).pack(padx=20, fill="x")
ctk.CTkLabel(f, text="Touche pour lancer le sort alternatif :", font=default_font).pack(anchor="w", padx=20, pady=(10, 0))
ctk.CTkEntry(f, textvariable=alt_spell_key_var, font=default_font).pack(padx=20, fill="x")

# Déplacement
section("Déplacement automatique").pack(anchor="w", padx=20)
f = section_frame()
ctk.CTkCheckBox(f, text="Effectuer un déplacement au début du combat", variable=move_enabled_var, font=default_font).pack(anchor="w", padx=20, pady=5)
ctk.CTkLabel(f, text="Coordonnées de déplacement (x,y) :", font=default_font).pack(anchor="w", padx=20, pady=(5, 0))
ctk.CTkEntry(f, textvariable=move_coords_var, font=default_font).pack(padx=20, fill="x")

ctk.CTkLabel(main_frame,
             text="\nSort principal : utilisé au début du combat.\nSort alternatif : utilisé si le combat dure > 10s.",
             font=small_font, text_color="#999999").pack(padx=20, pady=(10, 10), anchor="w")

btn_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
btn_frame.pack(pady=20)
ctk.CTkButton(btn_frame, text="✔ Lancer", command=enregistrer_et_lancer, font=ctk.CTkFont(size=18), fg_color="#00a1dc", width=140, height=50).pack(side="left", padx=20)
ctk.CTkButton(btn_frame, text="⛔ Arrêter", command=arreter_bot, font=ctk.CTkFont(size=18), fg_color="#a51212", width=140, height=50).pack(side="left", padx=20)

# Onglet Farmer un donjon
donjon_frame = tabview.tab("Farmer un donjon")

ctk.CTkLabel(donjon_frame, text="Configuration du Donjon", font=title_font).pack(anchor="w", padx=20, pady=10)

# Donjon config widgets

# Charge la config JSON au démarrage
donjon_config = lire_config_donjon()

def update_salles_frame():
    # Nettoie le cadre avant de reconstruire
    for widget in salles_frame.winfo_children():
        widget.destroy()

    nb = nb_salles_var.get()
    donjon_config["nb_salles"] = nb
    # Ajuste la liste des salles au besoin
    while len(donjon_config["salles"]) < nb:
        donjon_config["salles"].append({"mode": "1", "coords": [], "move_enabled": False, "move_coords": []})
    while len(donjon_config["salles"]) > nb:
        donjon_config["salles"].pop()

    for i in range(nb):
        salle = donjon_config["salles"][i]
        frame = ctk.CTkFrame(salles_frame, corner_radius=10, fg_color="#222222")
        frame.pack(fill="x", pady=8, padx=10)

        ctk.CTkLabel(frame, text=f"Salle {i+1}", font=title_font).pack(anchor="w", pady=(5,0), padx=10)

        # Mode
        mode_var = ctk.StringVar(value=salle.get("mode", "1"))

        def on_mode_change(var=mode_var, idx=i):
            donjon_config["salles"][idx]["mode"] = var.get()
            update_salles_frame()

        mode_frame = ctk.CTkFrame(frame, fg_color="transparent")
        mode_frame.pack(anchor="w", padx=10, pady=(5,0))
        ctk.CTkLabel(mode_frame, text="Mode :", font=default_font).pack(side="left")
        for val, txt in [("1", "1"), ("2", "2"), ("3", "3")]:
            ctk.CTkRadioButton(mode_frame, text=txt, variable=mode_var, value=val, command=on_mode_change).pack(side="left", padx=6)

        # Coordonnées case à cibler (si mode 2)
        if mode_var.get() == "2":
            coords_val = salle.get("coords", [])
            coords_str = f"{coords_val[0]},{coords_val[1]}" if isinstance(coords_val, list) and len(coords_val) == 2 else ""
            coords_var = ctk.StringVar(value=coords_str)

            def on_coords_change(var=coords_var, idx=i):
                val = var.get()
                try:
                    x, y = map(int, val.split(","))
                    donjon_config["salles"][idx]["coords"] = [x, y]
                except Exception:
                    donjon_config["salles"][idx]["coords"] = []

            ctk.CTkLabel(frame, text="Coords case à cibler (x,y) :", font=default_font).pack(anchor="w", padx=20, pady=(5,0))
            coords_entry = ctk.CTkEntry(frame, textvariable=coords_var, font=default_font)
            coords_entry.pack(fill="x", padx=20)
            coords_var.trace_add("write", lambda *_: on_coords_change())

        # Déplacement activé
        move_var = ctk.BooleanVar(value=salle.get("move_enabled", False))

        def on_move_change(var=move_var, idx=i):
            donjon_config["salles"][idx]["move_enabled"] = var.get()
            update_salles_frame()

        move_chk = ctk.CTkCheckBox(frame, text="Activer déplacement", variable=move_var, command=on_move_change, font=default_font)
        move_chk.pack(anchor="w", padx=20, pady=(10,0))

        # Coordonnées déplacement (si déplacement activé)
        if move_var.get():
            move_coords_val = salle.get("move_coords", [])
            move_coords_str = f"{move_coords_val[0]},{move_coords_val[1]}" if isinstance(move_coords_val, list) and len(move_coords_val) == 2 else ""
            move_coords_var = ctk.StringVar(value=move_coords_str)

            def on_move_coords_change(var=move_coords_var, idx=i):
                val = var.get()
                try:
                    x, y = map(int, val.split(","))
                    donjon_config["salles"][idx]["move_coords"] = [x, y]
                except Exception:
                    donjon_config["salles"][idx]["move_coords"] = []

            ctk.CTkLabel(frame, text="Coords déplacement (x,y) :", font=default_font).pack(anchor="w", padx=20, pady=(5,0))
            move_coords_entry = ctk.CTkEntry(frame, textvariable=move_coords_var, font=default_font)
            move_coords_entry.pack(fill="x", padx=20)
            move_coords_var.trace_add("write", lambda *_: on_move_coords_change())

# Nombre de salles
nb_salles_var = ctk.IntVar(value=donjon_config.get("nb_salles", 3))
ctk.CTkLabel(donjon_frame, text="Nombre de salles :", font=default_font).pack(anchor="w", padx=20)
nb_salles_spinbox = tk.Spinbox(donjon_frame, from_=1, to=10, textvariable=nb_salles_var, command=update_salles_frame, width=5)
nb_salles_spinbox.pack(anchor="w", padx=20, pady=(0,10))

# Frame pour les salles
salles_frame = ctk.CTkScrollableFrame(donjon_frame, width=440, height=500, corner_radius=10)
salles_frame.pack(padx=20, pady=10, fill="both", expand=True)

# Initial render
update_salles_frame()

# Bouton lancer donjon
def lancer_donjon():
    for i, salle in enumerate(donjon_config["salles"]):
        if salle["mode"] == "2":
            coords = salle.get("coords", [])
            if not (isinstance(coords, list) and len(coords) == 2 and all(isinstance(c, int) for c in coords)):
                messagebox.showerror("Erreur", f"Coordonnées invalides pour la salle {i+1} (case ciblée).")
                return
        if salle.get("move_enabled", False):
            move_coords = salle.get("move_coords", [])
            if not (isinstance(move_coords, list) and len(move_coords) == 2 and all(isinstance(c, int) for c in move_coords)):
                messagebox.showerror("Erreur", f"Coordonnées déplacement invalides pour la salle {i+1}.")
                return
    donjon_config["nb_salles"] = nb_salles_var.get()
    enregistrer_config_donjon(donjon_config)
    messagebox.showinfo("Donjon", "✅ Configuration du donjon enregistrée.\nLe bot démarre...")
    subprocess.Popen(["python", "main_donjon.py"], creationflags=subprocess.CREATE_NEW_CONSOLE)

btn_lancer = ctk.CTkButton(donjon_frame, text="🗡️ Farmer le donjon", command=lancer_donjon, font=ctk.CTkFont(size=18), fg_color="#00a1dc", width=200, height=50)
btn_lancer.pack(pady=15)

# Version info at bottom
version_label = ctk.CTkLabel(root, text=f"Version {get_version()}", font=ctk.CTkFont(size=10), text_color="#666666")
version_label.pack(side="bottom", pady=5)


root.mainloop()
