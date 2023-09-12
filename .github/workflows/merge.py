import json
import os

pyodide_version = os.environ['PYODIDE_VERSION']

repo_file = 'pyodide/repodata.json'
ori = json.load(open(repo_file))
pkg = ori['packages']

for name in pkg:
    p = pkg[name]
    if not p['file_name'].startswith('https://') and not os.path.exists(os.path.join('pyodide', p['file_name'])):
        p['file_name'] = f"https://cdn.jsdelivr.net/pyodide/v{pyodide_version}/full/"+p['file_name']
    pkg[name] = p

pkg['webgui-jupyter-widgets']['depends'].append('numpy')
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
    },
    "netgen": {
      "name": "netgen",
      "version": "6.2.2304",
      "file_name": "netgen.zip",
      "install_dir": "stdlib",
      "sha256": "cf1656caff13c5f06926efd39cd8bd5d5aa99b457e014df5b9990adc9d4ec07c",
      "package_type": "cpython_module",
      "imports": [
        "netgen"
      ],
      "depends": [
        "pyngcore",
        "webgui-jupyter-widgets"
      ],
      "unvendored_tests": False,
      "shared_library": True
    },
    "ngsolve": {
      "name": "ngsolve",
      "version": "6.2.2304",
      "file_name": "ngsolve.zip",
      "install_dir": "stdlib",
      "sha256": "4ea7339029648daff408a46bcb031355974fc759b0f108ce0525d91f4247edf2",
      "package_type": "cpython_module",
      "imports": [
        "ngsolve"
      ],
      "depends": [
        "openblas",
        "numpy",
        "netgen"
      ],
      "unvendored_tests": False,
      "shared_library": True
    },
    "pyngcore": {
      "name": "pyngcore",
      "version": "0.0.1",
      "file_name": "pyngcore.zip",
      "install_dir": "stdlib",
      "sha256": "afb15ca2d1b03925e7d77d798e06a325a06bca22b36e63219b4fba4d11dad05d",
      "package_type": "cpython_module",
      "imports": [
        "pyngcore"
      ],
      "depends": [],
      "unvendored_tests": False,
      "shared_library": True
    }
})

json.dump(ori, open(repo_file, "w"), indent=2)
