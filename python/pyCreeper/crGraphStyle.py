INVALID_VALUE = -999999;

from enum import Enum, unique
from matplotlib import pyplot;
import matplotlib;
from . import crHelpers;

@unique
class LEGEND_POSITION(Enum):
    BEST = "best"
    UPPER_RIGHT = "upper right"
    UPPER_LEFT = "upper left"
    LOWER_LEFT = "lower left"
    LOWER_RIGHT = "lower right"
    RIGHT = "right"
    CENTER_LEFT = "center left"
    CENTER_RIGHT = "center right"
    LOWER_CENTER = "lower center"
    UPPER_CENTER = "upper center"
    CENTER = "center"

@unique
class GRID_TYPE(Enum):
    NONE = 0
    FULL = 1
    HORIZONTAL = 2
    VERTICAL = 3
    MAJOR = 4
    MAJOR_HORIZONTAL = 5
    MAJOR_VERTICAL = 6
    MINOR = 7
    MINOR_HORIZONTAL = 8
    MINOR_VERTICAL = 9

class crGraphStyle:

    """
    Encapsulates styling that :mod:`pyCreeper.crData` uses.

    Author: Lenka Pitonakova: contact@lenkaspace.net

    Minimal example:

    .. code-block:: python

        myStyle = pyCreeper.crGraphStyle.crGraphStyle();
        style.lineWidth = 3;
        pyCreeper.crGraphs.setStyle(style);

        # now use pyCreeper.crGraphs functions and the new style will be applied

    """

    __markers = INVALID_VALUE;
    __colors = INVALID_VALUE;
    __colorMap = INVALID_VALUE;
    __lineWidth = INVALID_VALUE;
    __boxPlotLineWidth = INVALID_VALUE;
    __markerSize = INVALID_VALUE;
    __lineStyles = INVALID_VALUE;
    __gridType = INVALID_VALUE;
    __legendPosition = INVALID_VALUE;
    __titleFontSize = INVALID_VALUE;
    __legendFontSize = INVALID_VALUE;
    __labelFontSize = INVALID_VALUE;
    __tickFontSize = INVALID_VALUE;
    __figureSize = INVALID_VALUE;
    __xOffset = INVALID_VALUE;
    __yOffset = INVALID_VALUE;
    __numOfLegendColumns = INVALID_VALUE;

    __xLabelPadding = INVALID_VALUE;
    __yLabelPadding = INVALID_VALUE;

    __initDone = False;

    wereColorsSetByUser = False;

    def __init__(self):
        self.reset();
        self.__initDone = True;

    def reset(self):
        """
        Set everything to defaults
        """
        self.lineWidth = 2;
        self.boxPlotLineWidth = 2;
        self.markerSize = 12;
        self.lineStyles = [];
        self.gridType = GRID_TYPE.FULL;
        self.legendPosition = LEGEND_POSITION.BEST;
        self.titleFontSize = 25;
        self.labelFontSize = 25;
        self.legendFontSize = 25;
        self.tickFontSize = 17;
        self.figureSize = (12,6);
        self.xOffset = 0.0;
        self.yOffset = 0.0;
        self.markers = ['bs-','rs-','gs-','cs-','ks-'];
        self.colors = ['b','r','g','c','k'];
        self.colorMap = pyplot.cm.get_cmap("summer");
        self.numOfLegendColumns = 2;
        self.xLabelPadding = 20;
        self.yLabelPadding = 20;


        self.wereColorsSetByUser = False;

    def getMatplotlibGridSettings(self):
        """
        Get matplotlib strings that should be used for matplotlib's `ax.grid(which=gridWhich, axis=gridAxis)`

        :return: [gridAxis, gridWhich]
        """

        gridAxis = 'both';
        gridWhich = 'both';
        if (self.gridType == GRID_TYPE.HORIZONTAL or self.gridType == GRID_TYPE.MAJOR_HORIZONTAL or self.gridType == GRID_TYPE.MINOR_HORIZONTAL):
            gridAxis = 'y';
        elif (self.gridType == GRID_TYPE.VERTICAL or self.gridType == GRID_TYPE.MAJOR_VERTICAL or self.gridType == GRID_TYPE.MAJOR_VERTICAL):
            gridAxis = 'x';

        if (self.gridType == GRID_TYPE.MAJOR or self.gridType == GRID_TYPE.MAJOR_HORIZONTAL or self.gridType == GRID_TYPE.MAJOR_VERTICAL):
            gridWhich = 'major';
        elif (self.gridType == GRID_TYPE.MINOR or self.gridType == GRID_TYPE.MINOR_HORIZONTAL or self.gridType == GRID_TYPE.MINOR_VERTICAL):
            gridWhich = 'minor';

        return [gridAxis, gridWhich];

    @property
    def xLabelPadding(self):
        """
        Padding between the X axis label and markers. Default = 20
        """
        return self.__xLabelPadding;
    @xLabelPadding.setter
    def xLabelPadding(self, value):
        crHelpers.checkVariableDataType(value, int);
        self.__xLabelPadding = value


    @property
    def yLabelPadding(self):
        """
        Padding between the Y axis label and markers. Default = 20
        """
        return self.__yLabelPadding;
    @yLabelPadding.setter
    def yLabelPadding(self, value):
        crHelpers.checkVariableDataType(value, int);
        self.__yLabelPadding = value



    @property
    def numOfLegendColumns(self):
        """
        Number of columns in the legend. Default = 2
        """
        return self.__numOfLegendColumns;
    @numOfLegendColumns.setter
    def numOfLegendColumns(self, value):
        crHelpers.checkVariableDataType(value, int);
        self.__numOfLegendColumns = value


    @property
    def markers(self):
        """
        A 1D list of markers for the plot lines. Default = ['bs-','rs-','gs-','cs-','ks-']
        """
        return self.__markers;
    @markers.setter
    def markers(self, value):
        crHelpers.checkVariableIsList(value,1,True);
        self.__markers = value


    @property
    def colors(self):
        """
        A 1D list of colors for the plot lines. Default = ['b','r','g','c','k']
        """
        return self.__colors;
    @colors.setter
    def colors(self, value):
        crHelpers.checkVariableIsList(value,1,True);
        self.wereColorsSetByUser = True;
        self.__colors = value

    @property
    def colorMap(self):
        """
        A python.cm instance to use for the matrix plots. Default = pyplot.cm.get_cmap("summer")
        """
        return self.__colorMap;
    @colorMap.setter
    def colorMap(self, value):
        crHelpers.checkVariableDataType(value,matplotlib.colors.Colormap);
        self.__colorMap = value;


    @property
    def xOffset(self):
        """
        Horizontal offset of the plot. Note this doesn't work for matrix plots. Default = 0.0
        """
        return self.__xOffset;
    @xOffset.setter
    def xOffset(self, value):
        crHelpers.checkVariableDataType(value, float);
        self.__xOffset = value


    @property
    def yOffset(self):
        """
        Vertical offset of the plot. Note this doesn't work for matrix plots. Default = 0.0
        """
        return self.__yOffset;
    @yOffset.setter
    def yOffset(self, value):
        crHelpers.checkVariableDataType(value, float);
        self.__yOffset = value


    @property
    def figureSize(self):
        """
        The figure size. Default = (12,6)
        """
        return self.__figureSize;
    @figureSize.setter
    def figureSize(self, value):
        crHelpers.checkVariableDataType(value, tuple);
        self.__figureSize = value

    @property
    def tickFontSize(self):
        """
        Font size of axis ticks and of values inside the plot. Default = 17
        """
        return self.__tickFontSize;
    @tickFontSize.setter
    def tickFontSize(self, value):
        crHelpers.checkVariableDataType(value, int);
        self.__tickFontSize = value


    @property
    def labelFontSize(self):
        """
        Font size of the axis and color bar labels. Default = 25
        """
        return self.__labelFontSize;
    @labelFontSize.setter
    def labelFontSize(self, value):
        crHelpers.checkVariableDataType(value, int);
        self.__labelFontSize = value


    @property
    def legendFontSize(self):
        """
        Font size of the legend. Default = 25
        """
        return self.__legendFontSize;
    @legendFontSize.setter
    def legendFontSize(self, value):
        crHelpers.checkVariableDataType(value, int);
        self.__legendFontSize = value


    @property
    def titleFontSize(self):
        """
        Font size of the title. Default = 25
        """
        return self.__titleFontSize;
    @titleFontSize.setter
    def titleFontSize(self, value):
        crHelpers.checkVariableDataType(value, int);
        self.__titleFontSize = value

    @property
    def boxPlotLineWidth(self):
        """
        Box plot line width. Default = 2
        """
        return self.__boxPlotLineWidth;
    @boxPlotLineWidth.setter
    def boxPlotLineWidth(self, value):
        crHelpers.checkVariableDataType(value, int);
        self.__boxPlotLineWidth = value

    @property
    def lineWidth(self):
        """
        Line width. Default = 2
        """
        return self.__lineWidth;
    @lineWidth.setter
    def lineWidth(self, value):
        crHelpers.checkVariableDataType(value, int);
        self.__lineWidth = value

    @property
    def lineStyles(self):
        """
        A 1D list of line styles for the plot lines. If a corresponding style for a plot line is not specified, a solid line is displayed.
        """
        return self.__lineStyles;
    @lineStyles.setter
    def lineStyles(self, value):
        crHelpers.checkVariableIsList(value);
        self.__lineStyles = value


    @property
    def gridType(self):
        """
        A :class:`.GRID_TYPE` enum member. Default = `GRID_TYPE.FULL`
        """
        return self.__gridType;
    @gridType.setter
    def gridType(self, value):
        crHelpers.checkVariableDataType(value, GRID_TYPE);
        self.__gridType = value


    @property
    def legendPosition(self):
        """
        A :class:`.LEGEND_POSITION` enum member. Default = `LEGEND_POSITION.BEST`
        """
        return self.__legendPosition;
    @legendPosition.setter
    def legendPosition(self, value):
        crHelpers.checkVariableDataType(value, LEGEND_POSITION);
        self.__legendPosition = value


    @property
    def markerSize(self):
        """
        Size of markers. Default = 12
        """
        return self.__markerSize;
    @markerSize.setter
    def markerSize(self, value):
        crHelpers.checkVariableDataType(value, int);
        self.__markerSize = value


    def __setattr__(self, key, value):
        """
        Override the setattr to prevent creation of new attributes
        :param key:
        :param value:
        """
        if self.__initDone and not hasattr(self, key):
            raise AttributeError("crGraphStyle: Attribute " + str(key) + " does not exist");
        object.__setattr__(self, key, value)



