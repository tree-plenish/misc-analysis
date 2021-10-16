import numpy as np
import pandas as pd
pd.set_option("display.max_rows", 10, "display.max_columns", None)
import matplotlib.pyplot as plt

#########################
# Loading in df & y set #
# Identification simply #
# using emails to start #
#########################

# Loading in saved demographic & global address data from offline source
principals = pd.read_csv("../../privateData/principals.csv")
teachers = pd.read_csv("../../privateData/teachers.csv")

# Combining dfs
df = principals.append(teachers)
print(len(df), " total entries.")

# Loading in responses (interest forms)
interest_df = pd.read_csv("../../privateData/typeform1008.csv")
interest_emails = interest_df["Email?"].values

################################
# Loading in interest variable #
################################ 

# Adding new variable for interest 
interest_bool = [int(i in interest_emails) for i in df["Email Address"].values]
df["interest"] = interest_bool
print(sum(interest_bool), " identifiable interested.")

# Not good enough. Cue levenshtein

####################################
# FUNCTION FOR CLEANING STATE DATA #
# IDK WHERE ELSE TO PUT THIS BITCH #
####################################
def get_state_codes(state_column):
    # Loading in and cleaning states/abbrevs/code lookup table
    states = pd.read_csv("states.csv")
    states["State"] = [state.lower() for state in states["State"]]
    states["Abbrev"] = [abb.replace(".","").lower() for abb in states["Abbrev"]]
    states["Code"] = [code.lower() for code in states["Code"]]

    # Getting distribution of how people describe state
    state_input = {"state":0,"abbrev":0,"code":0,"unident":0}
    state_user = [state.lower() for state in state_column]
    state_idx = []

    # Looping through user states to get aquisition type counts and global labels
    for state in state_user:
        
        if state in states["State"].values:
            state_input["state"] = state_input["state"] + 1
            idx = np.argmax(states["State"] == state)
        elif state in states["Abbrev"].values:
            state_input["abbrev"] = state_input["abbrev"] + 1
            idx = np.argmax(states["Abbrev"] == state)
        elif state in states["Code"].values:
            state_input["code"] = state_input["code"] + 1
            idx = np.argmax(states["Code"] == state)
        else:
            state_input["unident"] = state_input["unident"] + 1
            idx = 999
        state_idx.append(idx)
        
    # Displaying identification status
    print("ID Status: ", state_input)

    # Getting state code from state index
    state_codes = [states["Code"].values[i] if i!=999 else "UNKNOWN" for i in state_idx]
    
    return state_codes

#############################
# DONE get_state_codes FUNC #
#############################

#################################
# Finding better identification #
# Using schools and states      #
#################################

# Getting interest state codes
state_column = interest_df["What state are you from?"]
state_codes = get_state_codes(state_column)

# Showing distribution of states
from collections import Counter
count = dict(Counter(state_codes))
print(count)
print(len(count)-1, " states interested.")

# Also (for fun) let's get some state estimates
# Getting rid of unknown for this
unknowns = count["UNKNOWN"]
del count["UNKNOWN"]

# Getting percent count dict
props = []
prop_keys = []
for key in list(count.keys()):
    prop_keys.append(key)
    props.append(count[key] / len(interest_df))
    
prop_keys = [prop_keys[i] for i in np.argsort(props)[::-1]]
props = np.sort(props)[::-1]

# Getting odds we'd have seen each state (currently)
commitments = 160
odds = 1 - (1-props)**commitments
print(sum(odds), " + expected states.")

# Getting plotted projection for up to 750 commitments (with current distribution)
commit_array = np.linspace(0,750,500)
expected_states = []
for commits in commit_array:
    expected = sum(1 - (1-props)**commits)
    expected_states.append(expected)

plt.plot(commit_array, expected_states, "r", label="Expected")

# Getting plotted actual for up to current number of commitments
commit_df = pd.read_csv("../../privateData/typeform1009commits.csv")
print("Loaded in ", len(commit_df), " commitment results.")

# Cleaning states to codes
commit_state_column = commit_df["What state is your school in?"]
commit_states = get_state_codes(commit_state_column)

# Getting counter for commit states
c_count = dict(Counter(commit_states))
print(c_count)
print(len(c_count)-1, " states commited.")

# Looping through actual commitment form progress printing number of unique
actual_count = [0]
idx = [0]
for i in range(commitments):
    
    # Getting count at the current level of commitments
    current_c_count = dict(Counter(commit_states[:i+1]))
    
    # Getting rid of unknown values if present
    if "UNKNOWN" in list(current_c_count.keys()):
        del current_c_count["UNKNOWN"]
    
    # Appending actual current count to list, helper index too
    actual_count.append(len(current_c_count))
    idx.append(i)

plt.plot(idx, actual_count, "-b", label = "Actual")
plt.title("Expected State Count vs Actual by Total Commitments")
plt.legend()
plt.xlabel("Commitments")
plt.ylabel("States")
plt.show()


###########################
# Now that we have states #
# Next step is distance   #
# to school names         #
###########################
import Levenshtein

# Creating list of words to remove since variations could cause levenshtein score increases
# Don't really need general stopwords... shouldn't play a part
removal_corpus = ["high", "middle", "school", "sch", "academy", "-", "_", " h s", "jr", "sr", "/", "institute", "and", "&", "hs", "senior", "junior", "sophomore", "freshman"]

# Cleaning list comprehensions for both main list cleaning & interest list
interest_schools = [school.lower() for school in interest_df["What school are you associated with?"]]
df_schools = [school.lower() for school in df["School Name"]]

# Looping through removing corpus words (surprisingly not that slow)
for word in removal_corpus:
    interest_schools = [school.replace(word,"").strip() for school in interest_schools]
    df_schools = [school.replace(word,"").strip() for school in df_schools]
    
print(interest_schools[:30])
print(df_schools[:30])
unique_interest_schools = np.unique(interest_schools)
unique_df_schools = np.unique(df_schools)
print(len(unique_df_schools))
print(len(unique_interest_schools))

test = interest_schools[0]
simple = []
complex = []
scores = []
for school_idx in range(len(interest_schools)):
    
    school = interest_schools[school_idx]
    state_code = state_codes[school_idx].upper()
    if school in df_schools:
        
        test_codes = df["Location State"][df_schools.index(school)]
        for test_code in test_codes:
            if test_code == state_code:
                simple.append(school_idx) # Getting index matches in a list (can sum later... this is more helpful)
                continue
    else:
        score_list = [Levenshtein.distance(school,df_school) for df_school in unique_df_schools] 
        min = np.min(score_list)
        argmin = np.argmin(score_list)
        if min <= 4:
            
            test_codes = df["Location State"][df_schools.index(unique_df_schools[argmin])]
            for test_code in test_codes:
                if test_code == state_code:
                    complex.append(school_idx)
                    continue
        
print(len(simple))
print(len(complex))
#for school in df_schools:
 #   distance = Levenshtein.distance(test,school)
  #  print(distance)
  
  
  
  
  
  
  
  
  
  
  
  
  
