

.. image:: images/pyCreeperLogo.png
    :width: 220 px
    :align: left

############################
pyCreeper 1.1
############################

**Welcome! pyCreeper is a python library that lets you create pretty graphs in python with one-line function calls.**

The main purpose of pyCreeper is to wrap tens of lines of python code, required to produce graphs that look good for a publication, into functions. It takes away your need to understand various quirks of matplotlib and gives you back ready-to-use and well-documented code.

.. image:: images/download.png
    :width: 220 px
    :align: left
    :target: https://github.com/LPitonakova/pyCreeper/archive/master.zip

**You can also download or clone pyCreeper from GitHub:** `https://github.com/Elendurwen/pyCreeper <https://github.com/Elendurwen/pyCreeper>`_

|
|

**Installing pyCreeper** is very easy and mostly simply means extracting the zip file and putting the contents into a location of your choice. Have a look at the `Readme file on GitHub <https://github.com/Elendurwen/pyCreeper>`_ to find out what dependencies you need and how to include pyCreeper in your project.

**Using pyCreeper?** `Let me know <mailto:contact@lenkaspace.net>`_ **and I will feature your project here!**

Newest additions
--------------------

* :ref:`Advanced: Broken line plots`
* New functions in :mod:`pyCreeper.crData`:
    * Compress a list into a shorter lists: :func:`pyCreeper.crData.compressList`
    * Flip columns and rows of 2D arrays: :func:`pyCreeper.crData.getListByFlippingColumnsAndRows`
    * Get median of a list and optionally ignore 0-values: :func:`pyCreeper.crData.getMedianOfAList`

* Better automatic detection of y-axis range y-ticks for plots
* Better styling of box plots


Contents
--------------------

.. toctree::
    :maxdepth: 2

    download
    supportedGraphs
    examples
    advanced_usingStyles
    advanced_brokenLinePlots
    api
    versionHistory

About
--------------------

Developed by `Lenka Pitonakova <http://lenkaspace.net/>`_ [`email <mailto:contact@lenkaspace.net>`_ `twitter <http://twitter.com/l_pitonakova>`_ `linkedIn <http://uk.linkedin.com/pub/lenka-pitonakova/b6/a61/54b>`_]
mostly as a part of the project `Designing Robot Swarms <http://robot-swarms-design.lenkaspace.net>`_

Related to this library is `Creeper <http://lenkaspace.net/index.php/code/java/creeper>`_, a Java framework for coding multi-agent simulations.


Indices and tables
--------------------

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

