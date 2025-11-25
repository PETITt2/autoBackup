# Configuration des Switchs et Routeurs Cisco pour Sauvegarde Automatique

## 1. Définir le hostname et le domaine
SSH nécessite un hostname et un domaine configuré.

```cisco
configure terminal
hostname Switch1        ! Nom du switch ou routeur
ip domain-name monreseau.local
exit
```

- `hostname` : nom de l'équipement.
- `ip domain-name` : requis pour la génération des clés RSA pour SSH.

## 2. Créer un utilisateur avec privilège 15
Cet utilisateur sera utilisé par le script Python pour se connecter et récupérer la configuration.

```cisco
configure terminal
username admin privilege 15 secret admin
exit
```

- `privilege 15` : accès complet aux commandes, y compris `show running-config`.
- `secret` : mot de passe crypté de l'utilisateur.

## 3. Définir un mot de passe enable
Nécessaire pour passer en mode privilégié si requis par le script.

```cisco
configure terminal
enable secret admin
exit
```

## 4. Générer les clés RSA pour SSH
```cisco
configure terminal
crypto key generate rsa modulus 2048
exit
```
- Taille 2048 bits recommandée.
- Obligatoire pour activer SSH.

## 5. Activer SSH sur les lignes VTY
```cisco
configure terminal
line vty 0 4
transport input ssh
login local
exit
```
- `login local` : utilise l'utilisateur local créé.
- `transport input ssh` : désactive Telnet et autorise uniquement SSH.

## 6. Configurer le NTP (optionnel)
Permet d'avoir des horodatages corrects pour les fichiers de sauvegarde.
```cisco
configure terminal
ntp server 192.168.100.1
exit
```

## 7. Vérifications
Après configuration, vérifier que tout est opérationnel :
```cisco
show running-config | include hostname
show running-config | include username
show running-config | include ssh
show ip interface brief
show ssh
```
- SSH doit être actif.
- L'utilisateur admin doit avoir les privilèges suffisants.
- Enable secret configuré.
- Interfaces IP correctes pour atteindre le serveur FTP.

## Points importants
- SSH activé pour le script Python.
- Utilisateur avec privilège 15 obligatoire pour exécuter `show running-config`.
- Enable secret configuré pour Netmiko.
- Domaine et clés RSA nécessaires pour SSH.
- NTP optionnel mais recommandé pour les horodatages.
---


