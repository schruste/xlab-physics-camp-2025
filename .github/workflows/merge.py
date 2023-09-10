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

pkg.update({
    "ipykernel": {
      "name": "ipykernel",
      "version": "6.9.2",
      "file_name": "../../extensions/@jupyterlite/pyodide-kernel-extension/static/pypi/./ipykernel-6.9.2-py3-none-any.whl",
      "install_dir": "site",
      "sha256": "3024d4ac0f91cb909d0d74e8be144ab2edf2c8b3a8c46df68c3efd910b15699f",
      "imports": [],
      "depends": []
    },
    "piplite": {
      "name": "piplite",
      "version": "0.1.1",
      "file_name": "../../extensions/@jupyterlite/pyodide-kernel-extension/static/pypi/piplite-0.1.1-py3-none-any.whl",
      "install_dir": "site",
      "sha256": "95ec2f128ad4e1c7d8bde13bb5261b669c72746094e128297c478e75adf24b5e",
      "imports": [],
      "depends": []
    },
    "pyodide-kernel": {
      "name": "pyodide-kernel",
      "version": "0.1.1",
      "file_name": "../../extensions/@jupyterlite/pyodide-kernel-extension/static/pypi/./pyodide_kernel-0.1.1-py3-none-any.whl",
      "install_dir": "site",
      "sha256": "cf50220493bf2bd6f1dfc5f0c10c64476c5c5fb93c5bab154fac0fe5f47f968a",
      "imports": [],
      "depends": []
    },
    "widgetsnbextension": {
      "name": "widgetsnbextension",
      "version": "4.0.7",
      "file_name": "../../extensions/@jupyterlite/pyodide-kernel-extension/static/pypi/./widgetsnbextension-4.0.7-py3-none-any.whl",
      "install_dir": "site",
      "sha256": "5fd374049672a5350eb999956f3051dde5523983f8a611b11a6ffabc32a794df",
      "imports": [],
      "depends": []
    }
})

json.dump(ori, open(sys.argv[2], 'w'), indent=2)


