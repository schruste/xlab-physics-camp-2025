import sys
import urllib.request
import json

url = sys.argv[1]
urllib.request.urlretrieve(url, 'ngsolve.json')

ngs = json.load(open('ngsolve.json'))['packages']
ori = json.load(open(sys.argv[2]))
pkg = ori['packages']
ori['info']['version'] = "0.24.0a1"

del pkg['micropip']
for name in pkg:
    p = pkg[name]
    if not p['file_name'].startswith('https://'):
        p['file_name'] = "https://cdn.jsdelivr.net/pyodide/dev/full/"+p['file_name']
    pkg[name] = p
for name in ngs:
    if name not in pkg:
        p = ngs[name]
        if p['file_name'].startswith('https://ngsolve'):
            continue
        if not p['file_name'].startswith('https://'):
            url = "https://ngsolve.org/ngslite/static/pyodide/"+p['file_name']
            print("download", url)
            urllib.request.urlretrieve(url, f'pyodide/{p["file_name"]}')
        pkg[name] = p

json.dump(ori, open(sys.argv[2], 'w'), indent=2)


