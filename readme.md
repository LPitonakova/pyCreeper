==================================================================================
INSTALLING DEPENDENCIES
==================================================================================

1. Python 3.4
------------------------------------------------------
Make sure you have Python 3.4 installed. E.g., if you are using macports:

sudo port install python34


2. Matplotlib toolkit
------------------------------------------------------
Install the python 3.4 matplot lib tool kit. E.g., if you are using macports:

sudo port install py34-matplotlib-basemap



==================================================================================
VIEWING ONLINE DOCUMENTATION
==================================================================================

The project's documentation can be found on
http://pycreeper.lenkaspace.net/


==================================================================================
BUILDING DOCUMENTATION
==================================================================================

Documentation can be built using sphinx.

1. Make sure you have sphinx for Python 3.4 installed.
------------------------------------------------------

E.g., if you are using macports:

sudo port install py34-sphinx
sudo port select --set sphinx py34-sphinx

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