from python.pyCreeper import crGraphs;
crGraphs.BASE_FILE_PATH = "../../exampleOutput/";

def example1_simple(saveFiles_):
    """
    In this example, a simple matrix plot created:

    .. image:: ../exampleOutput/matrixPlot_simple.png
        :scale: 50%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """

    performanceData = [
                        [12,11,10,9],
                        [11,10,7,6],
                        [9,8,6,5],
    ]
    filePath = "";
    if (saveFiles_):
        filePath = "matrixPlot_simple.png";

    crGraphs.createMatrixPlot(performanceData, "Cost of fuel for drivers", colorBarLabel_="Fuel cost", xLabel_="Driver skill", yLabel_="Engine efficiency", filePath_=filePath)



def example2_customAnnotations(saveFiles_):
    """
    In this example, a matrix plot with custom annotations is created:

    .. image:: ../exampleOutput/matrixPlot_fullAnnotations.png
        :scale: 50%

    :param saveFiles_: Boolean if True, figures are saved, if False, figures are displayed
    """
    performanceData = [
                        [12,11,10,9],
                        [11,10,7,6],
                        [9,8,6,5],
    ]

    annotations = [ ['poor','poor','good','good'],
                    ['poor','poor', 'good', 'excellent'],
                    ['good', 'good','excellent','excellent']
    ];

    filePath = "";
    if (saveFiles_):
        filePath = "matrixPlot_fullAnnotations.png";

    crGraphs.createMatrixPlot(performanceData, "Cost of fuel for drivers", colorBarLabel_="Fuel cost",
                            xLabel_="Driver skill", xTickLabels_=["Terrible","Quite bad","Satisfactory","Good"],
                            yLabel_="Engine efficiency", yTickLabels_=["Inefficient","OK","Efficient"],
                            annotateValues_=True, annotationValues_=annotations, annotationStringAfter_= "\ncost\nefficiency",
                            filePath_=filePath, size_=(12,7))

if __name__ == "__main__":

    saveFiles = True;

    example1_simple(saveFiles);
    example2_customAnnotations(saveFiles);

