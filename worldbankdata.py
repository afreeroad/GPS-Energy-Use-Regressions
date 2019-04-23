import wbdata
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime
import statsmodels.formula.api as sm
import seaborn as sns
from pprint import pprint

#import data and get country names from GPS study
data = pd.io.stata.read_stata('individual.dta')
data.to_csv('individual.csv')
df_ind_data = pd.DataFrame(data)
country_list = list(data['country'])
new_country_set = sorted(set(country_list))
#print(new_country_set)


# search wbdata and get the specific refs for the countries we are measuring
# Bosnia and South Korea names do not match between the GPS and WBData lists; causes errors,
# so, replaced names in new_country_set with those as listed in the wbdata
for idx, item in enumerate(new_country_set):
   if 'Bosnia Herzegovina' in item:
       new_country_set[idx] = 'Bosnia and Herzegovina'

for idx, item in enumerate(new_country_set):
   if 'South Korea' in item:
       new_country_set[idx] = 'Korea, Rep.'


# Sort GPS DataFrame --- 'trust' data only
new_data = df_ind_data.sort_values(by=['country'])
new_data = new_data.reset_index(drop=True)
d = dict.fromkeys(new_country_set, [])
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
data_frame = pd.DataFrame(d)

##
# Creating 'df_ex' dataframe and begin to merge and append all data:
df_ex = pd.DataFrame()
# Getting trust data from GPS dataframe
mean_trust = []
for country in data_frame:
    mean_trust.append(np.mean(data_frame[country]))
df_ex['mean_trust'] = mean_trust

# check the dictionary for available categories and associated information
# for country in new_country_set:
#     ass = wbdata.search_countries(country)
#     for key, val in ass[0].items():
#         if key == 'name':
#             print(val)
#         if key == 'region':
#             print(val)

country_name = []
iso2Code = []
region = []
income = []
for country in new_country_set:
    hoop = wbdata.search_countries(country)
    for key, val in hoop[0].items():
        if key == 'name':
            country_name.append(val)    ## We have an issue here regarding South Africa. Forced to manually change it.
        if key == 'iso2Code':
            iso2Code.append(val)
        if key == 'region':
            region.append(val['value'])
        if key == 'incomeLevel':
            income.append(val['value'])

df_ex['country'] = country_name
df_ex['iso2Code'] = iso2Code
df_ex['region'] = region
df_ex['income'] = income

df_ex['country'][58] = 'South Africa'
df_ex['iso2Code'][58] = 'ZA'
df_ex['region'][58] = 'Sub-Saharan Africa '
df_ex['income'][58] = 'Upper middle income'

# Make df_ex in alphabetical order by country
df_ex = df_ex.sort_values(by=['country'])

# with pd.option_context('display.max_rows', None, 'display.max_columns', None):
#     print(df_ex.head())


# Assign number sequence to 'region' for coloring purposes:
region_val = []
for region in df_ex['region']:
    if region == 'South Asia':
        region_val.append('.14')
    if region == 'East Asia & Pacific':
        region_val.append('.28')
    if region == 'Europe & Central Asia':
        region_val.append('.42')
    if region == 'Middle East & North Africa':
        region_val.append('.56')
    if region == 'Sub-Saharan Africa ':  #space is not a typo
        region_val.append('.7')
    if region == 'North America':
        region_val.append('.84')
    if region == 'Latin America & Caribbean ':  #space is not a typo
        region_val.append('.98')
df_ex['region_val'] = region_val

# Assign number sequence to 'income' for coloring purposes:
income_val = []
for income in df_ex['income']:
    if income == 'Lower middle income':
        income_val.append('.25')
    if income == 'Low income':
        income_val.append('.5')
    if income == 'High income':
        income_val.append('.75')
    if income == 'Upper middle income':
        income_val.append('1')
#df_ex['income_val'] = income_val



# # search indicators to find GDP per Capita $2010 and energy use and create dataframe with countries from iso2Code list and indicators
# search_ind = wbdata.search_indicators('energy use') #searched 'gdp per capita' and 'energy use'
# #pprint(search_ind)

# set the date period that I want to results of, which is 2010
ctry = list(df_ex['iso2Code'])
dates_00 = (datetime.datetime(2000, 1, 1), datetime.datetime(2000, 1, 1))
dates_10 = (datetime.datetime(2010, 1, 1), datetime.datetime(2010, 1, 1))
dates_15 = (datetime.datetime(2015, 1, 1), datetime.datetime(2015, 1, 1))

# set up the dataframe and api call for 2000 gdp per cap and energy use per cap
indicators = {'NY.GDP.PCAP.KD': 'GDPPC_2000', 'EG.USE.PCAP.KG.OE': 'EnergyUseKgOE_2000'}
df_00 = wbdata.get_dataframe(indicators, country=ctry, data_date=dates_00)
# Make df in alphabetical order by country name
df_00 = df_00.sort_values(by=['country'])

