"""
A module that lets you read data from files and manipulate data, mainly for use by crGraphs

Author: Lenka Pitonakova: contact@lenkaspace.net

"""

import os;
import scipy.stats;
import math;
import copy;

SHOW_OUTPUT = False;

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


def getArrayByFlippingColumnsAndRows(array_):
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



def sampleDownTimeSeriesData(data_, timeBinLength_, isTimeFirstDimension_=True, useAverages_ = True, discardZerosFromAverages_ = False, debug_=False):
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
        endTime_ = len(data_)
    else:
        otherDimLength = len(data_);
        endTime_ = (len(data_[0]));


    numOfTimeBins = int(endTime_ / timeBinLength_);
    if (numOfTimeBins*timeBinLength_ < endTime_):
        numOfTimeBins += 1;

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
