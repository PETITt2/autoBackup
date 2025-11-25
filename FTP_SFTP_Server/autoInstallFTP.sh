#!/bin/bash
set -e

echo "[INFO] Installation de vsftpd..."
apt update
apt install -y vsftpd

echo "[INFO] Activation du service..."
systemctl enable vsftpd
systemctl restart vsftpd

echo "[INFO] Création de l'utilisateur sauvegarde..."
# Home = /srv/ftpbackup
useradd -d /srv/ftpbackup -m sauvegarde || true
echo "sauvegarde:sauvegarde" | chpasswd

echo "[INFO] Création du dossier de sauvegarde..."
mkdir -p /srv/ftpbackup/configs
chown sauvegarde:sauvegarde /srv/ftpbackup/configs
chmod 750 /srv/ftpbackup/configs

echo "[INFO] Configuration de vsftpd..."
cat > /etc/vsftpd.conf <<EOF
local_enable=YES
write_enable=YES
chroot_local_user=YES
allow_writeable_chroot=YES
anonymous_enable=NO
xferlog_enable=YES
xferlog_file=/var/log/vsftpd.log
pasv_min_port=30000
pasv_max_port=31000
listen=YES
listen_ipv6=NO
EOF

echo "[INFO] Redémarrage FTP..."
systemctl restart vsftpd

echo "[INFO] Ouverture du firewall..."
ufw allow 21/tcp || true
ufw allow 30000:31000/tcp || true
ufw reload || true

echo "=========================================================="
echo "FTP installé et prêt !"
echo "Utilisateur  : sauvegarde"
echo "Mot de passe : sauvegarde"
echo "Dossier      : /srv/ftpbackup/configs"
echo "=========================================================="
