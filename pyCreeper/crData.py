"""
crData - library for python that lets you read data from files and manipulate data, mainly for use by crGraphs

Author: Lenka Pitonakova: contact@lenkaspace.net

"""

import os;
import scipy.stats;
import math;
import copy;

SHOW_OUTPUT = False;

#
def fileToArray(filePath_, separator_=",", ignoreFirstRow_=False,endRow_=-1,maxTime_=-1, timeColumn_=0, startRow_=1):
    """
    Take a file that has rows and columns of values and convert it into a 2d array 
    in format array[rows][columns]
    Set the containsNumbers_ to False if e.g. there are strings int the file
    """
    data = []
    fileOk = False;
    if (SHOW_OUTPUT == True):
        print("Reading " + filePath_ + " ...");  
    try:
        f = open(filePath_,'r')
        #-- read data into a list of strings
        lines = f.readlines()
        f.close()
        fileOk = True
    except Exception:
        raise IOError("The file " + filePath_ + " doesn't exist.");
    
    if (fileOk):
        counter=0;
        isFirstLine = True   
        #-- process the lines
        for line in lines:
            #print("LINE %d" % (counter))

            #-- ignore first row
            if (ignoreFirstRow_ and isFirstLine):
                isFirstLine = False;
                continue;

            counter+=1;
            #print(str(counter) + "  " + str(startRow_) + "  " + str(endRow_));
            #-- process to a certain row
            if (endRow_> 0 and counter > endRow_):
                continue;
            #-- start at a certain row
            if (counter < startRow_):
                continue;
           
            isFirstLine = False;
            #-- split the line into individual string numbers by comma
            dataStrings = line.split(separator_)
            #print(dataStrings);
            #-- convert the strings to ints
            dataInts = []
            for dataString in dataStrings:
                #-- clear the data string of encompassing double quotes
                dataString = dataString.replace('"','');
                if (dataString != "\n"):

                    try:
                        dataInts.append(float(dataString))
                    except:
                        dataInts.append(dataString.replace("\n",""));

            #print(dataInts);
            #-- add to main data structure
            if (len(dataInts) > 0):
                
                #-- process to a certain time of simulation, if time is given in column timeColumn_
                if (maxTime_ >= 0 and dataInts[timeColumn_] > maxTime_ ):
                    continue
  
                data.append(dataInts)
                #print(data);
            

    
   
   
    return data

    
#
def getAverage(valuesList_,nullValue_=0):
    """
    Get average value of a list of values. If no values, return nullValue_.
    """
    if (len(valuesList_) > 0):
        return sum(valuesList_) / len(valuesList_);
    return nullValue_;
#
def getMedian(valuesList_, ignoreZeros_ = False):
    """
    Get median value of a list of values.
    Can be set to ignore 0 values with the ignoreZeros_ argument. If it's true, and the list contains only 0s, 0 will be returned.
    """
    if (len(valuesList_) == 0):
        return 0;

    if (ignoreZeros_):
        valueList = [];
        for i in range(len(valuesList_)):
            if (valuesList_[i] != 0):
                valueList.append(valuesList_[i])

        if (len(valueList) == 0):
            return 0;
        #valueList = [2 for value in valueList if value != 0]
    else:
        valueList = valuesList_;

    theValues = sorted(valueList);
    if len(theValues) % 2 == 1:
        return theValues[(len(theValues)+1)/2-1]
    else:
        index = len(theValues)/2-1
        if (index >= 0 and index < len(theValues)):
            lower = theValues[len(theValues)/2-1]
            upper = theValues[len(theValues)/2]
            return (float(lower + upper)) / 2
        else:
            return theValues[0];

def getInterquartileRange(valuesList_):
    """
    Get interquartile range of a list, which is a range
    between 1st and 3rd quartile. Used usually with reporting
    median
    """
    theValues = sorted(valuesList_);
    upperQuartile = scipy.stats.scoreatpercentile(theValues, 75);
    lowerQuartile = scipy.stats.scoreatpercentile(theValues, 25);
    return upperQuartile - lowerQuartile;
#
def getListDifference(list1_,list2_):
    """
    Return a list where elements are difference between list1_ - list2_.
    If lists are 2d lists, the medians on 2nd dimensions are subtracted.
    """
    returnList = [];
    for i in range(len(list1_)):
        if (type(list1_[i]) == list and type(list2_[i]) == list):
            returnList.append(getMedian(list1_[i]) - getMedian(list2_[i]));
        else:
            returnList.append(list1_[i] - list2_[i]);
    return returnList;

#
def getListAddition(list1_,list2_):
    """
    Return a list where elements are additions between list1_ + list2_.
    If one list is shorter than another, it is understood as having 0s on the missing spaces.
    """
    returnList = [];
    length = len(list1_);
    if (len(list2_) > length):
        length = len(list2_);
    for i in range(length):
        val1 = 0;
        val2 = 0;
        if (i < len(list1_)):
            val1 = list1_[i];
        if (i < len(list2_)):
            val2 = list2_[i];
        returnList.append(val1 + val2);
    return returnList;

