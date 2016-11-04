
==================================================================================
==================== BUILDING DOCUMENTATION
==================================================================================

Documentation can be built using sphinx.

1. Make sure you have sphinx for Python 2.7 installed.
------------------------------------------------------

E.g., if you using macports:

sudo port install py27-sphinx
sudo port select --set sphinx py27-sphinx

Other examples on http://www.sphinx-doc.org/en/1.4.8/install.html


2. Install the rtd theme via:
------------------------------------------------------

pip install sphinx_rtd_theme


3. Build
------------------------------------------------------

To build, remain in the root directory of this folder and type

make doc


4. View
------------------------------------------------------
To view the documentation, go to doc/build/html/index.html