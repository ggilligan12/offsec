#!/usr/bin/env python3
import requests, gzip, re, os
# Get and unzip the text file
url = 'http://www.offensive-security.com/pwk-files/access_log.txt.gz'
r = requests.get(url)
with open('access_log.txt.gz', 'wb') as f:
    f.write(r.content)
with gzip.open("access_log.txt.gz", 'rb') as f:
	content = f.read().decode('utf-8').split('\n')
# Iterate over it's content and run a regex to extract what we want
js_files = [re.findall('[^/]*\.js', l) for l in content if '.js ' in l]
# Flatten the 2d list, get the unique items, sort, and print them
for filename in sorted(list(set([f for sl in js_files for f in sl]))):
	print(filename)
# Tidy up
os.remove('access_log.txt.gz')