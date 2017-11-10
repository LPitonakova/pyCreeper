"""

A module that lets you create pretty graphs with single-line function calls.

Useful constants:

* **SHOW_OUTPUT** - (default = False) Set to True to see output of the functions
* **BASE_FILE_PATH** - (default =  "./") File path that is pre-pended to any `filePath_` parameters of the functions
* **DPI** - (default = 100) DPI of created figures. Set to a higher number for a higher resolution.
* **DEBUG_LEVEL** - (default = 0) O - no debug messages, 1 - some debug messages, 2 - deep debug messages

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
import numpy;
import scipy;
import itertools;
import os;
from enum import Enum, unique

from . import crHelpers;
from . import crData;


#-- constants
SHOW_OUTPUT = True;
BASE_FILE_PATH = "./";
DPI = 100;

TITLE_FONT_SIZE = '21';
LABEL_FONT_SIZE = '21';
TICK_FONT_SIZE = "14";

DEFAULT_COLORS = ['b','r','g','c','k'];
DEFAULT_MARKERS = ['bs-','rs-','gs-','cs-','ks-'];

INVALID_VALUE = -999999;

DEBUG_LEVEL = 0;

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




def createBarChart(data_,
                    title_="", xLabel_ = "", yLabel_ = "", xTickLabels_=[], legendLabels_ = [], numOfLegendColumns_ = 2, legendPosition_=LEGEND_POSITION.BEST, colors_ = [],
                    showConfidenceIntervals_=False, barWidth_ = 0.35,
                    xMin_=INVALID_VALUE, xMax_=INVALID_VALUE, xAxisGroupSize_ = 0, yMin_=INVALID_VALUE, yMax_=INVALID_VALUE, yTicksStep_ = 0, yTicksStepMultiplier_ = 1,
                    titleFontSize_=INVALID_VALUE, labelFontSize_ = INVALID_VALUE, tickFontSize_ = INVALID_VALUE, legendFontSize_ = INVALID_VALUE, size_=(12,6),
                    filePath_ = "", renderFigure_=True, figure_=None, subPlot_=111):
    """
    Create bars for groups next to each other, grouped by group labels. [Work in progress]
    """

    #-- test and pre-set data
    numOfDataDimensions = crData.getNumberOfListDimensions(data_);
    if (numOfDataDimensions < 2 or numOfDataDimensions > 3):
        raise ValueError("The data_ parameter must be a 2D or a 3D list.")

    if (len(xTickLabels_) == 0):
        xTickLabels_ = range(len(data_[0]));

    crHelpers.checkListsHaveTheSameLength(data_[0], xTickLabels_);

    if (len(legendLabels_) > 0):
        crHelpers.checkListsHaveTheSameLength(data_, legendLabels_);

    crHelpers.checkVariableDataType(legendPosition_, LEGEND_POSITION);

    titleFontSize_ = replaceInvalidWithDefaultValue(titleFontSize_, TITLE_FONT_SIZE)
    labelFontSize_ = replaceInvalidWithDefaultValue(labelFontSize_, LABEL_FONT_SIZE);
    tickFontSize_ = replaceInvalidWithDefaultValue(tickFontSize_, TICK_FONT_SIZE);
    legendFontSize_ = replaceInvalidWithDefaultValue(legendFontSize_, LABEL_FONT_SIZE);


    xLocations = numpy.arange(len(data_[0]))  # the x locations for the groups

    fig, ax = createFigure(size_, title_, figure_, subPlot_, xLabel_, yLabel_, titleFontSize_, labelFontSize_, tickFontSize_, 1.2, 1.05);

    plt.xticks(xLocations+barWidth_, size=labelFontSize_);
    ax.set_xticklabels( xTickLabels_, size=tickFontSize_);


    #-- plot bars next to each other
    plots = [];
    maxVal = -9999999;
    minVal = 9999999;
    for i in range(len(data_)):
        #-- pick a color
        if (len(colors_) > i):
            colorCode = colors_[i];
        elif (len(DEFAULT_COLORS) > i):
            colorCode = DEFAULT_COLORS[i];

        if (numOfDataDimensions == 3):
            medians = [];
            for q in range(len(data_[i])):
                medians.append(numpy.median(data_[i][q]));

                for r in range(len(data_[i][q])):
                    if (data_[i][q][r] > maxVal):
                        maxVal = data_[i][q][r];
                    if (data_[i][q][r] < minVal):
                        minVal = data_[i][q][r]

            if (showConfidenceIntervals_):
                dataDof = [(len(data_[i][q])-1) for q in range(len(medians))]; #degrees of freedom is sample size -1
                dataStd = [numpy.std(data_[i][q]) for q in range(len(medians))];
                plot = ax.bar(xLocations+i*barWidth_, medians, barWidth_, color=colorCode, yerr=scipy.stats.t.ppf(0.95, dataDof)*dataStd); #yerr=stdData_[i]
                plots.append(plot);

            else:
                plot = ax.bar(xLocations+i*barWidth_, medians, barWidth_, color=colorCode, yerr=scipy.stats.t.ppf(0.95, dataDof)*dataStd); #yerr=stdData_[i]
                plots.append(plot);

        else:
            maxVal = crData.getMaxValueInAList(data_[i]);
            minVal = crData.getMinValueInAList(data_[i]);
            plot = ax.bar(xLocations+i*barWidth_, data_[i], barWidth_, color=colorCode); #yerr=stdData_[i]
            plots.append(plot);

    setFigureAxisLimits(ax, minVal, maxVal, xMin_, xMax_, yMin_, yMax_, yTicksStep_, yTicksStepMultiplier_);

    #-- plot line for y=0
    #pylab.plot(numpy.linspace(-0.1,N-1+0.8,3),[0,0,0],'k-');

    #-- setup legend
    #box = ax.get_position()
    #legendItems = [];
    #for g in range(len(plots)):
    #    legendItems.append(plots[g][0]);

    #-- show legend
    if (len(legendLabels_) > 0):
        def flip(items, ncol):
            return itertools.chain(*[items[i::ncol] for i in range(ncol)])

        legendItems = [];
        for g in range(len(plots)):
            legendItems.append(plots[g][0]);
        legend = ax.legend(flip(legendItems, numOfLegendColumns_), flip(legendLabels_,numOfLegendColumns_),loc=legendPosition_.value, ncol=numOfLegendColumns_)
        for t in legend.get_texts():
            if (type(legendFontSize_) == str):
                t.set_fontsize(legendFontSize_)
            else:
                font = math.QFont(t.font());
                font.setPointSize(legendFontSize_);
                t.setFont(font);


    #-- display / print, return:
    renderFigure(filePath_, renderFigure_);
    return fig;

#--------------------------------------------------------------------------------------------------------- Line plot

def createLinePlot(data_,
                title_="", xLabel_ = "", yLabel_ = "", xTickLabels_=[], legendLabels_ = [], numOfLegendColumns_ = 2, legendPosition_=LEGEND_POSITION.BEST, markers_ = [], colors_ = [],
                showBoxPlots_=False, boxPlotWidth_=-1, showConfidenceIntervals_=False, showAverages_=False, doWilcoxon_=False,
                lineWidth_ = 2, lineStyles_ = [], markerSize_=10, gridType_=GRID_TYPE.FULL,
                xMin_=INVALID_VALUE, xMax_=INVALID_VALUE, xAxisGroupSize_ = 0, yMin_=INVALID_VALUE, yMax_=INVALID_VALUE, yTicksStep_ = 0, yTicksStepMultiplier_ = 1,
                titleFontSize_=INVALID_VALUE, labelFontSize_ = INVALID_VALUE, tickFontSize_ = INVALID_VALUE, legendFontSize_ = INVALID_VALUE, size_=(12,6),
                filePath_ = "", renderFigure_=True, figure_=None, subPlot_=111):

    """

    Create one of a plot with a single or multiple lines. Optionally, each data point can have error bars or box plots around it.

    Minimal example:

    .. code-block:: python

        profitData = [
                [1, 2, 4, 3, 6, 8]
        ];

        crGraphs.createLinePlot(profitData);

    :param `data_`: A 2D or a 3D list of numbers. The 0th dimension represents individual lines. The 1st dimension represents data points on the line, ordered by x coordinate. Optional 3rd dimension is a list of values that each data point consists of. A data point is then a median of that list
    :param `title_`: (optional, default = "") The figure title
    :param `xLabel_`: (optional, default = "") Label of the x-axis
    :param `yLabel_`: (optional, default = "") Label of the y-axis
    :param `xTickLabels_`: (optional, default = []) A 1D list of tick labels for the x-axis. Must be the same length as the 1st dimension of `data_`, i.e., each data point must have a corresponding `xTickLabel`
    :param `legendLabels_`: (optional, default = []) A 1D list of labels for the individual plot lines. Must be the same length as the 0th dimension of `data_`, i.e., each plot line must have a corresponding `legendLabel`
    :param `numOfLegendColumns_`: (optional, default = 2) A int number of columns in the legend
    :param `legendPosition_`: (optional, default = `LEGEND_POSITION.BEST`) A :class:`.LEGEND_POSITION` enum member
    :param `markers_`: (optional, default = []) A 1D list of markers for the plot lines. If a corresponding marker for a plot line is not specified, a marker from `DEFAULT_MARKERS` is used
    :param `colors_`: (optional, default = []) A 1D list of colors for the plot lines. If a corresponding color for a plot line is not specified, a marker color is used
    :param `showBoxPlots_`: (optional, default = False) A boolean that specified whether to show box plots around data points. If True, `data_` must be a 3D list
    :param `boxPlotWidth_`: (optional, default = -1) A float that specified width of each box plot. If -1, box plot width is calculated automatically
    :param `showConfidenceIntervals_`: (optional, default = False) A boolean that specified whether to error bars around data points. If True, `data_` must be a 3D list
    :param `showAverages_`: (optional, default = False) A boolean that specifies whether to show averages instead of medians as data points. If True, `data_` must be a 3D list
    :param `doWilcoxon_`: (optional, default = False) A boolean that specified whether to perform `Wilcoxon signed-rank test <http://en.wikipedia.org/wiki/Wilcoxon_signed-rank_test>`_ between 2 plot lines. If True, the \* notation is used next to a tick label on the x-axis where there is significant difference with p=0.05. The \*\* notation is used when there is a significant different with p=0.01. This test can only be performed when `data_` has length of 2 and is a 3D list, i.e., if it containts data for 2 plot lines and each data point represents a list of values
    :param `lineWidth_`: (optional, default = 2) Width of the plot lines.
    :param `lineStyles_`: (optional, default = []) A 1D list of line styles for the plot lines. If a corresponding style for a plot line is not specified, a solid line is displayed
    :param `markerSize_`: (optional, default = 10) Size of the plot markers
    :param `gridType_`: (optional, default = `GRID_TYPE.FULL`) A :class:`.GRID_TYPE` enum member
    :param `xMin_`: (optional, default = `INVALID_VALUE`) Minimum value shown on the x-axis. If set to `INVALID_VALUE`, x-axis is displayed to fit the data
    :param `xMax_`: (optional, default = `INVALID_VALUE`) Maximum value shown on the x-axis. If set to `INVALID_VALUE`, x-axis is displayed to fit the data
    :param `xAxisGroupSize_`: (optional, default = 0) The number of data points that are joined by lines when they are next to each other on the x-axis. If set to 0, all data points are joined together. If set to > 0, groups of data points appear, with no joining lines between data points from different groups.
    :param `yMin_`: (optional, default = `INVALID_VALUE`) Minimum value shown on the y-axis. If set to `INVALID_VALUE`, y-axis is displayed to fit the data
    :param `yMax_`: (optional, default = `INVALID_VALUE`) Maximum value shown on the y-axis. If set to `INVALID_VALUE`, y-axis is displayed to fit the data
    :param `yTicksStep_`: (optional, default = 0) A number that represents the different between each tick on the y-axis. If set to 0, y-axis is displayed to fit the data
    :param `yTicksStepMultiplier_`: (optional default = 1) A number by which each tick on the y axis is multiplied by.
    :param `titleFontSize_`: (optional, default = TITLE_FONT_SIZE) Font size of the title
    :param `labelFontSize_`: (optional, default = LABEL_FONT_SIZE) Font size of the axis and color bar labels
    :param `tickFontSize_`: (optional, default = TICK_FONT_SIZE) Font size of axis ticks and of values inside the plot
    :param `legendFontSize_`: (optional, default = LABEL_FONT_SIZE) Font size of the legend
    :param `size_`: (optional, default = (8,6)) The figure size
    :param `filePath_`: (optional, default = "") If not empty, the figure will be saved to the file path specified. If empty, the figure will be displayed on screen instead.
    :param `renderFigure_`: (optional, default = True) If false, the figure will not be displayed or printed. Set to False when putting multiple figures together via the `figure_` parameter.
    :param `figure_`: (optional, default = None) If not None, the figure will be created into this figure (pylab.figure)
    :param `subPlot_`: (optional, default = 111) The subplot id of where to place the graph to

    :return: `pylab.figure` for the plot

    """

    #-- test and pre-set data
    numOfDataDimensions = crData.getNumberOfListDimensions(data_);
    if (numOfDataDimensions < 2 or numOfDataDimensions > 3):
        raise ValueError("The data_ parameter must be a 2D or a 3D list.")

    xTickLabels = xTickLabels_.copy();
    if (len(xTickLabels) == 0):
        xTickLabels = range(len(data_[0]));

    crHelpers.checkListsHaveTheSameLength(data_[0], xTickLabels);

    if (len(legendLabels_) > 0):
        crHelpers.checkListsHaveTheSameLength(data_, legendLabels_);

    crHelpers.checkVariableDataType(legendPosition_, LEGEND_POSITION);
    crHelpers.checkVariableDataType(gridType_, GRID_TYPE);

    titleFontSize_ = replaceInvalidWithDefaultValue(titleFontSize_, TITLE_FONT_SIZE)
    labelFontSize_ = replaceInvalidWithDefaultValue(labelFontSize_, LABEL_FONT_SIZE);
    tickFontSize_ = replaceInvalidWithDefaultValue(tickFontSize_, TICK_FONT_SIZE);
    legendFontSize_ = replaceInvalidWithDefaultValue(legendFontSize_, LABEL_FONT_SIZE);

    if (showAverages_):
        showBoxPlots_ = False;
        showConfidenceIntervals_ = False;

    if (doWilcoxon_):
        if (len(data_) != 2):
            doWilcoxon_ = False;
            print ("!!! Cannot perform Wilcoxon signed-rank test between more than 2 plot lines, i.e., the size of data_ must be 2.");
        elif (numOfDataDimensions < 3):
            doWilcoxon_ = False;
            print ("!!! Cannot perform Wilcoxon signed-rank test: each plot's data point represented by data_ must be a list, i.e., data_ must be a 3D list.");

    if (showBoxPlots_ and numOfDataDimensions < 3):
        print ("!!! Cannot draw box plots: each plot's data point represented by data_ must be a list, i.e., data_ must be a 3D list.");
    if (showConfidenceIntervals_ and numOfDataDimensions < 3):
        print ("!!! Cannot draw confidence intervals: each plot's data point represented by data_ must be a list, i.e., data_ must be a 3D list.");
    if (showAverages_ and numOfDataDimensions < 3):
        print ("!!! Cannot show averages: each plot's data point represented by data_ must be a list, i.e., data_ must be a 3D list.");



    #-- create the figure
    fig, ax = createFigure(size_, title_, figure_, subPlot_, xLabel_, yLabel_, titleFontSize_, labelFontSize_, tickFontSize_, 1.2, 1.05);

    #-- prepare x tick data, which has to be scalars
    xTickData = [];
    if (type(xTickLabels) == int):
        #-- xTickLabels are numbers, ok to use for plotting
        xTickData = xTickLabels;
    else:
        #-- xTickLabels are strings, the xTickData must be an array from 0-length of xTickLabels
        xTickData = range(len(xTickLabels));


    #-- prepare box plot width
    if ((showBoxPlots_ and boxPlotWidth_ <= 0) or showConfidenceIntervals_):
        boxPlotWidth_ = abs(xTickData[-1] - xTickData[0]) / 20.0;


    #-- do the potting
    plots = [];
    maxVal = -9999999;
    minVal = 9999999;
    for i in range(len(data_)):

        if (DEBUG_LEVEL >= 1): print("[crData] processing data row {}".format(i))

        legendLabel = " ";
        #-- choose a legend label
        if (len(legendLabels_) > i):
            legendLabel = legendLabels_[i];

        #-- choose a marker
        marker = DEFAULT_MARKERS[0];
        if (len(markers_) > i):
            marker = markers_[i];
        elif (len(DEFAULT_MARKERS) > i):
            marker = DEFAULT_MARKERS[i];

        #-- choose a color, default to marker color
        color = marker[0:1];
        if (len(colors_) > i):
            color = colors_[i];

        lineStyle = '-';
        if (len(lineStyles_) > i):
            lineStyle = lineStyles_[i];
        elif (lineWidth_ == 0):
            lineStyle = '';

        #-- apply custom x tick labels
        if (len(xTickLabels) > 0):
            plt.xticks(xTickData, xTickLabels);

        #-- find out how many line segments
        numOfSegments = 0;
        lineSegmentLength = xAxisGroupSize_;
        if (xAxisGroupSize_ > 0 and xAxisGroupSize_ <= len(xTickData)):
            numOfSegments = int(math.ceil(len(xTickData) / xAxisGroupSize_));
        else:
            numOfSegments = 1;
            lineSegmentLength = len(xTickData);

        #-- plot
        if (numOfDataDimensions == 3):
            #-- each element for a single data point is a list.
            #-- only plot median of data that is a list. Box plots can be added later if set
            #-- get medians one by one, as numpy can't deal with lists of different lengths
            dataPoints = [];
            for q in range(len(data_[i])):
                if (showAverages_):
                    dataPoints.append(numpy.mean(data_[i][q]));
                else:
                    dataPoints.append(numpy.median(data_[i][q]));
                if (doWilcoxon_ and i == 1):
                    #-- do the Wilcoxon test on individual samples (that together form a median) and compare them to runs of previous data set:
                    pVal = scipy.stats.wilcoxon(data_[i][q],data_[0][q])[1];
                    if (pVal < 0.01):
                        xTickLabels[q] = str(xTickLabels[q]) + "**";
                    elif (pVal < 0.05):
                        xTickLabels[q] = str(xTickLabels[q]) + "*";

                for r in range(len(data_[i][q])):
                    if (data_[i][q][r] > maxVal):
                        maxVal = data_[i][q][r];
                    if (data_[i][q][r] < minVal):
                        minVal = data_[i][q][r]

            if (showConfidenceIntervals_):
                dataDof = [(len(data_[i][q])-1) for q in range(len(dataPoints))]; #degrees of freedom is sample size -1
                dataStd = [numpy.std(data_[i][q]) for q in range(len(dataPoints))];
                (_, caps, _) = plt.errorbar(xTickData, dataPoints, yerr=scipy.stats.t.ppf(0.95, dataDof)*dataStd, color=color, linewidth=0, elinewidth=lineWidth_, capsize=markerSize_-2, linestyle=lineStyle);
                for cap in caps:
                    if (lineWidth_ == 0):
                        cap.set_markeredgewidth(3);
                    else:
                        cap.set_markeredgewidth(lineWidth_);

            #-- draw, in line segments
            for seg in range(numOfSegments):
                segStart = seg * lineSegmentLength;
                segEnd = segStart + lineSegmentLength;
                if (segEnd > len(xTickData)):
                    segEnd = len(xTickData-1);
                plot = pylab.plot(xTickData[segStart:segEnd], dataPoints[segStart:segEnd], marker, color=color, label = legendLabel, linewidth=lineWidth_, linestyle=lineStyle, markersize=markerSize_);

        else:
            #-- each element for a single data point is a single number. Plot directly from these numbers.

            maxVal = crData.getMaxValueInAList(data_[i]);
            minVal = crData.getMinValueInAList(data_[i]);

            #-- draw, in line segments
            for seg in range(numOfSegments):
                segStart = seg * lineSegmentLength;
                segEnd = segStart + lineSegmentLength;
                if (segEnd > len(xTickData)):
                    segEnd = len(xTickData-1);

                plot = pylab.plot(xTickData[segStart:segEnd], data_[i][segStart:segEnd], marker, color=color, label = legendLabel, linewidth=lineWidth_, linestyle=lineStyle, markersize=markerSize_);

        plots.append(plot);

        #-- do box plots
        if (showBoxPlots_):
            boxPlot = pylab.boxplot(data_[i],positions=xTickData,widths=boxPlotWidth_);
            boxPlotLineWidth = min(lineWidth_,2);

            pylab.setp(boxPlot['boxes'], color=color);
            pylab.setp(boxPlot['whiskers'], color=color);
            pylab.setp(boxPlot['medians'], color=color);
            pylab.setp(boxPlot['fliers'], markeredgecolor=color, marker="+", markerSize = max(6,markerSize_*0.7),markerEdgeWidth=max(1,boxPlotLineWidth));
            pylab.setp(boxPlot['caps'], color=color);


            if (boxPlotLineWidth <= 0):
                boxPlotLineWidth = 1;

            for box in boxPlot['boxes']:
                box.set(linewidth=boxPlotLineWidth)
            for median in boxPlot['medians']:
                median.set(linewidth=boxPlotLineWidth)
            for cap in boxPlot['caps']:
                cap.set(linewidth=boxPlotLineWidth)
            for cap in boxPlot['whiskers']:
                cap.set(linewidth=boxPlotLineWidth)

            #-- reapply x ticks labels
            ax.set_xticklabels(xTickLabels);


    #-- grid
    if (gridType_ != GRID_TYPE.NONE):
        gridAxis = 'both';
        gridWhich = 'both';
        if (gridType_ == GRID_TYPE.HORIZONTAL or gridType_ == GRID_TYPE.MAJOR_HORIZONTAL or gridType_ == GRID_TYPE.MINOR_HORIZONTAL):
            gridAxis = 'y';
        elif (gridType_ == GRID_TYPE.VERTICAL or gridType_ == GRID_TYPE.MAJOR_VERTICAL or gridType_ == GRID_TYPE.MAJOR_VERTICAL):
            gridAxis = 'x';

        if (gridType_ == GRID_TYPE.MAJOR or gridType_ == GRID_TYPE.MAJOR_HORIZONTAL or gridType_ == GRID_TYPE.MAJOR_VERTICAL):
            gridWhich = 'major';
        elif (gridType_ == GRID_TYPE.MINOR or gridType_ == GRID_TYPE.MINOR_HORIZONTAL or gridType_ == GRID_TYPE.MINOR_VERTICAL):
            gridWhich = 'minor';

        ax.grid(which=gridWhich, axis=gridAxis, linestyle=":");

    #-- adjust x axis and y axis limits:
    if (showBoxPlots_ or showConfidenceIntervals_):
        #-- make space for box plots
        ax.set_xlim(xTickData[0]-2*boxPlotWidth_/3.0,xTickData[-1]+2*boxPlotWidth_/3.0);
    else:
        #-- make a little space
        ax.set_xlim(xTickData[0]-xTickData[-1]*0.01,xTickData[-1]+xTickData[-1]*0.01);

    if (DEBUG_LEVEL>=1): print("[crData] min data value={}    max data value={}".format(minVal,maxVal))
    setFigureAxisLimits(ax, minVal, maxVal, xMin_, xMax_, yMin_, yMax_, yTicksStep_, yTicksStepMultiplier_);

    #-- show legend
    if (len(legendLabels_) > 0):
        def flip(items, ncol):
            return itertools.chain(*[items[i::ncol] for i in range(ncol)])

        legendItems = [];
        for g in range(len(plots)):
            legendItems.append(plots[g][0]);
        legend = ax.legend(flip(legendItems, numOfLegendColumns_), flip(legendLabels_,numOfLegendColumns_),loc=legendPosition_.value, ncol=numOfLegendColumns_)
        for t in legend.get_texts():
            if (type(legendFontSize_) == str):
                t.set_fontsize(legendFontSize_)
            else:
                font = math.QFont(t.font());
                font.setPointSize(legendFontSize_);
                t.setFont(font);


    #-- display / print, return:
    renderFigure(filePath_, renderFigure_);
    return fig;


#--------------------------------------------------------------------------------------------------------- Matrix plot

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
    :param `xLabel_`: (optional, default = "") Label of the x-axis
    :param `yLabel_`: (optional, default = "") Label of the y-axis
    :param `xTickLabels_`: (optional, default = []) Labels of the individual ticks of the x-axis. If empty, values 0-N are displayed
    :param `yTickLabels_`: (optional, default = []) Labels of the individual ticks of the y-axis. If empty, values 0-N are displayed
    :param `colorBarLabel_`: (optional, default = "") Label of color bar, displayed vertically
    :param `colorMap_`: (optional, default = "summer") A python.colormap isntance to use for the matrix plot
    :param `minValue_`: (optional, default = `INVALID_VALUE`) Minimum float value that the color map considers. If set to INVALID_VALUE, the value is automatically calculated from `data_`
    :param `maxValue_`: (optional, default = `INVALID_VALUE`) Maximum float value that the color map considers. If set to INVALID_VALUE, the value is automatically calculated from `data_`
    :param `annotateValues_`: (optional, default = False) If True, data values will be displayed in the matrix plot
    :param `annotationStringAfter_`: (optional, default = "") A string to append after each annotation value
    :param `annotationValues_`: (optional, default = [[],[]]) A 2D list of annotations in the matrix plot. If non-empty, must have the same dimensions as `data_`
    :param `roundAnnotatedValues_`: (optional, default = False) If True and if `annotationValues_` is empty, annotation numbers will be rounded
    :param `titleFontSize_`: (optional, default = TITLE_FONT_SIZE) Font size of the title
    :param `labelFontSize_`: (optional, default = LABEL_FONT_SIZE) Font size of the axis and color bar labels
    :param `tickFontSize_`: (optional, default = TICK_FONT_SIZE) Font size of axis ticks and of values inside the plot
    :param `size_`: (optional, default = (8,6)) The figure size
    :param `filePath_`: (optional, default = "") If not empty, the figure will be saved to the file path specified. If empty, the figure will be displayed on screen instead.
    :param `renderFigure_`: (optional, default = True) If false, the figure will not be displayed or printed. Set to False when putting multiple figures together via the `figure_` parameter.
    :param `figure_`: (optional, default = None) If not None, the figure will be created into this figure (pylab.figure)
    :param `subPlot_`: (optional, default = 111) The subplot id of where to place the graph to

    :return: `pylab.figure` for the plot
    """


    #-- test and pre-set data
    crHelpers.checkVariableIsList(data_,2,True);
    crHelpers.checkVariableIsList(xTickLabels_);
    crHelpers.checkVariableIsList(yTickLabels_);
    crHelpers.checkVariableIsList(annotationValues_,2);

    if (len(xTickLabels_) > 0):
        crHelpers.checkListsHaveTheSameLength(data_[1], xTickLabels_);
    if (len(yTickLabels_) > 0):
        crHelpers.checkListsHaveTheSameLength(data_, yTickLabels_);

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

