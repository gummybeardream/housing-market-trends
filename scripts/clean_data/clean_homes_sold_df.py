import pandas as pd
import matplotlib.pyplot as plt

#Create a dataframe from the csv file
homes_sold_by_city = pd.read_csv('data/raw/Zillow_monthly_homes_sold_by_city.csv')

#Loop to remove whitespace from columns with object datatypes
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

#Convert RegionID from integer to string
homes_sold_by_city['RegionID'] = homes_sold_by_city['RegionID'].astype(str)

#Convert SizeRank from integer to string
homes_sold_by_city['SizeRank'] = homes_sold_by_city['SizeRank'].astype(str)

#Extract city from RegionName to make a City column
homes_sold_by_city['City'] = homes_sold_by_city['RegionName'].str[:-4]

#Change the first value in City and StateName columns to United States 
homes_sold_by_city.at[0, ('StateName', 'City')] = 'United States'

#Transform dataset from wide to long 
homes_sold_by_city_melted = pd.melt(
    homes_sold_by_city, id_vars= ['RegionID','SizeRank','RegionName','RegionType','StateName','City'], 
    var_name='Date',
    value_name='HomesSold'
)

#Convert Date column to datetime 
homes_sold_by_city_melted['Date'] = pd.to_datetime(homes_sold_by_city_melted['Date'])

#Extract month from Date column
homes_sold_by_city_melted['Month'] = homes_sold_by_city_melted['Date'].dt.month

#Extract year from Date column
homes_sold_by_city_melted['Year'] = homes_sold_by_city_melted['Date'].dt.year

#View dataset
#print(homes_sold_by_city_melted.head(10))
#print(homes_sold_by_city_melted.info())

#Create a dataframe with null values: there are about 10 rows with NaN
homes_sold_null = homes_sold_by_city_melted[homes_sold_by_city_melted.isnull().any(axis=1)]
print(homes_sold_null)

#Check on whether replacing 1191 null values with median/mean values will skew the data. compare both graphs
#Convert HomesSold column values to int64. currently cannot convert because of NaN values

#Plot number of HomesSold over 12 months to look at seasonal trends

#Create dataframe without null values
homes_sold_no_nulls = homes_sold_by_city_melted.dropna()

#Check if nulls were dropped
#print(homes_sold_no_nulls.info())

#Create copy of the dataframe with Month and HomesSold columns. Drop the first row 
homes_sold_barplot_columns = (homes_sold_no_nulls[['Month','HomesSold']].copy()).drop(index=0, inplace=False)

#Check if dataframe copied properly. Look at descriptive statistics 
#print(homes_sold_barplot_columns.head())
#print(homes_sold_barplot_columns.groupby('Month')['HomesSold'].describe())

#Create dataframe showing median or sum of HomesSold grouped by month 
median_homes_sold_by_month = homes_sold_barplot_columns.groupby(['Month']).median().reset_index()
total_homes_sold_by_month = homes_sold_barplot_columns.groupby(['Month']).sum().reset_index()

print(median_homes_sold_by_month.head(12))
print(total_homes_sold_by_month.head(12))


