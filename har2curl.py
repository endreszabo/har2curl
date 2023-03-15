#!/usr/bin/env python

from json import load
from sys import stdin, stderr

def escape(s):
    return "'"+s.replace("'", "'\\''")+"'"

def log_entry_to_curl(e):
    rv = []
    rv += ['--request', e['request']['method']]
    for header in e['request']['headers']:
        if header['name'] != 'Cookie':
            rv += ['--header', escape("%s: %s" % (header['name'], header['value']))]
        else:
            rv += ['--cookie', escape(header['value'])]
    rv += [escape(e['request']['url'])]
    if e['request']['bodySize'] > 0:
        if e['request']['postData']['mimeType'] == 'application/x-www-form-urlencoded':
            for param in e['request']['postData']['params']:
                rv += ['--data-urlencode', "%s=%s" % (escape(param['name']), escape(param['value']))]
    return rv

h = load(stdin)

for entry in h['log']['entries']:
    print(f"# {entry['pageref']} at {entry['startedDateTime']}: {entry['request']['url']}", file=stderr)
    print("curl", " ".join(log_entry_to_curl(entry)))

