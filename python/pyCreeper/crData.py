"""
A module that lets you read data from files and manipulate data, mainly for use by crGraphs

Author: Lenka Pitonakova: contact@lenkaspace.net

"""

import os;
import scipy.stats;
import math;
import copy;

SHOW_OUTPUT = False;


#======================== LIST PROPERTIES ================

def getNumberOfListDimensions(list_):
    """
    Return the number of dimensions of an N-dimensional list by recursively going through the list
    until a non-list or an empty list is found in one of the dimensions.

    To correctly measure dimensionality, it is recommended that the list doesn't contain empty sublists and that
    all elements (apart from those in the highest dimension) are of the same type.

    :param list_: The list

    :return: int : The number of dimensions
    """
    stop = False;
    dimension = 0;
    listToCheck = list_;

    while (stop == False):
        try:
            listToCheck = listToCheck[dimension];
            dimension += 1;
            #-- if this not a list, stop immediatelly
            if (type(listToCheck) != list):
                stop = True;


        except:
            #print("Exception at dimension " + str(dimension));
            stop = True;
            #-- check that the exception wasn't thrown because the list is empty at this dimension.
            #   if that was the case, count that as a valid dimension
            try:
                length = len(listToCheck);
                dimension += 1;
            except:
                pass
                #print("Not an empty list at dimension " + str(dimension));

    return dimension;



def getMinValueInAList(list_):
    """
    Get a minimum value from an N-dimensional list of numbers

    :param list_: The list

    :return: number
    """

    numOfDimensions = getNumberOfListDimensions(list_);
    if (numOfDimensions == 1):
        return min(list_)
    elif (numOfDimensions == 2):
        return min([min(list_[x]) for x in range(len(list_))]);
    else:
        raise NotImplementedError("crData.getMinValueInAList() has not been implemented for more than 2-dimensional lists.")


def getMaxValueInAList(list_):
    """
    Get a maximum value from an N-dimensional list of numbers

    :param list_: The list

    :return: number
    """

    numOfDimensions = getNumberOfListDimensions(list_);
    if (numOfDimensions == 1):
        return max(list_)
    elif (numOfDimensions == 2):
        return max([max(list_[x]) for x in range(len(list_))]);
    else:
        raise NotImplementedError("crData.getMaxValueInAList() has not been implemented for more than 2-dimensional lists.")



def getMedianOfAList(list_, ignoreZeros_ = False):
    """
    Get median value of a list of values.

    :param list_: The list
    :param ignoreZeros_: (optional, default = False) If true, only non-zero values are considered when looking for a median

    :return number
    """
    if (len(list_) == 0):
        return 0;

    if (ignoreZeros_):
        valueList = [];
        for i in range(len(list_)):
            if (list_[i] != 0):
                valueList.append(list_[i])

        if (len(valueList) == 0):
            return 0;
        #valueList = [2 for value in valueList if value != 0]
    else:
        valueList = list_;

    theValues = sorted(valueList);
    if len(theValues) % 2 == 1:
        return theValues[int((len(theValues)+1)/2-1)]
    else:
        index = len(theValues)/2-1
        if (index >= 0 and index < len(theValues)):
            lower = theValues[int(len(theValues)/2)-1]
            upper = theValues[int(len(theValues)/2)]
            return (float(lower + upper)) / 2
        else:
            return theValues[0];


#
def getAverageOfAList(list_, ignoreZeros_=False, nullValue_ = 0):
    """
    Get average value of a list of values.

    :param list_: The list
    :param ignoreZeros_: (optional, default = False) If true, only non-zero values are considered when calculating the average
    :param nullValue_: (optional, default = 0) Value that should be returned when the `list_` is empty

    :return number

    """

    valueList = list_;
    if (ignoreZeros_):
        valueList = [];
        for i in range(len(list_)):
            if (list_[i] != 0):
                valueList.append(list_[i])

    if (len(valueList) > 0):
        return sum(valueList) / len(valueList);

    return nullValue_;

#======================== LIST ELEMENTS MANIPULATION ================


def addUniqueElementToList(element_, array_, debugMessage_ = "", printDebug_ = False):
    if (not (element_ in array_)):
        array_.append(element_);
        if (printDebug_ and debugMessage_ != ""):
            print(debugMessage_);

