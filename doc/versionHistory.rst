===================================================
Version history
===================================================

----------------------------
2.0 (NEW!)
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