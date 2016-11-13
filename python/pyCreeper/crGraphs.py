"""

A module that lets you create pretty graphs with single-line function calls.

Useful constants:

* **SHOW_OUTPUT** - (default = False) Set to True to see output of the functions
* **BASE_FILE_PATH** - (default =  "./") File path that is pre-pended to any `filePath_` parameters of the functions
* **DPI** - (default = 100) DPI of created figures. Set to a higher number for a higher resolution.

To override the constants, set them after importing `crGraphs`, e.g.

.. code-block:: python

    from pyCreeper import crGraphs;
    crGaphs.DPI = 200;

Author: Lenka Pitonakova: contact@lenkaspace.net

"""
import pylab;
import matplotlib.pyplot as plt;
from matplotlib import font_manager as fm;
from copy import deepcopy;
import math;

from . import crHelpers;
from . import crData;


#-- constants
SHOW_OUTPUT = True;
BASE_FILE_PATH = "./";
DPI = 100;

TITLE_FONT_SIZE = 'xx-large';
LABEL_FONT_SIZE = 'xx-large';
TICK_FONT_SIZE = "large";

DEFAULT_COLORS = ['b','r','g','c','k'];
DEFAULT_MARKERS = ['b-','r-','g-','c-','k-'];



INVALID_VALUE = -999999;

def createPieChart(data_=[], itemLabels_=[],
                    title_="", itemColors_=[],
                    showActualVals_=True, showPercentageVals_=False, showShadow_=False,
                    titleFontSize_=INVALID_VALUE, itemsFontSize_= INVALID_VALUE, valuesFontSize_=INVALID_VALUE, size_=(6,6),
                    filePath_ = "", renderFigure_=True, figure_=None, subPlot_=111):
    """
    Create a pie chart.

     Minimal example:

    .. code-block:: python

        expenseCategories = ["Rent", "Food", "Travel", "Fun"];
        expenses = [1000, 300, 500, 250];
        crGraphs.createPieChart(expenses, expenseCategories);


    :param `data_`: A 1D list of values
    :param `itemLabels_`: A 1D list of value labels. Must be the same length as `data_`
    :param `title_`: (optional, default = "") The figure title
    :param `itemColors_`: (optional, default = DEFAULT_COLORS) A 1D list of colors for each value. Must be the same length as `data_`
    :param `showActualVals_`: (optional, default = True) Boolean whetehr to show data values in the pie parts
    :param `showPercentageVals_`: (optional, default = False) Boolean whether to show percentages in the pie parts
    :param `showShadow_`: (optional, default = False) Boolean whether to show shadow underneath the pie
    :param `titleFontSize_`: (optional, default = TITLE_FONT_SIZE) Font size of the title
    :param `groupsFontSize_`: (optional, default = LABEL_FONT_SIZE) Font size of the item names
    :param `valuesFontSize_`: (optional, default = TICK_FONT_SIZE) Font size of values in the pie
    :param `size_`: (optional, default = (6,6)) The figure size
    :param `filePath_`: (optional, default = "") If not empty, the figure will be saved to the file path specified. If empty, the figure will be displayed on screen instead.
    :param `renderFigure_`: (optional, default = True) If false, the figure will not be displayed or printed. Set to False when putting multiple figures together via the `figure_` parameter.
    :param `figure_`: (optional, default = None) If not None, the figure will be created into this figure (pylab.figure)
    :param `subPlot_`: (optional, default = 111) The subplot id of where to place the graph to

    :return: pylab.figure
    """

    #-- test and pre-set data
    crHelpers.checkVariableIsList(data_,1,True);
    crHelpers.checkVariableIsList(itemLabels_,True);
    crHelpers.checkVariableIsList(itemColors_);

    crHelpers.checkListsHaveTheSameLength(data_, itemLabels_, "itemLabels_");

    if (len(itemColors_) > 0):
        crHelpers.checkListsHaveTheSameLength(data_, itemColors_, "itemColors_");

    itemsFontSize_ = replaceInvalidWithDefaultValue(itemsFontSize_, LABEL_FONT_SIZE);
    valuesFontSize_ = replaceInvalidWithDefaultValue(valuesFontSize_, TICK_FONT_SIZE);

    if (len(itemColors_) == 0):
        itemColors_ = DEFAULT_COLORS;

    #--

    def formatPieceNumber(val_):
        if (showActualVals_ and showPercentageVals_):
            val=int(val_*sum(data_)/100.0)
            return '{p:.1f}% ({v:d})'.format(p=val_,v=val);
        if (showActualVals_):
            val=int(val_*sum(data_)/100.0)
            return '{v:d}'.format(v=val);
        elif (showPercentageVals_):
            return '{p:.2f}%'.format(p=val_);
        return '';
        
    #-- create the graph
    fig, ax = createFigure(size_, title_, figure_, subPlot_, titleFontSize_=titleFontSize_);
    patches, texts, autotexts = ax.pie(data_, labels=itemLabels_, autopct=formatPieceNumber, shadow=showShadow_, colors=itemColors_);
    
    #-- setup fonts
    proptease = fm.FontProperties();
    proptease.set_size(itemsFontSize_);
    plt.setp(texts, fontproperties=proptease);
    proptease.set_size(valuesFontSize_);
    plt.setp(autotexts, fontproperties=proptease);
    
    #-- display / print, return:
    renderFigure(filePath_, renderFigure_);
    return fig;



