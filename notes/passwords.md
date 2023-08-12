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

### Hashcat
Standard `hashcat` usage:
```bash
hashcat crackable.txt /usr/share/wordlists/rockyou.txt
```
For debugging a new rule:
```bash
head /usr/share/wordlists/rockyou.txt > demo.txt
hashcat -r newrule.rule --stdout demo.txt
```
See https://hashcat.net/wiki/doku.php?id=rule_based_attack for docs on the syntax for rules based attacks. Spaces separate discrete instructions to apply to one word. Newlines define a new pattern to attempt. Save it in a `.rules` file.
```bash
hashcat -m <insert hashing algo id here (0 for md5)> crackme.txt /usr/share/wordlists/rockyou.txt -r nonsense.rule --force
```

All of the above is kinda cringe though. Just make use of a rulefile thats been crafted for us:
```bash
hashcat -m 0 crackable.txt /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/rockyou-30000.rule --force
```


### Hashid
Hashcat seems to kinda suck at identifying the hash in use for some reason. Fortunately `hashid` doesn't. Nb. take care to use quotes, particularly if your hash starts with a `$` or other syntactically important character.
```bash
hashid "$2y$10$XrrpX8RD6IFvBwtzPuTlcOqJ8kO2px2xsh17f60GZsBKLeszsQTBC"
```

### keepass2john
```bash
keepass2john allTehS3cre75.kdbx > keepass.hash
```
Be sure to drop the username and colon that is prepended to `keepass.hash`. Hashcat will parse it as a salt and get sad otherwise.
```bash
hashcat -h | grep KeePass | awk -F ' ' '{print $1}' 
hashcat -m <output of the above> keepass.hash /usr/share/wordlists/rockyou.txt -r /usr/share/hashcat/rules/rockyou-30000.rule --force
```

### JohnTheRipper
In the event that Hashcat isn't working for whatever reason, consider making use of John:
```bash
john --wordlist=<password list> --rules=<rule Name> <our Hash>
```
Nb. with rules passed to John we can use the same syntax as with Hashcat, however we must prepend the file with:
```
[List.Rules:<rule Name>]
```
and we must be sure to add the rule file to the John config:
```bash
sudo sh -c 'cat /home/kali/Downloads/ssh.rule >> /etc/john/john.conf'
```

If we have an `id_rsa` file that we've managed to dump via some means (eg. path traversal in an http server) the we must first make it digestible for John:
```bash
ssh2john id_rsa > ssh.hash
```
nb. if we want to later log in to the SSH server using the credentials we've just recovered we may need to go ahead and `chmod` the private key file. Try both 600 and 400.