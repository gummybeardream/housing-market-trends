import pandas as pd
import matplotlib.pyplot as plt

#creating a dataframe from the csv file
home_value_by_zip_code=pd.read_csv("data/raw/ZHVI_all_homes_by_zipcode.csv")

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
remove_whitespace(home_value_by_zip_code)

#check if these two state columns match
#print(home_value_by_zip_code['StateName'].equals(home_value_by_zip_code['State']))

#change column name from RegionID to Zipcode 
home_value_by_zip_code = home_value_by_zip_code.rename(columns={'RegionID': 'Zipcode'})

#convert Zipcode from integer to string 
home_value_by_zip_code['Zipcode'] = home_value_by_zip_code['Zipcode'].astype(str)

#check if the length of all zipcode values is 4 (0-4)
'''check_zipcode_list = list((home_value_by_zip_code['Zipcode'].str.len() == 5).all())
zipcode_count = check_zipcode_list.count(1)
print(zipcode_count)'''

#convert SizeRank from integer to string 
home_value_by_zip_code['SizeRank'] = home_value_by_zip_code['SizeRank'].astype(str)

#convert RegionName from integer to string
home_value_by_zip_code['RegionName'] = home_value_by_zip_code['RegionName'].astype(str)

#transform dataset from wide to long data format
home_value_by_zip_code_melted = pd.melt(
    home_value_by_zip_code, 
    id_vars=['Zipcode','SizeRank','RegionName','RegionType','StateName','State','City','Metro','CountyName'], 
    var_name='Date', 
    value_name='MedianHomeValue'
    )

#convert Date column to datetime data type

#extract month from the date 
#create null dataframe view 

print(home_value_by_zip_code_melted.head(10))
print(home_value_by_zip_code_melted.info())

#should I round the number MedianHomeValue by 2 decimal places?


