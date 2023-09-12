export PYODIDE_VERSION=0.23.4
rm -rf *.tar.bz2 pyodide
wget https://github.com/pyodide/pyodide/releases/download/${PYODIDE_VERSION}/pyodide-core-${PYODIDE_VERSION}.tar.bz2
tar xvf pyodide-core-${PYODIDE_VERSION}.tar.bz2

cp .github/workflows/generate_repodata.js pyodide/
node pyodide/generate_repodata.js
rm pyodide/*.whl
python .github/workflows/merge.py

rm -f pyodide.tar.bz2
tar -cvjSf pyodide.tar.bz2 pyodide
