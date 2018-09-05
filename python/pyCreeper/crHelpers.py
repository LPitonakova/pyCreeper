"""

A module that lets you create pretty graphs with single-line function calls

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

    checkVariableDataType(variable_,list);

    #-- check dimensions
    throwException = False;
    numOfDimensions = crData.getNumberOfListDimensions(variable_);
    if (numOfDimensions != dimensions_):
        throwException = True;

    if (nonEmpty_):
        if (len(variable_) == 0):
            throwException = True;

    if (throwException):
        errorStr = "The " + getVariableNamePassedAsParameter() + " parameter must be a ";
        if (nonEmpty_):
            errorStr += "non-empty ";
        errorStr += str(dimensions_) + "D list"
        raise TypeError(errorStr);

def checkListsHaveTheSameLength(list1_, list2_):
    """
    Raises a ValueError if 2 lists are not of the same length.

    :param `list1_`: List 1
    :param `list2_`: List 2
    """
    list1Name = getVariableNamePassedAsParameter();
    list2Name = getVariableNamePassedAsParameter(2);
    if (len(list1_) != len(list2_)):
        raise ValueError("The " + list1Name + " and " + list2Name + " must have the same length. Length of " + list1Name + " is " + str(len(list1_)) + ". Length of " + list2Name + " is " + str(len(list2_)) + ".");

def checkListHasAtLeastLengthOfList(list1_, list2_):
    """
    Raises a ValueError if list 1 is shorter than list 2.

    :param `list1_`: List 1
    :param `list2_`: List 2 to compare length of ``list1_`` to
    """
    list1Name = getVariableNamePassedAsParameter();
    list2Name = getVariableNamePassedAsParameter(2);
    if (len(list1_) < len(list2_)):
        raise ValueError(list1Name + " must have at least length of " + list2Name + ". Length of " + list1Name + " is " + str(len(list1_)) + ". Length of " + list2Name + " is " + str(len(list2_)) + ".");


def checkVariableDataType(variable_, expectedDataType_):
    """
    Check if a variable has a specified data type. If not, raises a TypeError.

    :param `variable_`: The value of a variable
    :param `expectedDataType_`: The desired data type. Can either be one type or a list of types

    """

    if (not variable_ is None):
        if (not isinstance(variable_, expectedDataType_)):
            raise TypeError("The " + getVariableNamePassedAsParameter() + " parameter must be of data type " + str(expectedDataType_) + ". Got: " + str(type(variable_)));


def checkVariableGreaterThanAnother(variable1_, variable2_):
    """
    Check if a variable is greater than another. If not, raises a TypeError.

    :param `variable1_`: The value of variable 1
    :param `variable2_`: The value of variable 2
    """
    variable1Name = getVariableNamePassedAsParameter();
    variable2Name = getVariableNamePassedAsParameter(2);
    if (variable1_ <= variable2_):
        raise ValueError("The value of " + variable1Name + " must be greater than " + variable2Name + ". Got " + variable1Name + " = " + str(variable1_) + ", " + variable2Name + " = " + str(variable2_));


def checkVariableBetweenValues(variable_, valueMin_, valueMax_):
    """
    Check if `valueMin_` <= `variable_` <= `valueMax_`

    :param `variable_`: The value of the variable
    :param `valueMin_`: Minimum value the variable can take
    :param `valueMax_`: Maximum value the variable can take

    """
    variable1Name = getVariableNamePassedAsParameter();

    if (valueMin_ > variable_ or valueMax_ < variable_):
        raise ValueError("The value of " + variable1Name + " must be " + str(valueMin_) + " <= " + variable1Name + " <= " + str(valueMax_) + ". Got " + variable1Name + " = " + str(variable_));


def getVariableNamePassedAsParameter(parameterNumber_=1):
    """
    Get the name of the variable that was passed as the first parameter to a function that called this function.

    :param parameterOrder_: (optional, default = 1) Parameter number (1-X)
    :return: String variable name
    """

    try:
        frame = inspect.getouterframes(inspect.currentframe())[2]; # go 2 steps up in the frame - 1 step to the function that called this, 1 step to the function that called the function in step 1.
        string = inspect.getframeinfo(frame[0]).code_context[0].strip();

        args = string[string.find('(') + 1:-1].split(',')
        arg = args[parameterNumber_-1]
        if arg.find('=') != -1:
            variableName = (arg.split('=')[1].strip())
        else:
            variableName = arg
        if (variableName[-1] == ")"):
            variableName = variableName[:-1];
        if (variableName[0] == " "):
            variableName = variableName[1:];

    except Exception:
        variableName = "[Unknown argument name]"
    return str(variableName);
