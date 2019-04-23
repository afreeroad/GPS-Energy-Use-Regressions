### GPS Data Set
### The GOAL here is to transform the GPS individual.csv data set into a new dataframe consisting of ---
### the country names as columns, and the rows consisting of the preference data we assign.

import pandas as pd
import numpy as np

## import the data
ind_data = pd.read_csv('individual.csv')

## transform ind_data into a data frame and sort the country column alphabetically, retaining assoc. data
df_ind_data = pd.DataFrame(ind_data)
new_data = df_ind_data.sort_values(by=['country'])

## reset new_data index to 0,1,2,3...etc
new_data = new_data.reset_index(drop=True)

## create a list of the country names, alphabetically
country_list = list(ind_data['country'])
new_country_set = sorted(set(country_list))

## form a dictionary to append our data into
d = dict.fromkeys(new_country_set, [])

## since the country column of ind_data includes all 76 countries within 80000 rows, we must separate which sets of ---
## rows apply to which country, making sure the exact data for that country is chosen and transformed into the ---
## data set.
lengths = []
for country in new_country_set:
    pink = new_data.loc[(new_data['country'] == country)] #locate all rows for 'Afghanistan' (and so on)
    value = list(pink.trust) #create a list of the 'trust' data for 'Afghanistan' -- this is hard-coded...fix this
    lengths.append(len(value)) # the rows of data for each country differ, and we need to know the difference later.
max_length = max(lengths)

for country in new_country_set:
    pink = new_data.loc[(new_data['country'] == country)]
    value = list(pink.trust)
    while len(value) < max_length:  #python won't let us have columns of differing lengths, so we add in "NaN" values---
        value.append(np.NaN)        #for columns with # of rows less than the maximum.
    d[country] = value

## Create the new DataFrame and print to CSV.
data_frame = pd.DataFrame(d)
data_frame.to_csv('dataframe_copy.csv')


### ISSUES: this code is hard-coded for the 'trust' category of data. We need to create something which loops ---
### through all data categories and prints a csv with named csv i.e "dataframe_trust", dataframe_patience" et al.