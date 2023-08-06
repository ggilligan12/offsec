### SMB OS Enumeration

```bash
nmap -v -p 139, 445 --script=smb-os-discovery <Target IP address>
```

```bash
SMB Share Enumeration (from Powershell):
net view \\<computer name> /all
```

```bash
SMB Enumeration (from Linux):
enum4linux <Target IP address>
```

```bash
Get SMB Share:
smbclient -L <Target IP address>
```

More available from: `impacket-smbserver`
