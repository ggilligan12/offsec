#!/bin/bash

# Check if argument was given, if not, print usage
if [ -z "$1" ]; then
	echo "[*] Simple SMB vulnerability scanner"
	echo "[*] Usage: $0 <target IP addresses>.txt "
	exit 0
fi

# If argument was given, grab all the NSE scripts beginning with 'smb-vuln'
regex="/usr/share/nmap/scripts/smb-vuln*"
ls -1 $regex | awk -F "/" '{ print substr($6, 1, length($6)-4); }' > scripts.txt
for script in $(cat scripts.txt); do
	# For each of these scripts, run it against the target IPs
	echo "Assessing targets vulnerability with: $script"
done

# Tidying up
rm scripts.txt