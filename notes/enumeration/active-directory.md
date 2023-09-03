## Active Directory

### Manual Enumeration

Login as a user on a domain:
```bash
xfreerdp /u:ggilligan12 /d:vulnerable.corp /v:192.168.12.34
```
Get users on the domain:
```cmd
net user /domain
```
Enumerate particular domain user:
```cmd
net user ggilligan12 /domain
```
Enumerate groups on the domain:
```cmd
net group /domain
```
Enumerate particular domain group:
```cmd
net group "uberPwnage" /domain
```
Get the Primary Domain Controller:
```powershell
[System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
```



### Automatic Enumeration