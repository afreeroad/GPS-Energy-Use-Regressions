# GPS Dataset + World Bank GDP and Energy Use Data
This code is part of an exploratory analysis of the Global Preferences Survey (GPS), which is a worldwide survey measuring economic preferences such as risk-taking, patience, reciprocity and others. You will need to download the 'individual' dataset of the GPS from here: https://www.briq-institute.org/global-preferences/downloads

'worldbank.py' will convert the stata-based dataset into .csv form and perform a series of data cleaning methods in order to align the data with the 76 specific countries as utilized in the GPS. 

Using the World Bank API --> wbdata --> we extract various datapoints concerning these 76 countries representative of the GPS, in the categories of Gross Domestic Product (GDP) and Energy Use.

From this data, we are able to compare and observe the relations between these variables, and most importantly, see how the economic preference measures from the GPS relate to the GDP and energy use values. 

'viz_exp.py' is an example of a 3-D data visualization, depicting the relations among 3 variables. It is an extension of 'worldbank.py' and requires 'worldbank.py' to be run beforehand. 

