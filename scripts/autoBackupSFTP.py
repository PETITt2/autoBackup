#!/usr/bin/env python3
"""
Script de sauvegarde automatique des configs Cisco sur un serveur SFTP.
"""

from netmiko import ConnectHandler
import paramiko
from datetime import datetime
import os

# ---------------- CONFIGURATION ----------------

switches = [
    {
        "host": "192.168.100.38",
        "username": "admin",
        "password": "admin",
        "secret": "admin",
        "name": "switch1"
    }
]

# SFTP
sftp_host = "192.168.100.36"
sftp_user = "sauvegarde"
sftp_pass = "sauvegarde"
sftp_root = "configs"  # dossier racine sur le serveur SFTP

# Dossier temporaire local
local_temp_dir = "/tmp/switch_backup"
os.makedirs(local_temp_dir, exist_ok=True)

# ---------------- FONCTIONS ----------------

def sftp_ensure_dir(sftp, path):
    """Crée un dossier sur le serveur SFTP s'il n'existe pas"""
    try:
        sftp.chdir(path)
    except IOError:
        # Dossier inexistant : on le crée
        sftp.mkdir(path)
        sftp.chdir(path)

def backup_switch(switch):
    """Se connecte au switch, récupère la config et l'envoie sur le serveur SFTP"""
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

        # Connexion SFTP
        transport = paramiko.Transport((sftp_host, 22))
        transport.connect(username=sftp_user, password=sftp_pass)
        sftp = paramiko.SFTPClient.from_transport(transport)

        # Aller dans le dossier racine des configs
        sftp_ensure_dir(sftp, sftp_root)

        # Créer un dossier spécifique à ce switch
        sftp_ensure_dir(sftp, switch["name"])

        # Envoi du fichier
        remote_path = f"{sftp_root}/{switch['name']}/{filename}"
        sftp.put(local_path, remote_path)
        print(f"[INFO] Sauvegarde de {switch['name']} terminée -> /{remote_path}")

        sftp.close()
        transport.close()

    except Exception as e:
        print(f"[ERROR] Impossible de sauvegarder {switch['name']} : {e}")

# ---------------- EXECUTION ----------------

if __name__ == "__main__":
    for sw in switches:
        backup_switch(sw)
