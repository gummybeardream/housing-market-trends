import pandas as pd 
import matplotlib.pyplot as plt

#Creating a dataframe from the csv file
home_sale_prices = pd.read_csv("data/raw/Zillow_monthly_median_sales_price_by_city.csv")

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
remove_whitespace(home_sale_prices) 

#Convert RegionID from integer to string
home_sale_prices['RegionID'] = home_sale_prices['RegionID'].astype(str)

#Convert SizeRank from integer to string 
home_sale_prices['SizeRank'] = home_sale_prices['SizeRank'].astype(str)

#Extract city name from RegionName to make a City column
home_sale_prices['City'] = home_sale_prices['RegionName'].str[:-4]

#Change the first value in City and StateName columns to United States 
home_sale_prices.at[0, ('StateName','City')] = 'United States'

#Transform dataset from wide to long 
home_sale_prices_melted = pd.melt(
    home_sale_prices, id_vars= ['RegionID','SizeRank','RegionName','RegionType','StateName','City'],
    var_name= 'Date',
    value_name= 'MedianSalePrice'
)

#Convert Date column to datetime 
home_sale_prices_melted['Date'] = pd.to_datetime(home_sale_prices_melted['Date'])

#Extract month from Date column 
home_sale_prices_melted['Month'] = home_sale_prices_melted['Date'].dt.month

#Extract month name from Date column
home_sale_prices_melted['MonthName'] = home_sale_prices_melted['Date'].dt.month_name()

#Extract year from Date column
home_sale_prices_melted['Year'] = home_sale_prices_melted['Date'].dt.year

#Country column with United States as the only value
country_value = 'United States'
home_sale_prices_melted['Country'] = country_value

#View dataset
#print(home_sale_prices_melted.head(10))
#print(home_sale_prices_melted.info())

#Create a dataframe with null values 
sale_prices_null = home_sale_prices_melted[home_sale_prices_melted.isnull().any(axis=1)]
#print(sale_prices_null.head())
#print(sale_prices_null.info())

#Plot MedianSalePrice over years (2018-2024) to look at trends. Create dataframe without null values
sale_prices_no_nulls = home_sale_prices_melted.dropna()

#Create copy of dataframe with only the Year and MedianSalePrices columns
sales_prices_columns = sale_prices_no_nulls[['Year','City', 'MedianSalePrice']].copy()
#print(sales_prices_columns.groupby('Year')['MedianSalePrice'].describe())

#Dataframe showing median or average of MedianSalePrice grouped by Year 
sale_prices_by_year_median = sales_prices_columns.groupby(['City', 'Year']).median().reset_index()
sale_prices_by_year_avg = sales_prices_columns.groupby(['City', 'Year']).mean().reset_index()

#print(sale_prices_by_year_median.head(20))
#print(sale_prices_by_year_avg.head(20))

#To check on whether replacing 6410 null values with city median/mean values will skew the data



