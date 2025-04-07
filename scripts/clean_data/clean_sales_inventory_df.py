
import pandas as pd
import matplotlib.pyplot as plt

#Create a dataframe from the csv file
sales_inventory_by_city = pd.read_csv('data/raw/Zillow_monthly_sales_inventory_by_city.csv')

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
remove_whitespace(sales_inventory_by_city) 

#Convert RegionID from integer to string
sales_inventory_by_city['RegionID'] = sales_inventory_by_city['RegionID'].astype(str)

#Convert SizeRank from integer to string
sales_inventory_by_city['SizeRank'] = sales_inventory_by_city['SizeRank'].astype(str)

#Extract city name from RegionName to make a new City column 
sales_inventory_by_city['City'] = sales_inventory_by_city['RegionName'].str[:-4]

#Change the first value in City and StateName columns to United States 
sales_inventory_by_city.at[0, ('StateName', 'City')] = 'United States'

#Transform dataset from wide to long 
sales_inventory_by_city_melted = pd.melt(
    sales_inventory_by_city, id_vars= ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'City'],
    var_name= 'Date',
    value_name='ActiveListings'
)

#Convert Date column to datetime format 
sales_inventory_by_city_melted['Date'] = pd.to_datetime(sales_inventory_by_city_melted['Date'])

#Extract month from Date column
sales_inventory_by_city_melted['Month'] = sales_inventory_by_city_melted['Date'].dt.month

#Extract month name from Date column
sales_inventory_by_city_melted['MonthName'] = sales_inventory_by_city_melted['Date'].dt.month_name()

#Extract year from Date column
sales_inventory_by_city_melted['Year'] = sales_inventory_by_city_melted['Date'].dt.year

#Add Country column with United States as the only value
country_value = 'United States'
sales_inventory_by_city_melted['Country'] = country_value

#View dataset
#print(sales_inventory_by_city_melted.head(10))
#print(sales_inventory_by_city_melted.info())

#Create a dataframe with null values
sales_inventory_null = sales_inventory_by_city_melted[sales_inventory_by_city_melted.isnull().any(axis=1)]
#print(sales_inventory_null.info())
#print(sales_inventory_null.head(10))

#Create dataframe without null values
sales_inventory_no_nulls = sales_inventory_by_city_melted.dropna()

#Check if nulls were dropped 
#print(sales_inventory_no_nulls.info())

#Convert ActiveListings values from float to whole numbers
sales_inventory_no_nulls.loc[:,'ActiveListings'] = sales_inventory_no_nulls['ActiveListings'].round().astype(int)
sales_inventory_no_nulls['ActiveListings'] = sales_inventory_no_nulls['ActiveListings'].astype(int)

#Create final dataframe to send to Tableau. Drop the first row
sales_inventory_final = sales_inventory_no_nulls[['Country', 'RegionID', 'StateName', 'City' , 'ActiveListings', 'Date', 'Month', 'MonthName', 'Year']].drop(index=0, inplace=False)
#print(sales_inventory_final.head())

#Run to convert dataframe to CSV file when dataset is ready for Tableau
#sales_inventory_final.to_csv("data/processed/sales_inventory_final.csv")

#Plot total number of ActiveListings over 12 months to look at seasonal trends
#Create copy of the dataframe with only the Month and HomesForSale columns. Drop the first row 
inventory_barplot_columns = (sales_inventory_no_nulls[['Month','ActiveListings']].copy()).drop(index=0, inplace=False)

#Descriptive statistics for sales_inventory dataset with no nulls
#print(inventory_barplot_columns.groupby('Month')['ActiveListings'].describe())

#Dateframe showing median or sum of ActiveListings grouped by month 
inventory_by_month_median = inventory_barplot_columns.groupby(['Month']).median().reset_index()
inventory_by_month_sum = inventory_barplot_columns.groupby(['Month']).sum().reset_index()

#print(inventory_by_month_sum.head(12))
#print(inventory_by_month_median.head(12))
#print(inventory_by_month.head(10))
#print(inventory_by_month.info())
#print(sales_inventory_no_nulls.head(10))
#print(sales_inventory_no_nulls.info())

#bar graph for ActiveListings trends over 12 months in a year
'''plt.bar(x=inventory_by_month['Month'], height= inventory_by_month['ActiveListings'])
plt.plot()
plt.xlabel('Month number')
plt.ylabel('Number of Homes Listed For Sale')
plt.title('Best Month to Look at Active Listings')
plt.show()'''