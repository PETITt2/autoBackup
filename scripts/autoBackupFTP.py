#!/usr/bin/env python3
"""
Script de sauvegarde automatique des configs Cisco sur un serveur FTP.
"""

from netmiko import ConnectHandler
from ftplib import FTP, error_perm
from datetime import datetime
import os

# ---------------- CONFIGURATION ----------------

# Liste des switches
switches = [
    {
        "host": "192.168.100.38",
        "username": "admin",
        "password": "admin",
        "secret": "admin",
        "name": "switch1"
    }
]

# FTP
ftp_host = "192.168.100.36"
ftp_user = "sauvegarde"
ftp_pass = "sauvegarde"
ftp_folder = "configs"  # dossier racine sur le FTP

# Dossier temporaire local pour stocker les configs avant FTP
local_temp_dir = "/tmp/switch_backup"
os.makedirs(local_temp_dir, exist_ok=True)

# ---------------- FONCTIONS ----------------

def ftp_ensure_dir(ftp, dirname):
    """Crée un dossier sur le FTP s'il n'existe pas encore."""
    try:
        ftp.cwd(dirname)
    except error_perm:
        ftp.mkd(dirname)
        ftp.cwd(dirname)

def backup_switch(switch):
    """Se connecte au switch, récupère la config et l'envoie dans le dossier FTP du switch"""
    try:
        print(f"[INFO] Connexion à {switch['name']} ({switch['host']})...")
        device = ConnectHandler(
            device_type="cisco_ios",
            host=switch['host'],
            username=switch['username'],
            password=switch['password'],
            secret=switch['secret']
        )
        device.enable()

        # Récupération de la configuration
        running_config = device.send_command("show startup-config")
        device.disconnect()

        # Nom du fichier avec horodatage
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{switch['name']}_{date_str}.cfg"
        local_path = os.path.join(local_temp_dir, filename)

        # Sauvegarde locale temporaire
        with open(local_path, "w") as f:
            f.write(running_config)
        print(f"[INFO] Configuration récupérée pour {switch['name']} -> {local_path}")

        # Envoi sur le serveur FTP
        print(f"[INFO] Envoi de {filename} sur FTP {ftp_host}...")
        ftp = FTP(ftp_host)
        ftp.login(ftp_user, ftp_pass)

        # Aller dans le dossier racine des configs
        ftp_ensure_dir(ftp, ftp_folder)

        # Créer un dossier propre à ce switch
        ftp_ensure_dir(ftp, switch["name"])

        # Envoyer le fichier
        with open(local_path, "rb") as f:
            ftp.storbinary(f"STOR {filename}", f)

        ftp.quit()
        print(f"[INFO] Sauvegarde de {switch['name']} terminée dans /{ftp_folder}/{switch['name']}/\n")

    except Exception as e:
        print(f"[ERROR] Impossible de sauvegarder {switch['name']} : {e}")

# ---------------- EXECUTION ----------------

if __name__ == "__main__":
    for sw in switches:
        backup_switch(sw)