def removeElementFromList(element_, array_, debugMessage_ = "", printDebug_ = False):
    if (element_ in array_):
        array_.remove(element_);
        if (printDebug_ and debugMessage_ != ""):
            print(debugMessage_);

def getListByFlippingColumnsAndRows(array_):
    """
    Return array that has rows with columns flipped

    :param array_: 2D array of data

    :return: 2D array of data
    """
    numOfDimensions=getNumberOfListDimensions(array_);
    if (numOfDimensions != 2):
        raise ValueError("The parameter array_ must be a 2D array. The array provided has {} dimension(s).".format(numOfDimensions))

    numOfRows = len(array_);
    numOfCols = len(array_[0]);
    retArray = [[0.0 for i in range(numOfRows)] for j in range(numOfCols)];
    for i in range(numOfRows):
        for j in range(numOfCols):
            retArray[j][i] = array_[i][j];
    return retArray;

def getListColumnAsArray(array_, columnId_, valueMultiplier_=1):
    """
    Returns a 1d list filled with values of a column of a specified array.
    Also multiplies each value by `valueMultiplier_`.

    :param array_: 2D array of data
    :param columnId_: id of the column to retrieve (0-based)
    :param valueMultiplier_: (optional, default=1) A value by which to multiply each element in the selected column

    :return 1D array with selected data
    """
    retArray = [];
    numOfRows = len(array_);
    for i in range(numOfRows):
        retArray.append(array_[i][columnId_]*valueMultiplier_);
    return retArray;


def compressList(data_, timeBinLength_, useAverages_ = True, discardZerosFromAverages_ = False, debug_=False):
    """
    Compress a list by aggregating data into bins.

    For example:

    .. code-block:: python

        realTimeData = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10];

        compressedData = pyCreeper.crData.compressList(realTimeData,3)
        print(compressedData)

        [out:] [2.0, 5.0, 8.0, 3.3333333333333335]

    :param data_: 2D array
    :param timeBinLength_: length of one time bin (number of time bins of the uncompressed data)
    :param useAverages_: (optional, default = True) If true, the compressed value in each bin will be an average of values of the uncompressed data. If false, sum of uncompressed data values will be used.
    :param discardZerosFromAverages_: (optional, default = False) If true, averages calculated when useAverages_=True do not take 0s into account
    :param debug_: (optional, default = False) If true, extra debug info is printed

    :return: A compressed list
    """

    # Note: in the below code, "time" is synonymous to the dimension to compress

    if (debug_):
        print("sample down using time bin length " + str(timeBinLength_))
        print("Original data:")
        print(data_);

    endTime = len(data_)


    numOfTimeBins = int(endTime / timeBinLength_);
    if (numOfTimeBins*timeBinLength_ < endTime):
        numOfTimeBins += 1;

    returnData = [0 for i in range(numOfTimeBins)];

    accumulatedVal = 0;

    timeBinNumOfNonZeroValues = 0;
    binEndTime = endTime;
    for t in range(binEndTime):
        timeBin = int(math.floor(t / timeBinLength_));
        startTime = timeBin * timeBinLength_;
        binEndTime = min(endTime-1, startTime + timeBinLength_ - 1);

        if (t == startTime):
            timeBinNumOfNonZeroValues = 0;
            accumulatedVal = 0;
            if (debug_):
                print("Time bin start at t={}".format(t))

        valueToAdd = 0;
        try:
            valueToAdd = data_[t];
        except IndexError:
            pass


        if (valueToAdd != 0):
            timeBinNumOfNonZeroValues += 1;

        accumulatedVal += valueToAdd;
        if (debug_):
            print("t {} endTime {} val {}".format(t, binEndTime, accumulatedVal));

        if (t == binEndTime):
            #-- end of time bin, take average and note it into output array
            if (useAverages_):
                if (discardZerosFromAverages_):
                    if (timeBinNumOfNonZeroValues > 0):
                        returnData[timeBin] = accumulatedVal / float(timeBinNumOfNonZeroValues);
                    else:
                        returnData[timeBin]= 0;
                else:
                    returnData[timeBin] = accumulatedVal / float(timeBinLength_);
            else:
                returnData[timeBin] = accumulatedVal;

            if (debug_):
                if (returnData[timeBin] != 0):
                    print("t = {} return val={} num of non zero vals={} total val={} ".format(t, returnData[timeBin], timeBinNumOfNonZeroValues, accumulatedVal));


    return returnData;
