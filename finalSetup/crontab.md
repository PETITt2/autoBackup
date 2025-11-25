# Utilisation de Cron et Crontab pour Automatisation de Scripts


## 1. Qu'est-ce que Cron et Crontab ?
- **Cron** : service Linux qui exécute automatiquement des commandes ou scripts à des intervalles planifiés.

- **Crontab** : fichier de configuration ou commande pour gérer les tâches planifiées pour un utilisateur donné.

## 2. Éditer la crontab
Pour configurer les tâches d'un utilisateur :
```bash
crontab -e
```
- Choisir un éditeur si demandé (nano recommandé).
- Chaque utilisateur a sa propre crontab.

## 3. Syntaxe des lignes dans crontab
```
* * * * * commande
┬ ┬ ┬ ┬ ┬
│ │ │ │ │
│ │ │ │ └─ Jour de la semaine (0-7, 0 et 7 = dimanche)
│ │ │ └── Mois (1-12)
│ │ └─── Jour du mois (1-31)
│ └──── Heure (0-23)
└───── Minute (0-59)
```

### Exemples
- Exécuter un script tous les jours à 2h00 :
```bash
0 2 * * * /usr/bin/python3 /chemin/vers/script.py
```
- Exécuter un script tous les jours à 15h15 :
```bash
15 15 * * * /usr/bin/python3 /chemin/vers/backup_switches_ftp.py >> /var/log/switch_backup.log 2>&1
```

Explications :
- `/usr/bin/python3` : chemin vers l'exécutable Python.
- `/chemin/vers/backup_switches_ftp.py` : chemin complet vers le script Python.
- `>> /var/log/switch_backup.log 2>&1` : redirige la sortie standard et les erreurs vers un fichier de log pour suivi.

## 4. Vérifier les tâches planifiées
```bash
crontab -l
```
- Affiche toutes les tâches planifiées pour l'utilisateur.

## 5. Tester la crontab
- Modifier temporairement l'heure de la tâche pour une minute proche afin de tester l'exécution.
- Vérifier le fichier de log avec :
```bash
tail -f /var/log/switch_backup.log
```
- Permet de confirmer que le script s'exécute correctement via cron.

## 6. Conseils
- Utiliser des chemins absolus pour les scripts et fichiers.
- Utiliser un utilisateur dédié si possible pour éviter les conflits avec d'autres tâches du système.
- Ajouter des horodatages dans le log pour suivre les exécutions sur le long terme deja integré dans le script.