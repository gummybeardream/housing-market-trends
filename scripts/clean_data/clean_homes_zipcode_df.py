import pandas as pd
import matplotlib.pyplot as plt

#Create a dataframe from the csv file
home_value_by_zip_code=pd.read_csv("data/raw/ZHVI_all_homes_by_zipcode.csv")

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
remove_whitespace(home_value_by_zip_code)

#Check if these two state columns match
#print(home_value_by_zip_code['StateName'].equals(home_value_by_zip_code['State']))

#Change column name from RegionID to Zipcode 
home_value_by_zip_code = home_value_by_zip_code.rename(columns={'RegionID': 'Zipcode'})

#Convert Zipcode from integer to string 
home_value_by_zip_code['Zipcode'] = home_value_by_zip_code['Zipcode'].astype(str)

#Check if the length of all zipcode values is 4 (0-4)
'''check_zipcode_list = list((home_value_by_zip_code['Zipcode'].str.len() == 5).all())
zipcode_count = check_zipcode_list.count(1)
print(zipcode_count)'''

#Convert SizeRank from integer to string 
home_value_by_zip_code['SizeRank'] = home_value_by_zip_code['SizeRank'].astype(str)

#Convert RegionName from integer to string
home_value_by_zip_code['RegionName'] = home_value_by_zip_code['RegionName'].astype(str)

#Transform dataset from wide to long data format
home_value_by_zip_code_melted = pd.melt(
    home_value_by_zip_code, 
    id_vars=['Zipcode','SizeRank','RegionName','RegionType','StateName','State','City','Metro','CountyName'], 
    var_name='Date', 
    value_name='MedianHomeValue'
    )

#Convert Date column to datetime data type
home_value_by_zip_code_melted['Date'] = pd.to_datetime(home_value_by_zip_code_melted['Date'])

#Extract month from Date column
home_value_by_zip_code_melted['Month'] = home_value_by_zip_code_melted['Date'].dt.month

#Extract year from Date column
home_value_by_zip_code_melted['Year'] = home_value_by_zip_code_melted['Date'].dt.year

#Add Country column with United States as values 
country_value = 'United States'
home_value_by_zip_code_melted['Country'] = country_value

#Create final dataframe to send to Tableau 
home_value_final = home_value_by_zip_code_melted[['Country', 'Month', 'Year', 'State', 'City', 'MedianHomeValue','Zipcode']]

#View dataset
#print(home_value_final.head(10))
#print(home_value_final.info())

#Display number of rows that have a null value
null_rows = home_value_by_zip_code_melted[home_value_by_zip_code_melted.isnull().any(axis=1)]
#print(null_rows.head(10))

#Display total number of null values and the number of nulls in each column
total_null = home_value_by_zip_code_melted.isnull().sum().sum()
#print(total_null)
null_per_column = home_value_by_zip_code_melted.isnull().sum()
#print(null_per_column)

#Display the number of rows that have null_values in the original dataframe
og_null_rows = home_value_by_zip_code[home_value_by_zip_code.isnull().any(axis=1)]
#print(og_null_rows.head(10))

#Display the total number of null values and the number of nulls in each column
og_total_null = home_value_by_zip_code.isnull().sum().sum()
#print(og_total_null)
og_null_per_column = home_value_by_zip_code.isnull().sum()
#print(og_null_per_column)

#Run to convert dataframe to csv file when dataset is ready to go to Tableau 
#home_value_final.to_csv("data/processed/home_value_final.csv")