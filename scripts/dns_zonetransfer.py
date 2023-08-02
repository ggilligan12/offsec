#!/usr/bin/env python3
import sys, dns.query, dns.resolver, dns.zone

'''
This script is ridiculously verbose, but I like it that way.
It's extremely clear what's going on, and because these functions
are so atomic some are potentially reusable for other bits and bobs!
'''

# Check for and get mandatory zone argument
def getZoneName():
    if len(sys.argv) != 2:
        print('Usage: ./dns_zoneXfer.py <target domain>')
        print('eg. ./dns_zoneXfer.py megacorpone.com')      
        sys.exit(1)
    else:
        return sys.argv[1]

# Get the DNS Name Servers assocaited with this domain.
def getNameServers(domain):
    return dns.resolver.resolve(domain,'NS')

# Get the IP address the given domain name resolves to.
def resolveIPFromServer(server):
    return dns.resolver.resolve(str(server),'A')[0].address

# Get a list of (Name Server Domain, Ip Address) pairings.
def getDomainsAndIPs(domain):
    return [[ns,resolveIPFromServer(ns)] for ns in getNameServers(domain)]

# Attempt a zone transfer for the given server and domain.
def try_xfr(address, server, domain):
    print(f'\nAttempting transfer for {server}')
    z = dns.zone.from_xfr(dns.query.xfr(address, domain))
    for n in sorted(z.nodes.keys()):
        line = z[n].to_text(n)
        if line[0]=='@':
            print(line)
        else:
            line = line.split()
            print(f'{line[0]}.{domain} has address: {line[-1]}')

def attempt_zone_transfer(zone):
    DomainsAndIPs = getDomainsAndIPs(zone)
    for server,ip in DomainsAndIPs:
        try:
            try_xfr(ip, server, zone)
        except dns.xfr.TransferError as e:
            print(e)

zone = getZoneName()
attempt_zone_transfer(zone)

