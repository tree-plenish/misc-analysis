# Surgeo accuracy analysis using collected demographic data
import numpy as np
import pandas as pd
import surgeo

# Tree plenish event demographic responses... pre-downloaded
df = pd.read_csv("/home/justinmiller/Documents/Data/tpEventDemographic.csv")

names = df[df.columns[2]].values
last_names = [name.split(" ")[-1] if name.split(" ")[-1] else name.split(" ")[-2] for name in names]

fsg = surgeo.SurnameModel()

fsg_results = fsg.get_probabilities(pd.Series(last_names))
print(str(len(fsg_results)) + " Total Entries")

df = pd.concat([df, fsg_results], axis = 1)

df = df.dropna(subset = ['white'])
print(str(len(df)) + " Usable Surnames")

pd.set_option('display.max_columns', None)
print(df)

# Mapping keys for comparison row by row
r = 5 # Column with race question
keys = np.unique(df[df.columns[r]]) # Race row
keyMap = {}
keyMap[keys[0]] = "api"
keyMap[keys[1]] = "black"
keyMap[keys[2]] = "hispanic"
keyMap[keys[3]] = "multiple"
keyMap[keys[6]] = "white"

# Looping through to find percent estimate of actual race
probList = np.array([])

for i in df.index:

    race = df[df.columns[r]][i]
    try:
        probability = df[keyMap[race]][i]
        probList = np.append(probList, probability)
    except:
        probList = np.append(probList, np.nan)
        print("The user answered: " + race) 

        
# Adding problist back onto df
df = pd.concat([df, pd.DataFrame(probList, index = df.index)], axis = 1)
df.columns[-1] = "probability"

