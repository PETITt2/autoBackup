# Sauvegarde des configurations des switches et routeurs

**Contexte :**  
Pour enregistrer les configurations dans un réseau, le projet consiste à mettre en place un système de sauvegarde automatisé.

---

## Objectifs

1. Mettre en place un serveur FTP/SFTP sécurisé (par exemple sur Proxmox).  
2. Créer une VM dédiée pouvant accéder aux équipements réseau actifs (switches, routeurs) pour effectuer les sauvegardes et les restaurations.

---

## Contenu de ce repository

Ce repository détaille la mise en place et le fonctionnement d’un système de sauvegarde des configurations réseau, accessible via SSH.  
Tous les fichiers et leur rôle sont répertoriés ci-dessous.

| Description | Chemin |
|------------|--------|
| Création et configuration du serveur FTP/SFTP | **/FTP_SFTP_Server/setupServer.md** |
| Configuration des switches et routeurs pour récupérer les backups | **/Switch_Router/confExplained.md** |
| Explication des scripts de sauvegarde Python | **/scripts/scriptsExplained.md** |
