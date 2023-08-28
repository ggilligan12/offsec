# Port Forwarding

## Socat Port Forwarding
Via `socat`:
```bash
socat -ddd TCP-LISTEN:<port to listen on>,fork TCP:<IP to forward to>:<port to forward to>
```
Remember it is useful to select a high port to listen on (>1000), since our choice of port there is arbitrary, but we cannot have ports below 1000, as we require admin privileges to bind to those!

## SSH Tunneling
Principle here is to establish a tunnel from machine 1 to machine 2, that subsequently forwards traffic onto machine 3

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
ssh -N -D 0.0.0.0:<port for machine 1 to listen on> user@<machine2 IP>
```
We omit any information about `machine3` here, since we'll handle that when we come to use the tunnel. We now make use of `Proxychains`. Before we make a connection attempt we need to replace any existing proxy information in `/etc/proxychains4.conf` with the following config info about `machine1`:
```
socks5 <machine1 IP> <port for machine 1 to listen on>
```
Now `machine3` is effectively reachable from our Kali host, we just need to prepend `proxychains` to the command that we'd like to run through the tunnel. Eg.
```bash
proxychains nmap -sV -sT -A <machine3 IP>
```