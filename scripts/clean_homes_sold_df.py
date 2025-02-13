import pandas as pd
import matplotlib.pyplot as plt

#creating a dataframe from the csv file
homes_sold_by_city = pd.read_csv('data/raw/Zillow_monthly_homes_sold_by_city.csv')

#loop to remove whitespace from columns with object datatypes
def remove_whitespace(dataframe):
    for column in dataframe.columns:
        #check datatype of each column 
        if dataframe[column].dtype == 'object':
            #apply strip function on each column
            dataframe[column] = dataframe[column].astype(str).map(str.strip)
        else:
            #if condition is false, do nothing
            pass
remove_whitespace(homes_sold_by_city)

#convert RegionID from integer to string
homes_sold_by_city['RegionID'] = homes_sold_by_city['RegionID'].astype(str)

#convert SizeRank from integer to string
homes_sold_by_city['SizeRank'] = homes_sold_by_city['SizeRank'].astype(str)

#extract city from RegionName to make a City column
homes_sold_by_city['City'] = homes_sold_by_city['RegionName'].str[:-4]

#change the first value in City and StateName columns to United States 
homes_sold_by_city.at[0, ('StateName', 'City')] = 'United States'

#transform dataset from wide to long 
homes_sold_by_city_melted = pd.melt(
    homes_sold_by_city, id_vars= ['RegionID','SizeRank','RegionName','RegionType','StateName','City'], 
    var_name='Date',
    value_name='HomesSold'
)

#convert Date column to datetime 
homes_sold_by_city_melted['Date'] = pd.to_datetime(homes_sold_by_city_melted['Date'])

#extract month from Date column
homes_sold_by_city_melted['Month'] = homes_sold_by_city_melted['Date'].dt.month

#extract year from Date column
homes_sold_by_city_melted['Year'] = homes_sold_by_city_melted['Date'].dt.year

#view dataset
print(homes_sold_by_city_melted.head(10))
print(homes_sold_by_city_melted.info())

#create a dataframe view with null values: there are about 10 rows with NaN
'''null_df = homes_sold_by_city_melted[homes_sold_by_city_melted.isnull().any(axis=1)]
print(null_df)
#To check on whether replacing 1191 null values with median/mean values will skew the data. compare both graphs
#convert HomesSold column values to int64. currently cannot convert because of NaN values '''

#check region ids. merge with sales inventory for bar graph

#plot number of HomesSold over 12 months to look at seasonal trends
#create dataframe without null values

