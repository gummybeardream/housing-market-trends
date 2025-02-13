
import pandas as pd
import matplotlib.pyplot as plt

#creating a dataframe from the csv file
sales_inventory_by_city = pd.read_csv('data/raw/Zillow_monthly_sales_inventory_by_city.csv')

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
remove_whitespace(sales_inventory_by_city) 

#convert RegionID from integer to string
sales_inventory_by_city['RegionID'] = sales_inventory_by_city['RegionID'].astype(str)

#convert SizeRank from integer to string
sales_inventory_by_city['SizeRank'] = sales_inventory_by_city['SizeRank'].astype(str)

#extract city name from RegionName to make a new City column 
sales_inventory_by_city['City'] = sales_inventory_by_city['RegionName'].str[:-4]

#change the first value in City and StateName columns to United States 
sales_inventory_by_city.at[0, ('StateName', 'City')] = 'United States'

#transform dataset from wide to long 
sales_inventory_by_city_melted = pd.melt(
    sales_inventory_by_city, id_vars= ['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName', 'City'],
    var_name= 'Date',
    value_name='HomesForSale'
)

#convert Date column to datetime format 
sales_inventory_by_city_melted['Date'] = pd.to_datetime(sales_inventory_by_city_melted['Date'])

#extract month from Date column
sales_inventory_by_city_melted['Month'] = sales_inventory_by_city_melted['Date'].dt.month

#extract year from Date column
sales_inventory_by_city_melted['Year'] = sales_inventory_by_city_melted['Date'].dt.year

#view dataset
#print(sales_inventory_by_city_melted.head(10))
#print(sales_inventory_by_city_melted.info())

#plot number of HomesForSale over 12 months to look at seasonal trends
#create dataframe without null values
sales_inventory_no_nulls = sales_inventory_by_city_melted.dropna()

#copy of the dataframe with only the Month and HomesForSale columns. drop the first row 
inventory_barplot_columns = sales_inventory_no_nulls[['Month','HomesForSale']].copy()
inventory_barplot_drop_row = inventory_barplot_columns.drop(index=0, inplace=False)
#print(inventory_barplot_drop_row.head(10))
#print(inventory_barplot_drop_row.info())
print(inventory_barplot_drop_row.groupby('Month')['HomesForSale'].describe())

#df showing the HomesForSale grouped by month 
inventory_by_month_median = inventory_barplot_drop_row.groupby(['Month']).median().reset_index()
inventory_by_month_sum = inventory_barplot_drop_row.groupby(['Month']).sum().reset_index()

#print(inventory_by_month_sum.head(12))
#print(inventory_by_month_median.head(12))

#print(inventory_by_month.head(10))
#print(inventory_by_month.info())
#print(sales_inventory_no_nulls.head(10))
#print(sales_inventory_no_nulls.info())

#create bar graph
'''plt.bar(x=inventory_by_month['Month'], height= inventory_by_month['HomesForSale'])
plt.plot()
plt.xlabel('Month number')
plt.ylabel('Number of Homes Listed For Sale')
plt.title('Best Month to Look at Home Listings')
plt.show()'''

#change numbers to more easily read millions. tableau demo. if you don't exit out of the plot, the terminal doesn't work when you run code
#plot the data each you put in 0s or median 
