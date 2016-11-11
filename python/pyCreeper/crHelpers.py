"""

A module that let you create pretty graphs with single-line function calls

Author: Lenka Pitonakova: contact@lenkaspace.net

"""

import numpy;
import inspect;

from . import crData;

def checkVariableIsList(variable_, dimensions_ = 1, nonEmpty_=False):
    """
    Raises a TypeError if a variable is not a list.

    :param `variable_`: The value of a variable
    :param `dimensions_`: (optional, default=1) The number of dimensions of the array
    :param `nonEmpty_`: (optional, default=False) If true, the list must be non-empty
    """

    throwException = False;
    numOfDimensions = crData.getNumberOfListDimensions(variable_);
    if (numOfDimensions != dimensions_):
        throwException = True;

    if (nonEmpty_):
        if (len(variable_) == 0):
            throwException = True;

    if (throwException):
        errorStr = "The " + getVariableNamePassedAsFirstParameter() + " parameter must be a ";
        if (nonEmpty_):
            errorStr += "non-empty ";
        errorStr += str(dimensions_) + "D list"
        raise TypeError(errorStr);

def checkListsHaveTheSameLength(list1_, list2_, list2Name_):
    """
    Raises a ValueError if 2 lists are not of the same length.

    :param `list1_`: List 1
    :param `list2_`: List 2
    :param `list2Name_`: Name of list 2 variable
    """
    list1Name = getVariableNamePassedAsFirstParameter();
    if (len(list1_) != len(list2_)):
        raise ValueError("The " + list1Name + " and " + list2Name_ + " must have the same length. Length of " + list1Name + " is " + str(len(list1_)) + ". Length of " + list2Name_ + " is " + str(len(list2_)) + ".");


def getVariableNamePassedAsFirstParameter():
    """
    Get the name of the variable that was passed as the first parameter to a function that called this function.

    :return: String variable name
    """

    try:
        frame = inspect.getouterframes(inspect.currentframe())[2]; # go 2 steps up in the frame - 1 step to the function that called this, 1 step to the function that called the function in step 1.
        string = inspect.getframeinfo(frame[0]).code_context[0].strip();

        args = string[string.find('(') + 1:-1].split(',') #TODO: this line needs to change to be able to get name of any, not just the first, passed variable
        arg = args[0]
        if arg.find('=') != -1:
            variableName = (arg.split('=')[1].strip())
        else:
            variableName = arg
        if (variableName[-1] == ")"):
            variableName = variableName[:-1];
    except Exception:
        variableName = "[Unknown argument name]"

    return str(variableName);
