# Typeform Analytics... Views, Costs, and Successes
# Runtime < 60 Seconds
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
import requests


# apiKey = HIDDEN, text me if not running on server
headers = {"Authorization" : "Bearer " + apiKey}
    
# Getting and choosing all ids
def getIds(keyword):
    global apiKey
    global headers
    
    # List to collect all ids ft. keyword as strings
    idList = []
    nameList = []

    # Get request + json
    result = requests.get("https://api.typeform.com/forms", params = {"page_size" : 200}, headers = headers)
    json = result.json()

    # Check json is right length and get items
    assert(json['total_items'] <= 200) # Will need to refactor once we get more than one page
    itemJson = json["items"]

    # Loop through json of items and keep ids with the right name
    for item in itemJson:

        if keyword in item['title']:

            idList.append(item['id'])
            nameList.append(item['title'].split(keyword)[0])


    return idList, nameList

# Calling to get tree requests
idList, nameList = getIds("Tree Request")

# Sorting namelist and getting the args of that sort to sort ids
argSort = np.argsort(nameList)
nameList.sort()
idList = np.array(idList)[argSort]

# Load typeform analytics stats
# Initializing statlists from summary
timeList = []
responseList = []
visitList = []
uniqueList = []

# Looping through each id
for i in range(len(idList)):
    
    # Request stat summary
    result = requests.get("https://api.typeform.com/insights/" + idList[i] + "/summary", headers = headers)
    stats = result.json()
    summary = stats['form']['summary']

    # Getting statlists
    timeList.append(summary['average_time'])
    responseList.append(summary['responses_count'])
    visitList.append(summary['total_visits'])
    uniqueList.append(summary['unique_visits'])

# Loading in treesBySchool csv as df, gonna have to mangle (hardcoded)
df = pd.read_csv("treesBySchool.csv")
df = df.drop(df.columns[4:], axis = 1)
df.columns = ["event", "requests", "goal", "price"]
df = df.sort_values(by=['event'])

# Gonna have to hard code some more weak comparer
"""
for i in range(len(df.event)):

    sameFirstWord = df.event.iloc[i].split(" ")[0] == nameList[i].split(" ")[0]

    if not sameFirstWord:

        del nameList[i]

        print(nameList[i])

"""
# Well this sucks... just go through it manually for now

# Dropping typeforms with no requests made
for td in [82, 63, 48, 44, 35, 21, 19, 14, 12, 11]:

    del nameList[td]
    del timeList[td]
    del responseList[td]
    del visitList[td]
    del uniqueList[td]
    
# Here is a clearer picture of what is happening here, we need to drop in stats lists as well
"""
del nameList[82]
del nameList[63]
del nameList[48] # If mansfield numbers are messed up switch this to 49 (other mansfield form)
del nameList[44]
del nameList[35]
del nameList[21]
del nameList[19]
del nameList[14]
del nameList[12]
"""

# Reinserting ones with different names alphabetically (can't really loop this one)
nameList.insert(6, nameList[79])
del nameList[80]
timeList.insert(6, timeList[79])
del timeList[80]
responseList.insert(6, timeList[79])
del responseList[80]
visitList.insert(6, nameList[79])
del visitList[80]
uniqueList.insert(6, uniqueList[79])
del uniqueList[80]

# Having to delete weird ones with names that were really screwed up
df = df.drop(index = df.index[41])
df = df.drop(index = df.index[13])

# Adding the lists to the df
df["time"] = timeList
df["response"] = responseList
df["visit"] = visitList
df["unique"] = uniqueList

# ---------------------
# Cleaning Completed...
# ---------------------

# I capped, the free trees are fucked up too. df.price == 0 gives what airtable thinks our free trees are
# The following segment creates a copy of df and gives what typeform knows
# CAREFUL... ALSO HARDCODED I LITERALLY CANT DO ANYTHING ELSE

# Duplicate
oldDf = df

# Full list of free trees from typeform responses lack of you owe $X for trees
listOfFrees = [0, 5, 7, 8, 22, 32, 36, 38, 39, 41, 44, 47, 61, 62, 63, 72]

# Change all of these prices to 0, I guess we'll never know for <100% discounts 
for idx in listOfFrees:
    df.price[idx] = 0

# -------------
# Now its clean
# -------------

# Getting free df
dfree = df[df.price == 0]
dcost = df[df.price > 0]

# RESULTS
"""
Did some simple off-script pandas stuff
Results pending
"""
