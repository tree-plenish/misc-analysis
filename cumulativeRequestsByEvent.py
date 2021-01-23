# Timeline Analysis by School
# Overlaying line plots of cumulative tree requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import numpy as np

# Getting list of files
path = "C:/Users/justi/Downloads/Tree Requests By Event/"
fileList = os.listdir(path)

# Free tree indicator
freeTreePrompt = "You have requested {{var:score}} trees, and will be prompted to donate {{var:price}} (including processing fee). Would you be able to support our student-run organization by donating an additional $5 to help us build sustainable communities?"

# Administrative
data = dict()
errorCount = 0
plottedCount = 0
otherSheetCount = 0
totalTrees = np.array([])

# Looping through each file in extracted .htmls
for file in fileList:

    # If sheet is a tree request form
    if "Tree Request" in file:

        # Exception for data misentry on user side
        try:

            # Load dataframe from html file
            df = pd.read_html(path + file)[0]

            # Assigning free tree boolean value
            if freeTreePrompt in df.values:


                freeTree = False
                color = "Red"
                label = "Must Pay"

            else:

                freeTree = True
                color = "Green"
                label = "Free"
                print(file)
            

            # Get the index of total trees and submit times for that sheet
            treeInd = np.where(df.iloc[[0]].values == "score")[-1][0]
            dateInd = np.where(df.iloc[[0]].values == "Submitted At")[-1][0]


            # Get list of trees requested, adding a 0 at the first day 
            treesRequested = np.append([0],df[df.columns[treeInd]][2:].values.astype(int))
            totalTrees = np.append(totalTrees, np.sum(treesRequested))
            
            # Get the dates requested in string format adding the first day
            dateArray = df[df.columns[dateInd]][2:].values
            dateRequested = np.array([datetime.datetime(2020,12,6)])
            

            # For each date in the string array
            for i in range(len(dateArray)): 

                # Convert the date submitted to datetime and append to datetime array
                dt = dateArray[i]
                length = len(dt)
                dateRequested = np.append(dateRequested, datetime.datetime.strptime(dt, '%m/%d/%Y %H:%M:%S'))


            # Adding the ending amount to the end of the dates
            treesRequested = np.append(treesRequested, treesRequested[-1])
            dateRequested = np.append(dateRequested, datetime.datetime.now())
            

            # Plot this sheets data            
            plt.step(dateRequested, np.cumsum(treesRequested), color = color, label=label, linewidth = .4)

            # Administrative success count
            plottedCount = plottedCount + 1
            
        except:
            # Administrative failure count
            errorCount = errorCount + 1


    else: # if 'tree request' not in file name
        otherSheetCount = otherSheetCount + 1
        

# Title and display overall chart
plt.title("Cumulative Tree Requests by Event")
#plt.legend()
plt.show()
