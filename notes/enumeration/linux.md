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