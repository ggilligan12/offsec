### Enumerate Subdirectories:
Nb. These tools use wordlists and hammer the server. They won't find precise or obscurely named directories.
A sitemap might. Be sure to visit subdirs like `sitemap.xml` and `robots.txt`

The `-r` flag gives us non-recursive search, if we discover directories we can drill into those more manually. Less clumsy.
The `-z` flag allows us to specify a millisecond delay between queries to prevent us from knocking over the server.
```bash
dirb https://www.target-domain.com -r -z 10
```

Alternatively use gobuster, multi-threaded so more performant, but no recursive function (and can enumerate dirs given only an IP...).
```bash
gobuster dir -u <Target IP> -w /usr/share/wordlists/dirb/common.txt -t 5
```

gobuster can be a little smarter as well, if you know directories will follow a certain structure you can have it search by pattern:
```bash
echo "{GOBUSTER}/v1" > pattern
echo "{GOBUSTER}/v2" >> pattern
gobuster dir -u <Target IP> -w /usr/share/wordlists/dirb/common.txt -p pattern
```

### Enumerate HTTP Web Server:
```bash
sudo nmap -p80 --script=http-enum <Target IP>
```

### Website Tech Stack Enumeration:
https://wappalyzer.com
```bash
whatweb http://192.168.12.34
```

### Enumerating a Wordpress website:
```bash
wpscan --url <Target URL>
```

### Local Admin Consoles:
Unlikely to be exposed, but always worth checking:
- `/manager/html` (Tomcat)
- `/phpmyadmin` (phpMyAdmin)