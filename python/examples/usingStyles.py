from numpy import random;
from python.pyCreeper import crGraphs;
from python.pyCreeper import crGraphStyle;

crGraphs.BASE_FILE_PATH = "../../exampleOutput/";


def example():
    """
    In this example, figures for the "Using Styles" page are created.
    """

    profitData = [
                [9,  20, 30, 20, 35, 55, 40, 20, 30],
                [1,  5,  10, 12, 25, 30, 35, 35, 40],
                [10, 25, 40, 32, 60, 85, 75, 55, 70],

    ];

    legendLabels = ['Customer sales', 'Stocks', 'Total profit'];
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"];

    crGraphs.createLinePlot(profitData, "Profit so far this year", xTickLabels_=months, xLabel_="Month", yLabel_="Profit (mil. £)", yMin_=0, yMax_=100, legendLabels_=legendLabels, filePath_="usingStyles_noStyle.png");

    style = crGraphStyle.crGraphStyle();
    style.markers = ['o','d','s'];
    style.colors = ['g','c','r'];
    style.titleFontSize = 40;
    style.numOfLegendColumns = 1;
    style.gridType = crGraphStyle.GRID_TYPE.MAJOR_HORIZONTAL;
    crGraphs.setStyle(style);

    crGraphs.createLinePlot(profitData, "Profit so far this year", xTickLabels_=months, xLabel_="Month", yLabel_="Profit (mil. £)", yMin_=0, yMax_=100, legendLabels_=legendLabels, filePath_="usingStyles_style.png");




if __name__ == "__main__":

    saveFiles = True;

    example();


