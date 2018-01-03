
DEBUG_LEVEL = 0;

#
def fileToArray(filePath_, separator_=",", ignoreFirstRow_=False,endRow_=-1,maxTime_=-1, timeColumn_=0, startRow_=1):
    """
    Take a file that has rows and columns of values and convert it into a 2d array
    in format array[rows][columns]
    Set the containsNumbers_ to False if e.g. there are strings int the file
    """
    data = []
    fileOk = False;
    if (DEBUG_LEVEL == 1):
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