# set up the dataframe and api call for 2010 gdp per cap and energy use per cap
indicators = {'NY.GDP.PCAP.KD': 'GDPPC_2010', 'EG.USE.PCAP.KG.OE': 'EnergyUseKgOE_2010'}
df_10 = wbdata.get_dataframe(indicators, country=ctry, data_date=dates_10)
# Make df in alphabetical order by country name
df_10 = df_10.sort_values(by=['country'])

# Set up the dataframe and api call for 2015 gdp per cap and energy use per cap
# Let's not use 2015, actually, b/c 'wbdata' has too many missing values
indicators = {'NY.GDP.PCAP.KD': 'GDPPC_2015', 'EG.USE.PCAP.KG.OE': 'EnergyUseKgOE_2015'}
df_15 = wbdata.get_dataframe(indicators, country=ctry, data_date=dates_15)
# Make df in alphabetical order by country name
df_15 = df_15.sort_values(by=['country'])

# Merge all the dataframes, including df_ex:
df1 = pd.merge(df_ex, df_00, left_on='country', right_on='country')
df2 = pd.merge(df_10, df_15, left_on='country', right_on='country')
df = pd.merge(df1, df2, left_on='country', right_on='country')

# Create figures for growth rates (CAGR) over 10 years (2000-2010)
df['delta_GDPPC_CAGR'] = (((df['GDPPC_2010'] - df['GDPPC_2000']) / df['GDPPC_2000'])*100)/10
df['delta_EnergyUse_CAGR'] = (((df['EnergyUseKgOE_2010'] - df['EnergyUseKgOE_2000']) / df['EnergyUseKgOE_2000'])*100)/10

# Print the df.head()
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(df.head())

# send 'df' to CSV
df.to_csv('full_Dataframe.csv')




# # 2010 log GDP ~ log Energy Use REGRESSION
# # Setting up log variables for regression analysis and
df['log_GDPPC_2010'] = np.log(df['GDPPC_2010'])
# df['log_EnergyUse_2010'] = np.log(df['EnergyUseKgOE_2010'])
# log_x_2010 = df['log_GDPPC_2010']
# log_y_2010 = df['log_EnergyUse_2010']


# # run regression Regressors: GDP Per Capita $2010 ~ Energy Use: KgOE per Capita
# result = sm.ols(formula='log_GDPPC_2010 ~ log_EnergyUse_2010', data=df).fit()
# print(result.summary())
# # show scatter plot of normalized 2010 variables
# # plt.scatter(log_x_2010,log_y_2010)
# # log_x_2010_plot = np.linspace(0,1,10)
# # plt.plot(log_x_2010_plot, log_x_2010_plot*result.params[0] + result.params[1])
# # plt.show()
# sns.FacetGrid(df, hue='region_val', size=10).map(plt.scatter, 'log_GDPPC_2010', 'log_EnergyUse_2010').add_legend()
# sns.regplot(x='log_GDPPC_2010', y='log_EnergyUse_2010', data=df, scatter=False) # x,y need to be named after column names in  df_log
# plt.show()
#
#
# # 2000-2010 DELTA GDP ~ Energy Use REGRESSION
# df['delta_GDP'] = (df['GDPPC_2010'] - df['GDPPC_2000']) / 10
# df['delta_EnergyUse'] = (df['EnergyUseKgOE_2010'] - df['EnergyUseKgOE_2000']) / 10
# df['log_delta_GDP'] = np.log(df['delta_GDP'])
# df['log_delta_EnergyUse'] = np.log(df['delta_EnergyUse'])
#
# # plot
# sns.FacetGrid(df, hue='region_val', size=10).map(plt.scatter, 'log_delta_GDP', 'log_delta_EnergyUse').add_legend()
# sns.regplot(x='log_delta_GDP', y='log_delta_EnergyUse', data=df, scatter=False) # x,y need to be named after column names in  df_log
# plt.show()






# run regression, Regressors: GDP Per Capita $2010 ~ mean_trust
result = sm.ols(formula='log_GDPPC_2010 ~ mean_trust', data=df).fit()
print(result.summary())

sns.regplot(x='log_GDPPC_2010', y='mean_trust', data=df)
plt.show()

sns.FacetGrid(df, hue='region_val', size=10).map(plt.scatter, 'log_GDPPC_2010', 'mean_trust', s=100).add_legend()
sns.regplot(x='log_GDPPC_2010', y='mean_trust', data=df, scatter=False) # x,y need to be named after column names in  df_log
plt.show()
























































