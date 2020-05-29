# Set up all windows pc mounts

import subprocess
import os

# fstab lines

with open('./mount_pcs.config') as config:
    for pc in config:
        pc = pc[:len(pc)-1]
        # Create pc mount point if needed
        if not os.path.isdir(f'/mnt/{pc}'):
            subprocess.check_call(['mkdir', f'/mnt/{pc}'])
        # Mount the pc
        os.system(f'smbmount //{pc}/C$ /mnt/{pc} -o credentials=/home/$SUDO_USER/.smbcredentials')