def getListMultiplication(list1_,list2_, debug_ = False):
    """
    Return a list where elements are multiplications of elements from list1_ * elements from list2_.
    If one list is shorter than another, error is returned.

    - list2_ can also be a single number. If that is the case, list1_ can have 1 or 2 dimensions and all its
    elements will be multiplied by number list2_

    """
    returnList = [];
    length = len(list1_);
    if (type(list2_) == list):
        if (len(list2_) != length):
            raise Exception("crData: getListMultiplication : lists must be of the same length.")
        for i in range(length):
            returnList.append(list1_[i] * list2_[i]);
    else:
        for i in range(length):
            if (type(list1_[i]) == list ):
                returnList.append([]);
                for j in range(len(list1_[i])):
                    returnList[i].append(list1_[i][j] * list2_);
            else:
                returnList.append(list1_[i] * list2_);
    if (debug_):
        print("oringinal list:")
        print(list1_)
        print("return list:")
        print(returnList)
    return returnList;


def getListDivision(list1_,list2_):
    """
    Return a list where elements are divisons of elements from list1_ / elements from list2_.
    If one list is shorter than another, error is returned.
    """
    returnList = [];
    length = len(list1_);
    if (len(list2_) != length):
        raise Exception("crData: getListMultiplication : lists must be of the same length.")
    for i in range(length):
        if (list2_[i] != 0):
            returnList.append(list1_[i] / float(list2_[i]));
        else:
            returnList.append(0);
    return returnList;

    
#
def extractColumns(array_, columns_):
    """
    Returns a 2d list with only specific columns of the array_.
    Clumn numbers are specified in the columns_ array
    """
    numOfRows = len(array_);
    numOfNewCols = len(columns_);
    retArray = [[0.0 for i in range(numOfNewCols)] for j in range(numOfRows)];
    currentCol = 0;
    for i in range(numOfRows):
        currentCol = 0;
        for j in range(len(array_[0])):
            if (j in columns_):
                retArray[i][currentCol] = array_[i][j];
                currentCol+=1;
    return retArray;

#
def columnToArray(array_, columnId_, valueMultiplier_=1):
    """
    Returns a 1d list filled with values of a column of a specified array.
    Also multiplies each value by valueMultiplier_.
    """
    retArray = [];
    numOfRows = len(array_);
    for i in range(numOfRows):
        retArray.append(array_[i][columnId_]*valueMultiplier_);
    return retArray;

#
def columnsToRows(array_):
    """
    Return array that has rows with columns swapped
    """
    numOfRows = len(array_);
    numOfCols = len(array_[0]);
    retArray = [[0.0 for i in range(numOfRows)] for j in range(numOfCols)];
    for i in range(numOfRows):
        for j in range(numOfCols):
            retArray[j][i] = array_[i][j];
    return retArray;

#
def removeValues(array_, valueToRemove_=0):
    """
    Returns a 1D list from a list array_, that does not contain valueToRemove_, i.e. is shorter
    """
    retArray = [];
    for i in range(len(array_)):
        if (array_[i] != valueToRemove_):
            retArray.append(array_[i]);
    return retArray;
    
       
#
def print2DArray(array_):
    for i in range(len(array_)):
        print(array_[i]);

#
def sampleDown2DData(data_, timeBinLength_, endTime_, isTimeFirstDimension_=True, useAverages_ = True, discardZerosFromAverages_ = False, debug_=False):
    """
    Sample down 2D data that has one dimension as time and another as soemthing else.
    isTimeFirstDimension_ defines if time is the 0th dimension of the data
    Return 2D array where 0th dimension is sampled down time (into numOfTimeBins_) and 1st dimension is the 0th dimension of the original data

    If useAverages_ is False, the returned data will be accumulation of data values for each bin.

    """
    if (debug_):
        print("sample down using time bin length " + str(timeBinLength_))
        print("Original data:")
        print(data_);

    otherDimLength = 0;
    if (isTimeFirstDimension_):
        otherDimLength = len(data_[0]);
    else:
        otherDimLength = len(data_);
    numOfTimeBins = endTime_ / timeBinLength_;
    returnData = [[0 for r in range(otherDimLength)] for i in range(numOfTimeBins)];
    for i in range(otherDimLength):
        accumulatedVal = 0;
        #print(len(data_[0]))
        timeBinNumOfNonZeroValues = 0;
        for t in range(endTime_):
            timeBin = int(math.floor(t / timeBinLength_));
            startTime = timeBin * timeBinLength_;
            endTime = startTime + timeBinLength_ - 1;
            if (t == startTime):
                timeBinNumOfNonZeroValues = 0;
                accumulatedVal = 0;
                #if (debug_):
                    #print("Time bin start at t={}".format(t))
            valueToAdd = 0;
            try:
                if (isTimeFirstDimension_):
                    valueToAdd = data_[t][i];
                else:
                    valueToAdd = data_[i][t];
            except IndexError:
                raise IndexError("!!!!!! index {} t {}  no value".format(i,t) )


            if (valueToAdd != 0):
                timeBinNumOfNonZeroValues += 1;

            accumulatedVal += valueToAdd;

            if (t == endTime):
                #-- end of time bin, take average and note it into output array
                if (useAverages_):
                    if (discardZerosFromAverages_):
                        if (timeBinNumOfNonZeroValues > 0):
                            returnData[timeBin][i] = accumulatedVal / float(timeBinNumOfNonZeroValues);
                        else:
                            returnData[timeBin][i] = 0;
                    else:
                        returnData[timeBin][i] = accumulatedVal / float(timeBinLength_);
                else:
                    returnData[timeBin][i] = accumulatedVal;

                if (debug_):
                    if (returnData[timeBin][i] != 0):
                        print("t = {} return val={} num of non zero vals={} total val={} ".format(t, returnData[timeBin][i], timeBinNumOfNonZeroValues, accumulatedVal));


    return returnData;
            