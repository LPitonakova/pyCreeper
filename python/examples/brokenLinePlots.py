from numpy import random;
from python.pyCreeper import crGraphs;

crGraphs.BASE_FILE_PATH = "../../exampleOutput/";


def example(saveFiles_):
    """
    In this example, plot images for a broken line plot are created:

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """

    data = [
        [10, 12, 25, 32, 25, 57, 44, 54, 62, 60, 44, 35, 51, 62, 84, 280, 305, 312, 309, 323],
    ];

    data = [ [ list(random.standard_normal(10)*2*j + data[i][j]) for j in range(len(data[i])) ] for i in range(len(data))];

    filePathStandardPlot = "";
    filePathBottomPlot = "";
    filePathTopPlot = "";
    if (saveFiles_):
        filePathStandardPlot = "brokenLinePlot_standard.png"
        filePathBottomPlot = "brokenLinePlot_bottom.png";
        filePathTopPlot = "brokenLinePlot_top.png"


    #-- get plot parameters for the zoomed in and zoomed out plots
    yMinStandardPlot = 0; # y min of a plot that would normally be drawn for all data
    yMaxStandardPlot = 400; # y max of a plot that would normally be drawn for all data
    brokenLineYCoordinate = 100; # y value at which broken line will be drawn. This value separates the two "zoomedIn" and "zoomedOut" plots
    brokenLineHeightPercentage = 50; # percentage of the plot height at which the broken line will be drawn

    yMinBottomPlot, yMaxBottomPlot, yMinTopPlot, yMaxTopPlot = crGraphs.getBrokenLinePlotParameters(yMinStandardPlot, brokenLineYCoordinate, yMaxStandardPlot, brokenLineHeightPercentage);

    #-- create the two plots as two separate files, using the y-axis parameters from above
    xTickLabels = [(g+1) for g in range(len(data[0]))];

    crGraphs.createLinePlot(data, "Population fitness", xTickLabels_=xTickLabels, xLabel_="Generation", yLabel_="Fitness", yMin_=yMinBottomPlot, yMax_=yMaxBottomPlot,
                            yTicksStep_=20, showBoxPlots_=True, lineWidth_=2, filePath_=filePathBottomPlot);
    crGraphs.createLinePlot(data, "Population fitness", xTickLabels_=xTickLabels, xLabel_="Generation", yLabel_="Fitness", yMin_=yMinTopPlot, yMax_=yMaxTopPlot,
                            showBoxPlots_=True, lineWidth_=2, filePath_=filePathTopPlot);


    #-- also create a standard plot for demonstration:
    crGraphs.createLinePlot(data, "Population fitness", xTickLabels_=xTickLabels, xLabel_="Generation", yLabel_="Fitness", yMin_=yMinStandardPlot, yMax_=yMaxStandardPlot,
                            showBoxPlots_=True, lineWidth_=2, filePath_=filePathStandardPlot);

if __name__ == "__main__":

    saveFiles = True;

    example(saveFiles);


