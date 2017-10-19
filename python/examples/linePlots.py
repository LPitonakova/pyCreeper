from numpy import random;
from python.pyCreeper import crGraphs;
crGraphs.BASE_FILE_PATH = "../../exampleOutput/";

def example1_simple(saveFiles_):
    """
    In this example, a single-line plot is created:

    .. image:: ../exampleOutput/linePlot_simple.png
        :scale: 50%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """

    profitData = [
                [10, 25, 40, 32, 60, 85, 75, 55, 70]
    ];

    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"];

    filePath = "";
    if (saveFiles_):
        filePath = "linePlot_simple.png";
    crGraphs.createLinePlot(profitData, "Profit so far this year", xTickLabels_=months, xLabel_="Month", yLabel_="Profit (mil. £)", yMin_=0, yMax_=100, filePath_=filePath);

def example2_multiple(saveFiles_):
    """
    In this example, a multi-line plot is created and its custom colours and markers are specified.

    .. image:: ../exampleOutput/linePlot_multi.png
        :scale: 50%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """

    profitData = [
                [9,  20, 30, 20, 35, 55, 40, 20, 30],
                [1,  5,  10, 12, 25, 30, 35, 35, 40],
                [10, 25, 40, 32, 60, 85, 75, 55, 70],

    ];

    legendLabels = ['Customer sales', 'Stocks', 'Total profit'];
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"];

    filePath = "";
    if (saveFiles_):
        filePath = "linePlot_multi.png";
    crGraphs.createLinePlot(profitData, "Profit so far this year", xTickLabels_=months, xLabel_="Month", yLabel_="Profit (mil. £)", yMin_=0, yMax_=100,
                            markers_ = ['o','o','s'], colors_=['g','c','r'], legendLabels_=legendLabels, filePath_=filePath);


def example3_errorBars(saveFiles_):
    """
    In this example, a multi-line plot with error bars is created, with horizontal-only grid shown and with
    data points connected together based on which year quarter they belong to:

    .. image:: ../exampleOutput/linePlot_errorBars2.png
        :scale: 50%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """

    profitData = [
                [9,  20, 30, 20, 35, 55, 40, 20, 30],
                [1,  5,  10, 12, 25, 30, 35, 35, 40],
                [10, 25, 40, 32, 60, 85, 75, 55, 70]
    ];
    #-- change each data point above to become a list with a normal distribution instead, with median of profitData[i][j]
    profitData = [ [ list(random.standard_normal(3)*5 + profitData[i][j]) for j in range(len(profitData[i])) ] for i in range(len(profitData))];

    legendLabels = ['Customer sales', 'Stocks', 'Total profit'];
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"];

    filePath = "";
    if (saveFiles_):
        filePath = "linePlot_errorBars.png";
    crGraphs.createLinePlot(profitData, "Profit so far this year", xTickLabels_=months, xLabel_="Month", yLabel_="Profit (mil. £)", yMin_=-20, yMax_=120,
                            markers_ = ['o','o','s'], colors_=['g','c','r'], legendLabels_=legendLabels, showConfidenceIntervals_=True, xAxisGroupSize_=3,
                            numOfLegendColumns_=3, legendPosition_=crGraphs.LEGEND_POSITION.UPPER_LEFT, gridType_=crGraphs.GRID_TYPE.HORIZONTAL,
                            filePath_=filePath);

def example4_boxPlots(saveFiles_):
    """
    In this example, a multi-line plot with box plots is created, without the grid or data point
    connections shown.

    Also, a Willcoxon test is performed find out data points with significant differences between them.
    A \* notation is used next to a month where there is significant difference with p=0.05.
    A \*\* notation is used when there is a significant different with p=0.01.

    .. image:: ../exampleOutput/linePlot_boxPlots2.png
        :scale: 50%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """

    profitData = [
                [9,  20, 30, 20, 35, 55, 40, 20, 30],
                [1,  20, 28.5, 12, 25, 53.5, 35, 35, 40]
    ];
    #-- change each data point above to become a list with a normal distribution instead, with median of profitData[i][j]
    profitData = [ [ list(random.standard_normal(20)*2 + profitData[i][j]) for j in range(len(profitData[i])) ] for i in range(len(profitData))];

    legendLabels = ['Customer sales', 'Stocks'];
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"];

    filePath = "";
    if (saveFiles_):
        filePath = "linePlot_boxPlots.png";
    crGraphs.createLinePlot(profitData, "Profit so far this year", xTickLabels_=months, xLabel_="Month", yLabel_="Profit (mil. £)", yMin_=0, yMax_=80,
                            markers_ = ['s','s'], colors_=['g','r'], legendLabels_=legendLabels, showBoxPlots_=True, lineWidth_=0, gridType_=crGraphs.GRID_TYPE.NONE, doWilcoxon_=True,
                            filePath_=filePath);


if __name__ == "__main__":

    saveFiles = True;

    example1_simple(saveFiles);
    example2_multiple(saveFiles);
    example3_errorBars(saveFiles);
    example4_boxPlots(saveFiles);


