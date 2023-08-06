1. Get all machines running NFS in a CIDR range:
```bash
nmap -p 111 --script=rpcinfo <Target CIDR> -oG rpc-machines.txt
```
2. Wittle rpc-machines.txt down to just those running NFS
3. Enumerate the NFS services floating about:
```bash
nmap -p 111 --script nfs* -iL nfs-machines.txt
```