#--------------------------------------------------------------------------------------------------------- Pie chart

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

    :return: `pylab.figure` for the plot
    """

    #-- test and pre-set data
    crHelpers.checkVariableIsList(data_,1,True);
    crHelpers.checkVariableIsList(itemLabels_,True);
    crHelpers.checkVariableIsList(itemColors_);

    crHelpers.checkListsHaveTheSameLength(data_, itemLabels_);

    if (len(itemColors_) > 0):
        crHelpers.checkListsHaveTheSameLength(data_, itemColors_);

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

            #-- create directories recursively if they don't exist
            directoryPath = filePath_.rsplit('/', 1)[0]
            os.makedirs(directoryPath,exist_ok=True)

            #--
            pylab.savefig(filePath_, format='png')
            if (SHOW_OUTPUT == True):
                print("[crData] Saved " + filePath_);
        else:
            pylab.show()



def createFigure(size_, title_="", figure_=None, subPlot_=111,
                xLabel_="", yLabel_="",
                titleFontSize_=INVALID_VALUE, labelFontSize_=INVALID_VALUE, tickFontSize_=INVALID_VALUE,
                xStretchMultiply_=1.2, yStretchMultiply_=1.2):
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
    :param `xStretchMultiply_`: (optional, default = 1.2) By how much to stretch the plot inside the figure in x direction. Enter 1.0 to leave the plot as is.
    :param `yStretchMultiply_`: (optional, default = 1.2) By how much to stretch the plot inside the figure in y direction. Enter 1.0 to leave the plot as is.

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

    #-- specify title, stretch the plot
    xStretchMultiply_ = xStretchMultiply_-1;
    yStretchMultiply_ = yStretchMultiply_-1;
    if (title_ != ""):
        fig.suptitle(title_, fontsize=titleFontSize_);
        yStretchMultiply_ -= 0.1;

    if (xLabel_ != ""):
        yStretchMultiply_ -= 0.1;
    if (yLabel_ != ""):
        xStretchMultiply_ -= 0.1;

    box = ax.get_position();
    ax.set_position([box.x0 - box.width * (xStretchMultiply_/2), box.y0 - box.height*yStretchMultiply_/2, box.width*(1+xStretchMultiply_), box.height*(1+yStretchMultiply_)]);


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


def setFigureAxisLimits(ax_, minDataValue_, maxDataValue_, xMin_=INVALID_VALUE, xMax_=INVALID_VALUE, yMin_=INVALID_VALUE, yMax_=INVALID_VALUE, yTicksStep_ = 0, yTicksStepMultiplier_ = 1):

    #-- recursively find the correct yTickStep based on the max value. The yTickStep should fit N times into maxDataValue_.
    #   then annotate the y axis.
    if (yTicksStep_ <= 0):
        yTicksStep_ = 0.00001;
        stop = False;
        while (stop == False):
            if (maxDataValue_ / yTicksStep_ <= 20):
                stop = True;
            else:
                yTicksStep_ *= 10;

    #-- determine the y span of data
    dataRange = maxDataValue_ - minDataValue_;
    plotYMin = minDataValue_ - dataRange*0.1;
    plotYMax = maxDataValue_ + dataRange*0.1;

    #-- round to the closest multiply of N, where N fits yTickStep
    plotYMin = plotYMin - (plotYMin%yTicksStep_);

    if (xMin_ > INVALID_VALUE and xMax_ > INVALID_VALUE):
        ax_.set_xlim(xMin_, xMax_);

    if (yMin_ != INVALID_VALUE):
        plotYMin = yMin_;
    if (yMax_ != INVALID_VALUE):
        plotYMax = yMax_;

    ax_.set_ylim(plotYMin, plotYMax);

    ticks = [];
    ticksLabels = [];

    start = plotYMin;
    stop = plotYMax;

    if (yMin_ == - yMax_*0.05):
        start = 0;

    ticks = numpy.arange(start, stop + yTicksStep_, yTicksStep_);
    ax_.set_yticks(ticks);

    if (yTicksStepMultiplier_ != 1):
        for t in range(len(ticks)):
            ticksLabels.append(ticks[t] * yTicksStepMultiplier_);
        ax_.set_yticklabels(ticksLabels);
        ticks = ticksLabels;

    ticksLabels = [];
    for t in range(len(ticks)):
        intVal = int(ticks[t]);
        if (abs(intVal) >= 1000):
            ticksLabels.append("{}k".format( intVal / 1000));
        else:
            ticksLabels.append(ticks[t]);

    ax_.set_yticklabels(ticksLabels);



def getBrokenLinePlotParameters(yMin_, brokenLineY_, yMax_, brokenLinePlotHeightPercentage_ = 60):
    """
    Get y-axis parameters of two plots, bottom and top, that can be combined together into a broken line plot.

    :param yMin_:  Minimum value shown on the y-axis.
    :param brokenLineY_: Y-axis value at which the broken line will be drawn
    :param yMax_: Maximum value shown on the y-axis.
    :param brokenLinePlotHeightPercentage_: (optional, default = 60) The percentage (20-80) of the plot's height at which the broken line will be drawn

    :return: (bottom plot y min,  bottom plot y max, top plot y min, top plot y max)
    """
    crHelpers.checkVariableGreaterThanAnother(brokenLineY_,yMin_);
    crHelpers.checkVariableGreaterThanAnother(yMax_,yMin_);
    crHelpers.checkVariableGreaterThanAnother(yMax_,brokenLineY_);
    crHelpers.checkVariableBetweenValues(brokenLinePlotHeightPercentage_,20,80);

    brokenLinePlotHeightMultiplier = brokenLinePlotHeightPercentage_ / 100.0;

    zoomedInPlotRange = brokenLineY_ - yMin_;
    finalPlotRange = yMax_ - yMin_;
    zoomedInPlotYMax =  zoomedInPlotRange * 1/brokenLinePlotHeightMultiplier; # the broken line breaks at N% of the figure height
    zoomedOutPlotYMin = yMax_ - ((finalPlotRange - brokenLineY_) * (1/(1-brokenLinePlotHeightMultiplier)))

    return (yMin_, zoomedInPlotYMax, zoomedOutPlotYMin, yMax_);




