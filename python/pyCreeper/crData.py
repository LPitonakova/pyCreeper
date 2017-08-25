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
