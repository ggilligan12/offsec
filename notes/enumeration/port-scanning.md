
### Simple TCP scan:
1 second timeout (`-z` gives us zero I/O mode for scanning)
```bash
nc -nvv -w 1 -z 192.168.xx.xx <Port range>
```

### Simple UDP scan:
1 second timeout
```bash
nc -nv -u -z -w 1 192.168.xx.xx <Port range>
```

### SYN Stealth Scan:
```bash
sudo nmap -sS 192.168.xx.xx
```

### TCP Connect Scan:
```bash
nmap -sT 192.168.xx.xx
```

### UDP Scan:
```bash
sudo nmap -sU 192.168.xx.xx
```

### Network Sweep:
This sends out an ICMP ping, a TCP `SYN` packet to port `443`, a TCP `ACK` packet to port `80`, and an ICMP timestamp request. This is thanks to the `-sn` flag, which disables general port scanning in favour of a focused ping sweep.
```bash
nmap -sn 192.168.xx.xx-<no. of addresses youd like to sweep over>
```

### Top targets scan:
The `-A` option gives us a traceroute, and the `-oG` option gives us our output in a greppable text file.
```bash
nmap -sT -A --top-ports=4260 192.168.xx.xx-<no. of addresses to sweep> -oG <greppable results filename>.txt
```

### The 'Fuck It We Ball' Scan
```bash
nmap -p- 192.168.xx.xx
```

### OS Fingerprinting:
Reliable, but not a definitive tool, can be mistaken, more comprehensive enumeration required to verify the target OS.
```bash
sudo nmap -O 192.168.xx.xx
```

### Service Enumeration:
The `-sV` flag help look for service 'banners'. Nb. These can be changed by the machines owner and can therefore be used to mislead. Useful, but not to be trusted implicitly.
```bash
nmap -sV -sT -A 192.168.xx.xx
```

### NSE (nmap Scripting Engine):
Repository of scripts that come for free with nmap saved down to `/usr/share/nmap/scripts`.
Quite a few of these scripts appear to be straight up exploits targeting particular CVE's
To run a script:
```bash
nmap 192.168.xx.xx --script=<Script name>
```
To access that scripts man page:
```bash
nmap --script-help <Script name>
```
Useful scripts:
- `smb-os-discovery`
- `dns-zone-transfer`
- `http-headers`
- `http-title`
- `vuln`
Nmap can be used as an effective vuln scanner (that we're allowed to use!!)
```bash
sudo nmap -sV -p 443 --script "vuln" <Target IP>
```
More to be found at: `/usr/share/nmap/scripts`

### NetBIOS Scan:
This will perform a NetBIOS name scan, since the `-r` flag specifies the origin port must be `137`, the one used for querying the NetBIOS name service.
```bash
sudo nbtscan -r <Target CIDR>
```

### Powershell Port Scanning:
Sometimes we have to be scrubs and work from within Windows machines, in such scenarios we must make do with CMD and Powershell. To hit one port:
```powershell
Test-NetConnection -Port 445 192.168.50.151
```
To do a sweep of TCP ports:
```powershell
1..1024 | % {echo ((New-Object Net.Sockets.TcpClient).Connect("<Target IP>", $_)) "TCP port $_ is open"} 2>$null
```
To sweep a particular port on a subnet where you don't know the IPs:
```powershell
1..255 | % {echo $_; echo ((New-Object Net.Sockets.TcpClient).Connect("172.16.70.$_", 80)) "TCP port 80 is open on 172.16.70.$_"} 2>$null
```