def createMatrixPlot(data_=[[],[]],
                    title_="", xLabel_ = "", yLabel_ = "", xTickLabels_ = [], yTickLabels_ = [], colorBarLabel_ = "",
                    colorMap_ = None, minValue_ = INVALID_VALUE, maxValue_ = INVALID_VALUE,
                    annotateValues_=False, annotationStringAfter_="", annotationValues_=[[],[]], roundAnnotatedValues_=False,
                    titleFontSize_=INVALID_VALUE, labelFontSize_ = INVALID_VALUE, tickFontSize_ = INVALID_VALUE, size_=(8,6),
                    filePath_ = "", renderFigure_=True, figure_=None, subPlot_=111):

    """
    Create 2D matrix plot where color gradient represents value on a 3rd dimension.

    Minimal example:

    .. code-block:: python

        performanceData = [
                        [12,11,10,9],
                        [11,10,7,6],
                        [9,8,6,5],
                        ];
        crGraphs.createMatrixPlot(performanceData);

    :param `data_`: a 2D list of values, where the 0th dimension runs along the x axis and the 1st dimension along y axis, so [0,0] in the list specified a value for the bottom left square
    :param `title_`: (optional, default = "") The figure title
    :param xLabel_: (optional, default = "") Label of the x-axis
    :param yLabel_: (optional, default = "") Label of the y-axis
    :param xTickLabels_: (optional, default = []) Labels of the individual ticks of the x-axis. If empty, values 0-N are displayed
    :param yTickLabels_: (optional, default = []) Labels of the individual ticks of the y-axis. If empty, values 0-N are displayed
    :param colorBarLabel_: (optional, default = "") Label of color bar, displayed vertically
    :param colorMap_: (optional, default = "summer") A python.colormap isntance to use for the matrix plot
    :param minValue_: (optional, default = `INVALID_VALUE`) Minimum float value that the color map considers. If set to INVALID_VALUE, the value is automatically calculated from `data_`
    :param maxValue_: (optional, default = `INVALID_VALUE`) Maximum float value that the color map considers. If set to INVALID_VALUE, the value is automatically calculated from `data_`
    :param annotateValues_: (optional, default = False) If True, data values will be displayed in the matrix plot
    :param annotationStringAfter_: (optional, default = "") A string to append after each annotation value
    :param annotationValues_: (optional, default = [[],[]]) A 2D list of annotations in the matrix plot. If non-empty, must have the same dimensions as `data_`
    :param roundAnnotatedValues_: (optional, default = False) If True and if `annotationValues_` is empty, annotation numbers will be rounded
    :param `titleFontSize_`: (optional, default = TITLE_FONT_SIZE) Font size of the title
    :param `labelFontSize_`: (optional, default = LABEL_FONT_SIZE) Font size of the axis and color bar labels
    :param `tickFontSize_`: (optional, default = TICK_FONT_SIZE) Font size of axis ticks and of values inside the plot
    :param `size_`: (optional, default = (8,6)) The figure size
    :param `filePath_`: (optional, default = "") If not empty, the figure will be saved to the file path specified. If empty, the figure will be displayed on screen instead.
    :param `renderFigure_`: (optional, default = True) If false, the figure will not be displayed or printed. Set to False when putting multiple figures together via the `figure_` parameter.
    :param `figure_`: (optional, default = None) If not None, the figure will be created into this figure (pylab.figure)
    :param `subPlot_`: (optional, default = 111) The subplot id of where to place the graph to

    :return: pylab.figure for the graph
    """


    #-- test and pre-set data
    crHelpers.checkVariableIsList(data_,2,True);
    crHelpers.checkVariableIsList(xTickLabels_);
    crHelpers.checkVariableIsList(yTickLabels_);
    crHelpers.checkVariableIsList(annotationValues_,2);

    if (len(xTickLabels_) > 0):
        crHelpers.checkListsHaveTheSameLength(data_[1], xTickLabels_, "xTickLabels_");
    if (len(yTickLabels_) > 0):
        crHelpers.checkListsHaveTheSameLength(data_, yTickLabels_, "yTickLabels_");

    labelFontSize_ = replaceInvalidWithDefaultValue(labelFontSize_, LABEL_FONT_SIZE);
    tickFontSize_ = replaceInvalidWithDefaultValue(tickFontSize_, TICK_FONT_SIZE);


    if (len(annotationValues_[0]) == 0):
        annotationValues_ = deepcopy(data_);

    if (minValue_ == INVALID_VALUE):
        minValue_ = crData.getMinValueInAList(data_);
    if (maxValue_ == INVALID_VALUE):
        maxValue_ = crData.getMaxValueInAList(data_);


    #-- decide on colors
    origin = 'lower';
    if (colorMap_ == None):
        cmap=plt.cm.get_cmap("summer");
    else:
        cmap=colorMap_;

    #-- create the figure
    fig, ax = createFigure(size_, title_, figure_, subPlot_, xLabel_, yLabel_, titleFontSize_, labelFontSize_, tickFontSize_);
    cax = ax.matshow(data_,cmap=cmap,origin=origin,vmin=minValue_,vmax=maxValue_);

    #-- set tick labels
    if (len(xTickLabels_) > 0):
        ax.set_xticklabels([''] + xTickLabels_);
    if (len(yTickLabels_) > 0):
        ax.set_yticklabels([''] + yTickLabels_);


    #-- make a colorbar for the ContourSet returned by the contourf call.
    cbar = fig.colorbar(cax)
    cbar.ax.set_ylabel(colorBarLabel_, size=labelFontSize_);
    for t in cbar.ax.get_yticklabels():
        t.set_fontsize(tickFontSize_)

    #-- annotations
    if (annotateValues_):
        #-- the XY grid position has [0;0] in the bottom left corner
        gridStartX=0.0;
        gridStartY=0.0;
        gridEndX=1.0;
        gridEndY=1.0;
        gridStepX=(gridEndX-gridStartX)/len(data_[0]);
        gridStepY=(gridEndY-gridStartY)/len(data_);
        for y in range(len(data_)):
            for x in range(len(data_[0])):
                if (roundAnnotatedValues_):
                    ax.annotate(str(math.ceil(annotationValues_[y][x] * 100) / 100.0) + annotationStringAfter_, xy=(gridStartX+x*gridStepX+gridStepX/2, gridStartY+y*gridStepY+gridStepY/2),  xycoords='axes fraction',horizontalalignment='center', verticalalignment='center')
                else:
                    ax.annotate(str(annotationValues_[y][x]) + annotationStringAfter_, xy=(gridStartX+x*gridStepX+gridStepX/2, gridStartY+y*gridStepY+gridStepY/2),  xycoords='axes fraction',horizontalalignment='center', verticalalignment='center')

    #-- display / print, return:
    renderFigure(filePath_, renderFigure_);
    return fig;


