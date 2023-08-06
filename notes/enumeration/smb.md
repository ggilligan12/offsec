### SMB OS Enumeration
```bash
nmap -v -p 139, 445 --script=smb-os-discovery <Target IP address>
```

### SMB Share Enumeration (from Powershell):
```bash
net view \\<computer name> /all
```

### SMB Enumeration (from Linux):
```bash
enum4linux <Target IP address>
```

### Get SMB Share:
```bash
smbclient -L <Target IP address>
```

More available from: `impacket-smbserver`
