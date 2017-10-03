
# coding: utf-8

# ## Circonscription count
# 26/09/2017
# 
# Firstly we import Pandas and other relative libraries.

# In[89]:

# If we are not using Jupyter Notebook, don't take into account the two following lines.
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# Make sure we have the pandas library previously installed.
import pandas as pd
import numpy as np


# Then we load the csv file "Indicateurs statistiques 2013 sur les circonscriptions législatives".

# In[24]:

df = pd.read_csv("indic-stat-2013-circonscriptions-legislatives.csv", skiprows = 6)
# To show some of the data frame
df.head(20)
df.tail(30)


# In[22]:

# Is there any missing value in the data frame?
# Answer: no. So we are fine.
df.isnull().values.any()

# What are the numbers of rows and columns?
df.shape
# What are the data types of the columns?
df.dtypes
# What do we have in column 'DECIR'?
df['DEPCIR']


# Now we can extract the department name, which situates always before a space concatenated by a '-', with the string method ```partition()```.
# 
# Attention: a space alone as separator won't work correctly because of i.g. "La réunion". A '-' alone won't work either because of 
# i.g. "Alpes-Maritimes". The separator ' -' is the minimum which will work.
# 
# Then we add it as a new column to the data set.

# In[69]:

df['nomDepartement'] = df['DEPCIR INTITULE'].apply(func = lambda x: x.partition(' -')[0].strip()) 
# use strip() to get rid of the problem that the entries have different numbers of spaces around the '-' sign.

df['nomDepartement']
df['nomDepartement'][1]

# Which type does the department id have ?
type(df.iloc[1, 0]) 


# Now let's define what we want to do to each column that will be later kept in our final data frame, with a dictionary structure like ```{column : action}```.
# We actually want to count the circonscription number of a department, keep its name and add up the circonscription populations of the same department for all the rest of the data frame.

# In[68]:

myKwargs = {k:sum for k in df.columns.values[2:]}
myKwargs.update({'DEPCIR INTITULE' : len, "nomDepartement" : max})
myKwargs


# Now that we have our goal action associated to each column, we simply aggregate the lines by their department, before we feed to the ```groupby()``` function our action dictionary with a ```agg()``` method.

# In[87]:

dfFinal = df.groupby(df['DEPCIR'].map(lambda No: No[:2] if len(No) == 4 else No[:3]), as_index = True).agg(myKwargs)

# The following three lines are my first tries. No need to read them.
# df.groupby(df['DEPCIR'].map(lambda No: No[:2] if len(No) == 4 else No[:3])).agg(myKwargs)[['DEPCIR INTITULE', "nomDepartement"]] 
# map(int, df['DEPCIR']) # Doesn't work! Cause there are ids like '2A01'...
# df['DEPCIR'].map(lambda No: No[:2])

# The following command can "lift" the groupby factor to a normal column.
dfFinal.reset_index(inplace=True)

# We can chnge the names of the columns.
dfFinal.columns.values[[0, -1]] = ['DepartID', 'nombreCircons']

# Now we put the columns in a more friendly order.
namesInOrder = list(dfFinal.columns.values)
namesInOrder = [namesInOrder[0]] + namesInOrder[-2:] + namesInOrder[1:-2]

# Let's see what our result looks like.
dfFinal1 = dfFinal[namesInOrder]
dfFinal1

