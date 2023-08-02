#!/usr/bin/python3
import socket
import sys

if len(sys.argv) != 3:
	print("Usage: smtp_vrfy.py <username file> <target IP file>")
	sys.exit(0)

def testVFRY(username, ip):
	# Create a Socket
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to the Server
	connect = s.connect((ip,25))

	# Receive the banner
	banner = s.recv(1024)
	print(banner)

	# VRFY a user
	s.send('VRFY ' + username + '\r\n')
	result = s.recv(1024)

	# If the VRFY is successful the output is very brief,
	# and if not it is very verbose,
	# so we just need to check the output length.
	if len(result) < len(username) + 20:
		print(f'VERIFIED: {username}')

	# Close the socket
	s.close()

with open(sys.argv[1], 'r') as f:
	usernames = f.readlines()

with open(sys.argv[2], 'r') as f:
	IPs = f.readlines()

for ip in IPs:
	print(f"Running username list against: {ip}")
	for username in usernames:
		testVFRY(username, ip)
