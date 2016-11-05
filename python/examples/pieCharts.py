from python.pyCreeper.crGraphs import createPieChart;


def doSimpleExample():
    """
    In this example, a simple pie chart is created and displayed on the screen.

    """
    expenseCategories = ["Rent", "Food", "Travel", "Fun"];
    expenses = [1000, 300, 500, 250];

    createPieChart(expenses, expenseCategories);

def doColorsExample():
    """
    In this example, the title, colors and font sizes are specified. Percentage values and actual values are also shown

    """
    expenseCategories = ["Rent", "Food", "Travel", "Fun"];
    expenses = [1000, 300, 500, 250];
    colors = ['yellow','cyan','grey','white']

    createPieChart(expenses, expenseCategories, colors, title_="Colors example", showPercentageVals_=True, showShadow_=True);

def doMultiFigurePrintExample():
    """
    In this example, 2 figures are created below each other and saved into a single file.
    :return:
    """

    #-- create 1st figure. Make it portait size and use the holdFigure_=True argument to specify that the figure should not be displayed yet
    expenseCategories = ["Rent", "Food", "Travel", "Fun"];
    expenses = [1000, 300, 500, 250];

    figure1 =  createPieChart(expenses, expenseCategories, title_ = "Expenses", subPlot_=211, size_=(8,16), holdFigure_=True);

    #-- create 2nd figure into the figure1 saved previously. Specify the file path to save into.
    countries = ["Germany", "USA", "Canada"];
    numOfCountryVisits = [10, 3, 7];

    createPieChart(numOfCountryVisits, countries, showPercentageVals_=True, showActualVals_=False,
                    subPlot_=212,figure_=figure1, filePath_="./pieChart.png");

if __name__ == "__main__":

    #doSimpleExample();
    #doColorsExample();
    doMultiFigurePrintExample();


