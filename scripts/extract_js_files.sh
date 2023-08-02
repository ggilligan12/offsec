#!/bin/bash
wget -q 'http://www.offensive-security.com/pwk-files/access_log.txt.gz'
gunzip access_log.txt.gz
grep -o '[^/]*\.js' access_log.txt | sort -u > js-files.txt
cat js-files.txt
rm access_log.txt js-files.txt
