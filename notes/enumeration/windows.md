## Windows Enumeration
Having gained a foothold on a Windows machine by whatever mechanism the following items are important steps for us to gain situational awareness, with each item potentially proving critical to a successful effort at privilege escalation or lateral movement:

### Username and hostname
```cmd
whoami
```
### Group memberships of the current user
```cmd
whoami /groups
```
### Existing users and groups
```powershell
Get-LocalUser
Get-LocalGroup
Get-LocalGroupMember adminteam
Get-LocalGroupMember Administrators
```
### Operating system, version and architecture
```powershell
systeminfo
```
### Network information
To list all network interfaces:
```powershell
ipconfig /all
```
To display the routing table and potentially enumerate links to other systems or networks that haven't yet been enumerated:
```powershell
route print
```
To enumerate the active network connections on a Windows system (with no DNS resolution):
```powershell
netstat -ano
```
### Installed applications
To enumerate all 32 bit applications installed on the machine:
```powershell
Get-ItemProperty "HKLM:\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*" | select displayname
```
and for the 64 bit applications:
```powershell
Get-ItemProperty "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall\*" | select displayname
```
Nb. this is not necessarily a complete list, never forget to check the `C:\ProgramFiles*` directories, as well as the `C:\tools` and `Downloads` paths.
### Running processes
```powershell
Get-Process
```