#============================================================================
#============================== HELPER FUNCTIONS ============================
#============================================================================

def renderFigure(filePath_="", renderFigure_=True):
    """
    A helper function that performs the current pylab's figure rendering into a file or on screen

    :param `filePath_`: (optional, default = "") If not empty, the figure will be saved to the file path specified. If empty, the figure will be displayed on screen instead.
    :param `renderFigure_`: (optional, default = True) If false, the figure will not be displayed or printed.
    """
    if (renderFigure_):
        if (len(filePath_) > 0):
            filePath_ = BASE_FILE_PATH + filePath_;
            pylab.savefig(filePath_, format='png')
            if (SHOW_OUTPUT == True):
                print("Saved " + filePath_);
        else:
            pylab.show()



def createFigure(size_, title_="", figure_=None, subPlot_=111,
                xLabel_="", yLabel_="",
                titleFontSize_=INVALID_VALUE, labelFontSize_=INVALID_VALUE, tickFontSize_=INVALID_VALUE):

    """
    A helper function that creates a figure.

    :param `size_`: The figure size
    :param `title_`: (optional, default = "") The figure title
    :param `figure_`: (optional, default = None) If not None, the figure will be created into this figure (pylab.figure)
    :param `subPlot_`: (optional, default = 111) The subplot id of where to place the graph to
    :param `xLabel_`: (optional, default = "") Label of the x-axis
    :param `yLabel_`: (optional, default = "") Label of the y-axis
    :param `titleFontSize_`: (optional, default = TITLE_FONT_SIZE) Font size of the title
    :param `labelFontSize_`: (optional, default = LABEL_FONT_SIZE) Font size of the axis and color bar labels
    :param `tickFontSize_`: (optional, default = TICK_FONT_SIZE) Font size of axis ticks and of values inside the plot

    :return: (pylab.figure, pylab.ax)
    """

    #-- test and pre-set data
    titleFontSize_ = replaceInvalidWithDefaultValue(titleFontSize_, TITLE_FONT_SIZE);
    labelFontSize_ = replaceInvalidWithDefaultValue(labelFontSize_, LABEL_FONT_SIZE);
    tickFontSize_ = replaceInvalidWithDefaultValue(tickFontSize_, TICK_FONT_SIZE);

    if (figure_ == None):
        fig = pylab.figure(figsize=size_, dpi=DPI);
    else:
        fig = figure_;

    ax = fig.add_subplot(subPlot_);

    #-- specify title or stretch the graph if there is no title
    if (title_ != ""):
        fig.suptitle(title_, fontsize=titleFontSize_)
        box = ax.get_position();
        ax.set_position([box.x0 - box.width *0.05, box.y0 - box.height*0.1, box.width*1.1, box.height * 1.1]);
    else:
        box = ax.get_position();
        ax.set_position([box.x0 - box.width *0.10, box.y0 - box.height*0.1, box.width*1.2, box.height * 1.2]);


    pylab.xlabel(xLabel_, size=labelFontSize_);
    pylab.ylabel(yLabel_, size=labelFontSize_);
    pylab.xticks(size=tickFontSize_);
    pylab.yticks(size=tickFontSize_);

    return (fig, ax)



def replaceInvalidWithDefaultValue(value_, defaultValue_):
    """
    A helper function used when checking parameter values.
    If the parameter value (`value_`) is `crGraphs.INVALID_VALUE`, returns a specified `defaultValue_` instead.

    :param `value_`: the value
    :param `defaultValue_`: the value to use if `value_` == INVALID_VALUE
    """
    if (value_ == INVALID_VALUE):
        return defaultValue_;
    else:
        return value_;


