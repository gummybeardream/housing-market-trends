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

#Drop rows if United States is a value in the StateName or City column
home_sale_prices_melted = home_sale_prices_melted[~(home_sale_prices_melted['StateName'].str.contains(country_value, na=False) | home_sale_prices_melted['City'].str.contains(country_value, na=False))]

#Validate that StateName column does not contain United States as a value
check_state_column = home_sale_prices_melted[home_sale_prices_melted['StateName'].str.contains('United States')]
#print(check_state_column.info())
#print(check_state_column.head(10))

#Validate that City column does not contain United States as a value
check_city_column = home_sale_prices_melted[home_sale_prices_melted['City'].str.contains('United States')]
#print(check_city_column.info())
#print(check_city_column.head(10))

#View dataset
#print(home_sale_prices_melted.head(10))
#print(home_sale_prices_melted.info())

#Create dataframe without null values
sale_prices_no_nulls = home_sale_prices_melted.dropna()
#print(sale_prices_no_nulls.head())
#print(sale_prices_no_nulls.info())

#Create final dataframe to send to Tableau
sale_prices_final = sale_prices_no_nulls[['Country', 'RegionID', 'StateName', 'City', 'MedianSalePrice', 'Date', 'Month', 'MonthName', 'Year']]
#print(sale_prices_final.info())
#print(sale_prices_final.head())

#Run to convert dataframe to CSV file when dataset is ready for Tableau
#sale_prices_final.to_csv("data/processed/sale_prices_final.csv")

#Null dataset analysis 
#Create a dataframe with null values 
sale_prices_null = home_sale_prices_melted[home_sale_prices_melted.isnull().any(axis=1)]

#Count total expected city-month combinations
total_city_month_counts = home_sale_prices_melted.groupby(['City', 'MonthName'])\
    .size()\
    .reset_index(name='CityMonthRows')\
    .sort_values(by= 'CityMonthRows', ascending= False)
print(total_city_month_counts.info())
print(total_city_month_counts.head(10))
print(total_city_month_counts.shape)
print(total_city_month_counts['CityMonthRows'].describe())
print(total_city_month_counts.duplicated(subset=['City', 'MonthName']).sum())

#Count nulls per city-month combination
nulls_by_city_month = sale_prices_null\
    .groupby(['City','MonthName'])\
    .size()\
    .reset_index(name= 'NullCityMonth')\
    .sort_values(by = 'NullCityMonth', ascending =False)
print(nulls_by_city_month.info())
print(nulls_by_city_month.head(15))
print(nulls_by_city_month.shape)
print(nulls_by_city_month['NullCityMonth'].describe())
print(nulls_by_city_month.isna().sum())

#Merge and compare total and null city combination lists to filter for combinations that are completely missing 
city_month_check = pd.merge(total_city_month_counts, nulls_by_city_month, on = ['City', 'MonthName'], how='left')
#print(city_month_check.head(20))

#Fill NaN with zeros to easily which city-month combos are not missing
city_month_check['NullCityMonth'] = city_month_check['NullCityMonth'].fillna(0)

#Identify city-month combos that are fully missing by adding a True/False Column 
city_month_check['AllMissing'] = city_month_check['NullCityMonth'] == city_month_check['CityMonthRows']
print(city_month_check.head(20))

#Filter out only fully missing city-month combos
completely_missing_combos = city_month_check[city_month_check['AllMissing']]
print(completely_missing_combos.info())


#Create dataframe of nulls grouped by month
nulls_by_month = sale_prices_null\
    .groupby('Month')\
    .size()\
    .reset_index(name='MissingValues')
#print(nulls_by_month)

#Create dataframe of nulls grouped by state 
nulls_by_state = sale_prices_null\
    .groupby('StateName')\
    .size()\
    .reset_index(name='MissingValues')\
    .sort_values(by='MissingValues', ascending =False)
#print(nulls_by_state.info(show_counts=True))

#Create dataframe of nulls grouped by state and city
nulls_by_state_city = sale_prices_null\
    .groupby(['StateName','City'])\
    .size()\
    .reset_index(name='MissingValues')\
    .sort_values(by= 'MissingValues', ascending=False)
#print(nulls_by_state_city.info(show_counts=True))

#print(sale_prices_null.head())
#print(sale_prices_null.info())
#To check on whether replacing 6410 null values with city median/mean values will skew the data



