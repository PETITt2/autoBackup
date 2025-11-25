# Explication du fonctionnement des scripts de Sauvegarde Cisco (FTP et SFTP)

Ce document explique le fonctionnement des deux scripts que nous avons créés pour sauvegarder les configurations Cisco sur un serveur Linux, en utilisant **FTP** ou **SFTP**.

---

## Pré-requis

- Serveur Linux avec Python 3 installé.
- Bibliothèque Netmiko (`python3-netmiko`) pour la connexion SSH aux switches.
- Bibliothèque Paramiko (`paramiko`) pour la connexion SFTP.
- Accès SSH aux switches avec un utilisateur disposant de privilège 15.
- Serveur FTP ou SFTP opérationnel avec un utilisateur dédié pour la sauvegarde.

---

## Fonctionnement général des scripts

### 1. Connexion aux switches via SSH
- Le script utilise Netmiko pour établir une connexion SSH avec chaque switch listé dans la configuration.

### 2. Mode enable
- Si nécessaire, le script passe en mode privilégié (enable) en utilisant le mot de passe configuré sur le switch.

### 3. Récupération de la configuration
- Exécution de la commande `show startup-config` pour récupérer la configuration active du switch.

### 4. Sauvegarde locale temporaire
- La configuration est enregistrée dans un fichier local temporaire (`/tmp/switch_backup`).
- Le nom du fichier contient le nom du switch et un horodatage pour créer un historique.

### 5. Transfert vers le serveur
- **Script FTP** :
  - Connexion au serveur FTP avec l’utilisateur dédié.
  - Création du dossier correspondant au switch si nécessaire.
  - Transfert du fichier de configuration vers le dossier FTP configuré.
- **Script SFTP** :
  - Connexion au serveur SFTP avec Paramiko.
  - Création du dossier correspondant au switch sur le serveur SFTP si nécessaire.
  - Transfert du fichier de configuration via SFTP.

### 6. Déconnexion
- Une fois le transfert terminé, le script déconnecte le switch et passe au suivant.
- La connexion au serveur FTP ou SFTP est fermée.

---

## Structure de configuration du script

### Switches
Liste des switches avec les informations suivantes pour chaque switch :

- `host` : adresse IP du switch
- `username` : nom d’utilisateur SSH
- `password` : mot de passe SSH
- `secret` : mot de passe enable
- `name` : nom du switch utilisé pour nommer les fichiers

### Serveur FTP ou SFTP
- `ftp_host` / `sftp_host` : adresse IP ou hostname du serveur
- `ftp_user` / `sftp_user` : utilisateur
- `ftp_pass` / `sftp_pass` : mot de passe
- `ftp_folder` / `sftp_root` : dossier sur le serveur où déposer les fichiers

### Dossier temporaire local
- `local_temp_dir` : chemin local où les fichiers sont stockés temporairement avant envoi.

---

## Exécution

Pour lancer le script manuellement :

### FTP
```bash
python3 /chemin/vers/backup_switches_ftp.py
```

### SFTP
```bash
python3 /chemin/vers/backup_switches_sftp.py
```

---

## Points importants

- Les scripts nécessitent que SSH soit activé sur les switches et que l’utilisateur ait les droits nécessaires.
- Les fichiers sont horodatés pour conserver un historique et éviter d’écraser les sauvegardes précédentes.
- Chaque switch a son propre dossier sur le serveur pour organiser les backups.
- Le script SFTP est plus sécurisé car toutes les communications sont chiffrées.

---

## Conclusion

Ces scripts automatisent complètement la récupération et le stockage des configurations Cisco, avec une **version FTP** simple et une **version SFTP** sécurisée. Ils sont adaptés pour être intégrés à une tâche cron pour des sauvegardes régulières.
