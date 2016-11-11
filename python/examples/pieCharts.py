from python.pyCreeper import crGraphs;


def doSimpleExample(saveFiles_):
    """
    In this example, a simple pie chart is created:

    .. image:: ../python/examples/pieChart_simple.png
        :scale: 50%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """
    expenseCategories = ["Rent", "Food", "Travel", "Fun"];
    expenses = [1000, 300, 500, 250];

    filePath = "";
    if (saveFiles_):
        filePath = "pieChart_simple.png";
    crGraphs.createPieChart(expenses, expenseCategories,filePath_=filePath);

def doColorsExample(saveFiles_):
    """
    In this example, the title, colors and font sizes are specified. Percentage values and actual values are also shown:

    .. image:: ../python/examples/pieChart_colors.png
        :scale: 50%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """
    expenseCategories = ["Rent", "Food", "Travel", "Fun"];
    expenses = [1000, 300, 500, 250];
    colors = ['yellow','cyan','grey','white']

    filePath = "";
    if (saveFiles_):
        filePath = "pieChart_colors.png";
    crGraphs.createPieChart(expenses, expenseCategories, colors, title_="Colors example", showPercentageVals_=True, showShadow_=True, filePath_=filePath);

def doMultiFigurePrintExample(saveFiles_):
    """
    In this example, 2 figures are created below each other and saved into a single file:

    .. image:: ../python/examples/pieChart_large.png
        :scale: 100%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """

    #-- create 1st figure. Make it portait size and use the holdFigure_=True argument to specify that the figure should not be displayed yet
    expenseCategories = ["Rent", "Food", "Travel", "Fun"];
    expenses = [1000, 300, 500, 250];

    figure1 = crGraphs.createPieChart(expenses, expenseCategories, title_ = "Expenses", subPlot_=121, size_=(14,6), renderFigure_=False);

    #-- create 2nd figure into the figure1 saved previously. Specify the file path to save into.
    countries = ["Germany", "USA", "Canada"];
    numOfCountryVisits = [10, 3, 7];

    filePath = "";
    if (saveFiles_):
        filePath = "pieChart_large.png";
    crGraphs.createPieChart(numOfCountryVisits, countries, showPercentageVals_=True, showActualVals_=False,
                    subPlot_=122,figure_=figure1, filePath_=filePath);

if __name__ == "__main__":

    saveFiles = True;

    doSimpleExample(saveFiles);
    doColorsExample(saveFiles);
    doMultiFigurePrintExample(saveFiles);


