#!/bin/bash

input="./mount_pcs.config"
while IFS= read -r line
do
  sudo mkdir /mnt/"$line"
  sudo echo "//$line/C$ /mnt/$line/ cifs credentials=/home/$SUDO_USER/.smbcredentials,vers=1.0,iocharset=utf8,sec=ntlm 0 0" >> /etc/fstab
done < "$input"

sudo mount -a
