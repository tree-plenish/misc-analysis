# Timeline Analysis by School
# Overlaying line plots of cumulative tree requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

# Getting list of files
path = "C:/Users/justi/Downloads/Tree Requests By Event (1)/"
fileList = os.listdir(path)

# Administrative
data = dict()
errorCount = 0
plottedCount = 0
otherSheetCount = 0

# Looping through each file in extracted .htmls
for file in fileList:

    # If sheet is a tree request form
    if "Tree Request" in file:

        # Exception for data misentry on user side
        try:

            # Load dataframe from html file
            df = pd.read_html(path + file)[0]

            # Get the index of total trees and submit times for that sheet
            treeInd = np.where(df.iloc[[0]].values == "score")[-1][0]
            dateInd = np.where(df.iloc[[0]].values == "Submitted At")[-1][0]

            # Get list of trees requested, adding a 0 at the first day 
            treesRequested = np.append([0],df[df.columns[treeInd]][2:].values.astype(int))

            # Get the dates requested in string format adding the first day
            dateArray = df[df.columns[dateInd]][2:].values
            dateRequested = np.array([datetime.datetime(2020,12,6)])
            

            # For each date in the string array
            for i in range(len(dateArray)): 

                # Convert the date submitted to datetime and append to datetime array
                dt = dateArray[i]
                length = len(dt)
                dateRequested = np.append(dateRequested, datetime.datetime.strptime(dt, '%m/%d/%Y %H:%M:%S'))


            # Plot this sheets data       
            plt.plot(dateRequested, np.cumsum(treesRequested))

            # Administrative success count
            plottedCount = plottedCount + 1
            
        except:
            # Administrative failure count
            errorCount = errorCount + 1


    else: # if 'tree request' not in file name
        otherSheetCount = otherSheetCount + 1
        

# Title and display overall chart
plt.title("Cumulative Tree Requests by Event")
plt.show()
