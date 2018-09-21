
DEBUG_LEVEL = 0;

#
def fileToArray(filePath_, separator_=",", ignoreFirstRow_=False, startRow_=1, endRow_=-1):
   """
   Store data from a file in a 2D array with format array[rows][columns]. For example, if a file looks like this:

   .. code-block:: python

       time,column1,column2
       1,20,30
       2,25,60

   The resulting data array will be

   .. code-block:: python

       [[1,20,30],
        [2,25,60]]

   :param filePath_: Full path to the file
   :param separator_: (optional, default = ",") String that separates values in a row
   :param ignoreFirstRow_: (optional, default = False) If True, the first row of the file will not be parsed. Useful when the first row contains column descriptions
   :param startRow_: (optional, default = 1) The first row that will be read
   :param endRow_: (optional, default = -1) When >=0, only rows up to `endRow_` will be read

   :return: A 2D array
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
            data.append(dataInts)
            #print(data);

   return data
