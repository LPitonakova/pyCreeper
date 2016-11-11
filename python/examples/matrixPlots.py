from python.pyCreeper import crGraphs;
from python.pyCreeper import crData;

def doSimpleExample(saveFiles_):

    performanceData = [
                        [12,11,10,9],
                        [11,10,7,6],
                        [9,8,6,5],
    ]
    filePath = "";
    if (saveFiles_):
        filePath = "matrixPlot_simple.png";

    crGraphs.createMatrixPlot(performanceData, colorBarLabel_="Fuel cost", xLabel_="Driver skill", yLabel_="Engine efficiency", filePath_=filePath)



def doCustomAnnotationsExample(saveFiles_):

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

    crGraphs.createMatrixPlot(performanceData, colorBarLabel_="Fuel cost",
                            xLabel_="Driver skill", xTickLabels_=["Terrible","Quite bad","Satisfactory","Good"],
                            yLabel_="Engine efficiency", yTickLabels_=["Inefficient","OK","Efficient"],
                            annotateValues_=True, annotationValues_=annotations, annotationStringAfter_= "\ncost\nefficiency",
                            filePath_=filePath, size_=(11,6))

if __name__ == "__main__":

    saveFiles = True;

    doSimpleExample(saveFiles);
    doCustomAnnotationsExample(saveFiles);

