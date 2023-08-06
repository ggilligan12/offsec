SMB OS Enumeration:
`nmap -v -p 139, 445 --script=smb-os-discovery <Target IP address>`

SMB Share Enumeration (from Powershell):
`net view \\<computer name> /all`

SMB Enumeration (from Linux):
`enum4linux <Target IP address>`

Get SMB Share:
`smbclient -L <Target IP address>`

More available from: `impacket-smbserver`
