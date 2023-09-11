wget https://github.com/pyodide/pyodide/releases/download/0.24.0a1/pyodide-0.24.0a1.tar.bz2
tar xvf pyodide-0.24.0a1.tar.bz2
cd pyodide && rm -f astropy-* Fiona-* bokeh-* gensim-* mypy-* opencv_python-* pandas-* scikit-* scikit_image-* scikit_learn-* sympy-* test-* yt-* && cd ..
#mv pyodide/pyodide-lock.json pyodide/pyodide-lock.json.bak
#wget https://cdn.jsdelivr.net/pyodide/dev/full/pyodide-lock.json -O pyodide/pyodide-lock.json
python .github/workflows/merge.py https://ngsolve.org/ngslite/static/pyodide/pyodide-lock.json pyodide/pyodide-lock.json
rm -f pyodide.tar.bz2
tar -cvjSf pyodide.tar.bz2 pyodide
