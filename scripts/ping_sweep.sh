#!/bin/bash

# If the user doesn't pass exactly 1 argument tell em whats up
if [ "$#" -ne 1 ]; then
	echo 'Usage: ./ping_sweep.sh <first 3 octets to scan>'
	echo 'eg. ./ping_sweep.sh 10.11.1'
	exit
fi

pingRespondersFilename=ping_responders

# If this file is already kicking about then remove it
if [ -f $pingRespondersFilename ]; then
	rm $pingRespondersFilename
fi

# Iterate over every value the last octet can take
for ip in {1..254}
do
    # Ping the target in the background, filter for ones with a positive response, and append them to the responders file
    ping -c 1 $1.$ip | awk -v fto="$1" -v ip="$ip" '/transmitted/ { if ($4!=0) print fto "." ip; }' >> $pingRespondersFilename &
done

# Wait for the background ping jobs to finish
wait

# If we got any responses list them
if [ -s $pingRespondersFilename ]; then
	echo "Received responses from:"
	# Display the IPs we got a response from in order
	sort -V $pingRespondersFilename | cat
else
	echo "No responses received"
fi

# Clean up
rm $pingRespondersFilename
