import pandas as pd
import surgeo

fsg = surgeo.BIFSGModel()

first_names = pd.Series(["Justin", "Joy", "Samuel", "Paxton", "Cynthia", "Allison", "Sethu"])
last_names = pd.Series(["Miller", "He", "Schirmacher", "Howard", "Wang", "Kwan", "Odayappan"])
zctas = pd.Series(['02048','02048','02048','02048','02048','02048','02048'])

fsg_results = fsg.get_probabilities(first_names, last_names, zctas)

pd.set_option('display.max_columns', None)
print(fsg_results)

### RESULTS ###
"""
   zcta5 first_name      surname     white     black       api    native  \
0  02048     JUSTIN       MILLER  0.992970  0.003365  0.000276  0.001449   
1  02048        JOY           HE  0.160106  0.001445  0.828544  0.000000   
2  02048     SAMUEL  SCHIRMACHER  0.990138  0.000519  0.003764  0.000000   
3  02048     PAXTON       HOWARD       NaN       NaN       NaN       NaN   
4  02048    CYNTHIA         WANG  0.374203  0.004109  0.558988  0.000233   
5  02048    ALLISON         KWAN  0.543685  0.002201  0.377136  0.000000   
6  02048      SETHU    ODAYAPPAN       NaN       NaN       NaN       NaN   

   multiple  hispanic  
0  0.001740  0.000200  
1  0.009360  0.000546  
2  0.001023  0.004556  
3       NaN       NaN  
4  0.061338  0.001129  
5  0.076392  0.000586  
6       NaN       NaN

"""

### TAKEAWAYS ###
"""
Surgeo seems a bit more majority-leaning than methods I've used in the past.
Not sure why the high level of confidence is given to me and sam. Maybe zip
code, but even then I've never seen any confidences of 99% plus... might
have to tune the bayesian logic that it's using.
"""
