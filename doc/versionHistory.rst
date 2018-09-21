
.. image:: images/download.png
    :width: 220 px
    :align: left
    :target: https://github.com/LPitonakova/pyCreeper/archive/master.zip

**You can also download or clone pyCreeper from GitHub:** `https://github.com/Elendurwen/pyCreeper <https://github.com/Elendurwen/pyCreeper>`_

|
|

**Installing pyCreeper** is very easy and mostly simply means extracting the zip file and putting the contents into a location of your choice. Have a look at the `Readme file on GitHub <https://github.com/Elendurwen/pyCreeper>`_ to find out what dependencies you need and how to include pyCreeper in your project.

**Using pyCreeper?** `Let me know <mailto:contact@lenkaspace.net>`_ **and I will feature your project here!**

===================================================
Version history
===================================================

----------------------------
2.1 (NEW!)
----------------------------

* **New plot type: Bar plot** (see :ref:`Bar plot examples`)
* **Bar and line plot legends can have optional titles** (see :func:`examples.barPlots.example2_errorBars`)
* Box plot width can now be specified using the :func:`pyCreeper.crGraphStyle.boxPlotWidth` property
* Plot legends are semi-transparent to allow seeing data points underneath
* Better automatic detection of which x-axis tick to show

* Plot range and size bug fixes

----------------------------
2.0
----------------------------

* **Properly encapsulated plot styles!** :ref:`Tutorial: Using styles`
* **Reading text files into 2D arrays** with a new module :mod:`pyCreeper.crFiles`
* New functions in :mod:`pyCreeper.crData`:
    * Add and remove unique list elements with :func:`pyCreeper.crData.addUniqueElementToList` and :func:`pyCreeper.crData.removeElementFromList`
    * Extract data from a specific list column: :func:`pyCreeper.crData.getListColumnAsArray`
    * Get the average value in a list: :func:`pyCreeper.crData.getAverageOfAList`

* Minor bug fixes

----------------------------
1.1
----------------------------

* :ref:`Tutorial: Broken line plots`
* New functions in :mod:`pyCreeper.crData`:
    * Compress a list into a shorter lists: :func:`pyCreeper.crData.compressList`
    * Flip columns and rows of 2D arrays: :func:`pyCreeper.crData.getListByFlippingColumnsAndRows`
    * Get median of a list and optionally ignore 0-values: :func:`pyCreeper.crData.getMedianOfAList`

* Better automatic detection of y-axis range y-ticks for plots
* Better styling of box plots

* Minor bug fixes

----------------------------
1.0
----------------------------

Basic plot types:

* Line and box plots (see :ref:`Line and box plot examples`)
* Matrix plots (see :ref:`Matrix plot examples`)
* Pie charts (see :ref:`Pie chart examples`)

Basic functions in :mod:`pyCreeper.crData`:

* :func:`pyCreeper.crData.getNumberOfListDimensions`
* :func:`pyCreeper.crData.getMinValueInAList`
* :func:`pyCreeper.crData.getMaxValueInAList`