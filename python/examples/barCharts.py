from numpy import random;
from python.pyCreeper import crGraphs;
crGraphs.BASE_FILE_PATH = "../../exampleOutput/";


def example1_simple(saveFiles_):
    """
    In this example, a simple bar chart is created:

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
        filePath = "barChart_simple.png";
    crGraphs.createBarChart(profitData, "Profit so far this year", xTickLabels_=months, xLabel_="Month", yLabel_="Profit (mil. £)", yMin_=0, yMax_=100, filePath_=filePath);

def example2_multiple(saveFiles_):
    """
    In this example, a bar chart with multiple bar groups is created and their custom colors are specified:

    .. image:: ../exampleOutput/linePlot_simple.png
        :scale: 50%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """

def example3_errorBars(saveFiles_):
    """
    In this example, a bar chart with multiple bar groups and error bars is created:

    .. image:: ../exampleOutput/linePlot_simple.png
        :scale: 50%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """

if __name__ == "__main__":

    saveFiles = False;

    example1_simple(saveFiles);