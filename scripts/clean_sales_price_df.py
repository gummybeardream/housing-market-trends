import pandas as pd 
import matplotlib.pyplot as plt

#creating a dataframe from the csv file
home_sale_prices = pd.read_csv("data/raw/Zillow_monthly_sales_inventory_by_city.csv")

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
remove_whitespace(home_sale_prices) 

#convert RegionID from integer to string
home_sale_prices['RegionID'] = home_sale_prices['RegionID'].astype(str)

#convert SizeRank from integer to string 
home_sale_prices['SizeRank'] = home_sale_prices['SizeRank'].astype(str)

#extract city name from RegionName to make a City column
home_sale_prices['City'] = home_sale_prices['RegionName'].str[:-4]

#change the first value in City and StateName columns to United States 
home_sale_prices.at[0, ('StateName','City')] = 'United States'

#transform dataset from wide to long 
home_sale_prices_melted = pd.melt(
    home_sale_prices, id_vars= ['RegionID','SizeRank','RegionName','RegionType','StateName','City'],
    var_name= 'Date',
    value_name= 'MedianSalePrice'
)

#Convert Date column to datetime 
home_sale_prices_melted['Date'] = pd.to_datetime(home_sale_prices_melted['Date'])

#Extract month from Date column 
home_sale_prices_melted['Month'] = home_sale_prices_melted['Date'].dt.month

#Extract year from Date column
home_sale_prices_melted['Year'] = home_sale_prices_melted['Date'].dt.year

#view dataset
print(home_sale_prices_melted.head(10))
print(home_sale_prices_melted.info())

#To check on whether replacing 1191 null values with median/mean values will skew the data. compare both graphs 
#dig into which locations we are missing data from
#Reorder the columns at the end with a new df name.

