"""

A module that let you create pretty graphs with single-line function calls

Author: Lenka Pitonakova: contact@lenkaspace.net

"""
import pylab;
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

SHOW_OUTPUT = True;

from . import crHelpers;

TITLE_FONT_SIZE = 'xx-large';
LABEL_FONT_SIZE = 'xx-large';
TICK_FONT_SIZE = "large";

DEFAULT_COLORS = ['b','r','g','c','k'];
DEFAULT_MARKERS = ['b-','r-','g-','c-','k-'];

DPI = 100;

INVALID_VALUE = -999999;
#
def createPieChart(data_=[], itemLabels_=[], itemColors_=[],
                    title_="", showActualVals_=True, showPercentageVals_=False, showShadow_=False,
                    titleFontSize_=INVALID_VALUE, itemsFontSize_= INVALID_VALUE, valuesFontSize_=INVALID_VALUE, size_=(6,6),
                    filePath_ = "", holdFigure_=False, figure_=None, subPlot_=111):
    """

    Create a pie chart

    :param `data_`: A 1D list of values
    :param `itemLabels_`: A 1D list of value labels. Must be the same length as `data_`
    :param `itemColors_`: (optional, default = DEFAULT_COLORS) A 1D list of colors for each value. Must be the same length as `data_`
    :param `showActualVals_`: (optional, default = True) Boolean whetehr to show data values in the pie parts
    :param `showPercentageVals_`: (optional, default = False) Boolean whether to show percentages in the pie parts
    :param `showShadow_`: (optional, default = False) Boolean whether to show shadow underneath the pie
    :param `titleFontSize_`: (optional, default = TITLE_FONT_SIZE) Font size of the title
    :param `groupsFontSize_`: (optional, default = LABEL_FONT_SIZE) Font size of the item names
    :param `valuesFontSize_`: (optional, default = TICK_FONT_SIZE) Font size of values in the pie
    :param `size_`: (optional, default = (8,6)) Size of the graph
    :param `filePath_`: (optional, default = "") If not empty, the graph will be saved to the file path specified. If empty, the figure will be displayed on screen instead.
    :param `holdFigure_`: (optional, default = False) If true, the figure will not be displayed or printed
    :param `figure_`: (optional, default = None) If not None, the graph will be created into this figure (pylab.figure)
    :param `subPlot_`: (optional, default = 111) The subplot id of where to place the graph to

    :return: pylab.figure for the graph

    """

    #-- test and pre-set data
    crHelpers.checkVariableIsList(data_,1);
    crHelpers.checkVariableIsList(itemLabels_,1);
    crHelpers.checkVariableIsList(itemColors_,1);

    crHelpers.checkListsHaveTheSameLength(data_, itemLabels_, "groupLabels_");

    itemsFontSize_ = replaceInvalidWithDefaultValue(itemsFontSize_, LABEL_FONT_SIZE);
    valuesFontSize_ = replaceInvalidWithDefaultValue(valuesFontSize_, TICK_FONT_SIZE);
    titleFontSize_ = replaceInvalidWithDefaultValue(titleFontSize_, TITLE_FONT_SIZE);

    #--
    
    if (figure_ == None):
        fig = pylab.figure(figsize=size_, dpi=DPI);
    else:
        fig = figure_;

    ax = fig.add_subplot(subPlot_);

    #-- specify title or stretch the graph if there is no title
    if (title_ != ""):
        fig.suptitle(title_, fontsize=titleFontSize_)
    else:
        box = ax.get_position();
        ax.set_position([box.x0 - box.width *0.10, box.y0 - box.height*0.1, box.width*1.2, box.height * 1.2]);
    
    if (len(itemColors_) == 0):
        itemColors_ = DEFAULT_COLORS;

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
    patches, texts, autotexts = ax.pie(data_, labels=itemLabels_, autopct=formatPieceNumber, shadow=showShadow_, colors=itemColors_);
    
    #-- setup fonts
    proptease = fm.FontProperties();
    proptease.set_size(itemsFontSize_);
    plt.setp(texts, fontproperties=proptease);
    proptease.set_size(valuesFontSize_);
    plt.setp(autotexts, fontproperties=proptease);
    
    #-- display / print:
    if (not holdFigure_):
        if (len(filePath_) > 0):
            pylab.savefig(filePath_, format='png')
            if (SHOW_OUTPUT == True):
                print("Saved " + filePath_);
        else:
            pylab.show()
    #--
    return fig;


#============================================================================
#============================== HELPER FUNCTIONS ============================
#============================================================================

def replaceInvalidWithDefaultValue(value_, defaultValue_):
    """
    Used when checking parameter values.
    If the parameter value (`value_`) is `crGraphs.INVALID_VALUE`, returns a specified `defaultValue_` instead.

    :param `value_`: the value
    :param `defaultValue_`: the value to use if `value_` == INVALID_VALUE
    """
    if (value_ == INVALID_VALUE):
        return defaultValue_;
    else:
        return value_;
