## Linux Enumeration

### Manual Enumeration
File permissions
```bash
ls -l
```
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
List running processes:
```bash
ps aux
```
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
Packages installed via `dpkg` (Debian package manager):
```bash
dpkg -l
```
Find every directory the current user can write to:
```bash
find / -writable -type d 2>/dev/null
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
Find SUID marked binaries:
```bash
find / -perm -u=s -type f 2>/dev/null
```