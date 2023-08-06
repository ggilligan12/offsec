### whois

Forwards whois enumeration:
```bash
whois <hostname> -h <IP address some host we wanna direct the whois lookup at>
```
Reverse lookup:
```bash
whois <host IP> -h <IP address some host we wanna direct the whois lookup at>
```

### Google Hacking

Google hacking for filetypes in subdirectories:
```
site:megacorpone.com filetype:txt
```
Google hacking excluding filetypes in subdirectories:
```
site:megacorpone.com -filetype:html
```
Full list of search operators:
https://ahrefs.com/blog/google-advanced-search-operators/

GHDB queries for easy search engine enumeration:
https://www.exploit-db.com/google-hacking-database

Dorksearch for faster Google hacking:
https://dorksearch.com/

Finding relevant exploits:
```bash
firefox --search "Microsoft Edge site:exploit-db.com"
```

### Misc

Site report and server history:
https://searchdns.netcraft.com

Secrets discovery in Git repos:
`Gitrob & Gitleaks`

Domain enumeration:
```
Shodan hostname:megacorpone.com
```

HTTP headers:
https://securityheaders.com/

SSL/TLS security:
https://www.ssllabs.com/ssltest/

Dump file metadata:
```bash
exiftool -a -u <filename goes here>
```
