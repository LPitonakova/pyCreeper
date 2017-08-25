
INSTALLING DEPENDENCIES
======================================


Make sure you have Python 3.4 installed, along with matplotlib, scipy and numpy. E.g., if you are using macports:


sudo port install python34

sudo port install py34-numpy

sudo port install py34-scipy

sudo port install py34-matplotlib


INCLUDING pyCreeper IN YOUR PROJECT
======================================

Include the following directory in your interpreter path:

/DIRECTORY_WHERE_DOWNLOADED/pyCreeper-master/python



You can then use pyCreeper in your code as

import pyCreeper

pyCreeper.crGraphs.createLinePlot(myData)


VIEWING ONLINE DOCUMENTATION
======================================

The project's documentation can be found on
http://pycreeper.lenkaspace.net/




BUILDING DOCUMENTATION
======================================

Documentation can be built using sphinx.

1. Make sure you have sphinx for Python 3.4 installed.
------------------------------------------------------

E.g., if you are using macports:

sudo port install py34-sphinx

sudo port select --set sphinx py34-sphinx



Other examples on http://www.sphinx-doc.org/en/1.4.8/install.html


2. Install the rtd theme via:
------------------------------------------------------

sudo port install py34-sphinx_rtd_theme



(Make sure to install the 0.2.4 version if using the theme with Python 3.4!)


3. Build
------------------------------------------------------

To build, remain in the root directory of this folder and type

make doc


4. View
------------------------------------------------------
To view the documentation, go to doc/build/html/index.html