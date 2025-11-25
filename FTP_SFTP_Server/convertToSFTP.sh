#!/bin/bash
set -e

echo "[INFO] Préparation de l'environnement SFTP..."

echo "[INFO] Création du dossier de backups si nécessaire..."
mkdir -p /home/sauvegarde/configs

echo "[INFO] Permissions strictes pour le chroot..."
chown root:root /home/sauvegarde
chmod 755 /home/sauvegarde

echo "[INFO] Permissions pour le dossier configs..."
chown sauvegarde:sauvegarde /home/sauvegarde/configs
chmod 755 /home/sauvegarde/configs

echo "[INFO] Suppression des fichiers shell inutiles..."
rm -f /home/sauvegarde/.bashrc
rm -f /home/sauvegarde/.profile
rm -f /home/sauvegarde/.bash_profile

echo "[INFO] Désactivation du shell pour l'utilisateur..."
usermod -s /usr/sbin/nologin sauvegarde

echo "[INFO] Configuration SSH..."
sed -i '/Subsystem sftp/d' /etc/ssh/sshd_config

cat >> /etc/ssh/sshd_config <<EOF
Subsystem sftp internal-sftp

Match User sauvegarde
    ChrootDirectory /home/sauvegarde
    ForceCommand internal-sftp
    AllowTcpForwarding no
    X11Forwarding no
EOF

echo "[INFO] Redémarrage du service SSH..."
systemctl restart ssh

echo "=========================================================="
echo "La conversion FTP → SFTP est terminée !"
echo "Connectez-vous avec :"
echo "   sftp sauvegarde@IP"
echo "Dossier utilisable : /configs"
echo "=========================================================="
