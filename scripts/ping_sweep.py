#!/usr/bin/env python3
import sys
from subprocess import run
from multiprocessing import Process as proc

def ping(target_ip):
	if run(['ping','-c','1',target_ip], capture_output=True).returncode==0:
		print(target_ip)

if len(sys.argv) != 2:
	print('Usage: ./ping_sweep.py <first 3 octets to scan>')
	print('eg. ./ping_sweep.py 10.11.1')
else:
	fto = sys.argv[1] + '.' # First three octets
	print("Received responses from:")
	[proc(target=ping, args=(fto + str(i),)).start() for i in range(1,255)]
