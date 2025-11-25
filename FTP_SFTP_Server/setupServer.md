# Installation d'un serveur FTP puis migration vers SFTP pour sauvegarde Cisco

## 1. Installer vsftpd (Serveur FTP)

``` bash
sudo apt update
sudo apt install vsftpd -y
```

Vérification :

``` bash
vsftpd -version
```

Activer et démarrer :

``` bash
sudo systemctl enable vsftpd
sudo systemctl start vsftpd
sudo systemctl status vsftpd
```

## 2. Créer l'utilisateur FTP dédié

``` bash
sudo useradd -d /srv/ftpbackup -m sauvegarde
sudo passwd sauvegarde   # Exemple : sauvegarde
```

## 3. Créer le dossier de sauvegarde

``` bash
sudo mkdir -p /srv/ftpbackup/configs
sudo chown sauvegarde:sauvegarde /srv/ftpbackup/configs
sudo chmod 750 /srv/ftpbackup/configs
```

Vérification :

``` bash
ls -ld /srv/ftpbackup/configs
```

## 4. Configurer vsftpd

Éditer le fichier :

``` bash
sudo nano /etc/vsftpd.conf
```

Ajouter / modifier :

    local_enable=YES
    write_enable=YES
    chroot_local_user=YES
    allow_writeable_chroot=YES
    anonymous_enable=NO
    xferlog_enable=YES
    xferlog_file=/var/log/vsftpd.log
    pasv_min_port=30000
    pasv_max_port=31000

Redémarrer :

``` bash
sudo systemctl restart vsftpd
```

## 5. Configurer le firewall

``` bash
sudo ufw allow 21/tcp
sudo ufw allow 30000:31000/tcp
sudo ufw reload
```

## 6. Test FTP depuis un PC

``` text
ftp 192.168.100.36
Username: sauvegarde
Password: sauvegarde
cd configs
put test.cfg
```

## 7. Copier la configuration depuis un switch Cisco (FTP)

Depuis le switch :

``` text
Switch# copy running-config ftp:
Address or name of remote host []? 192.168.100.36
Destination filename [switch-confg]? configs/switch1.cfg
Username: sauvegarde
Password: sauvegarde
```

Vérifier côté serveur :

``` bash
ls -l /srv/ftpbackup/configs
```

## 8. Passer de FTP à SFTP (Sécurisé)

FTP est non chiffré, SFTP utilise SSH et chiffre toutes les
communications.

### 8.1. Créer un environnement sécurisé SFTP

``` bash
sudo mkdir -p /backups/configs
sudo chown root:root /backups
sudo chmod 755 /backups
sudo chown sauvegarde:sauvegarde /backups/configs
```

### 8.2. Configurer SSH pour activer SFTP chrooté

``` bash
sudo nano /etc/ssh/sshd_config
```

Ajouter :

    Subsystem sftp internal-sftp

    Match User sauvegarde
        ChrootDirectory /backups
        ForceCommand internal-sftp
        AllowTcpForwarding no
        X11Forwarding no

Redémarrer :

``` bash
sudo systemctl restart sshd
```

### 8.3. Désactiver l'accès shell

``` bash
sudo usermod -s /usr/sbin/nologin sauvegarde
```

### 8.4. Tester SFTP

``` bash
sftp sauvegarde@localhost
```

## 9. Copier la configuration Cisco via SFTP

``` text
Switch# copy running-config sftp:
Address or name of remote host []? 192.168.100.36
Destination filename [switch-confg]? configs/switch1.cfg
Username: sauvegarde
Password: ********
```
