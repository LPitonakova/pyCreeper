from numpy import random;
from pyCreeper import crGraphs;
from pyCreeper import crGraphStyle;
crGraphs.BASE_FILE_PATH = "../../exampleOutput/";


def example1_simple(saveFiles_):
   """
   In this example, a simple bar plot is created:

   .. image:: ../exampleOutput/barPlot_simple.png
       :scale: 50%

   :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
   """
   profitData = [
      [10, 25, 40, 32, 60, 85, 75, 55, 70]
   ];

   months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep"];

   filePath = "";
   if (saveFiles_):
      filePath = "barPlot_simple.png";

   style = crGraphStyle.crGraphStyle();
   style.gridType = crGraphStyle.GRID_TYPE.NONE;
   crGraphs.setStyle(style);

   crGraphs.createBarPlot(profitData, "Profit so far this year", xTickLabels_=months, xLabel_="Month", yLabel_="Profit (mil. £)", yMin_=0, yMax_=100, filePath_=filePath);


def example2_errorBars(saveFiles_):
   """
   In this example, a multi-bar plot with error bars is created. A legend with a title and horizontal-only grid is shown:

   .. image:: ../exampleOutput/barPlot_errorBars.png
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
      filePath = "barPlot_errorBars.png";

   style = crGraphStyle.crGraphStyle();
   style.markers = ['o','o','s'];
   style.colors = ['g','c','r'];
   style.numOfLegendColumns = 3;
   style.legendPosition = crGraphStyle.LEGEND_POSITION.UPPER_LEFT;
   style.gridType = crGraphStyle.GRID_TYPE.HORIZONTAL;
   crGraphs.setStyle(style);

   crGraphs.createBarPlot(profitData, "Profit so far this year", xTickLabels_=months, xLabel_="Month", yLabel_="Profit (mil. £)", yMin_=-20, yMax_=120,
      legendTitle_="Profit types:", legendLabels_=legendLabels, showConfidenceIntervals_=True, filePath_=filePath);

if __name__ == "__main__":

   saveFiles = False;

   example1_simple(saveFiles);
   example2_errorBars(saveFiles);