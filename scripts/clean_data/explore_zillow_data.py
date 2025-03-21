import pandas as pd #import pandas module as pd
import matplotlib.pyplot as plt

home_value_by_zip_code=pd.read_csv("data/raw/ZHVI_all_homes_by_zipcode.csv") #creating a dataframe for Zillow Home Value Index monthly values by zip code in the US
monthly_num_homes_sold = pd.read_csv("data/raw/Zillow_monthly_homes_sold_by_city.csv") #creating a dataframe for number of homes sold each month by city 
monthly_median_sales_price = pd.read_csv("data/raw/Zillow_monthly_median_sales_price_by_city.csv") #creating a dataframe for median home sales prices by city
monthly_sales_inventory = pd.read_csv("data/raw/Zillow_monthly_sales_inventory_by_city.csv") # creating a dataframe for the number of homes for sale by city 

def zillow_data_summary(dataset_name):
    print(dataset_name.head(10))
    print(dataset_name.info(show_counts=True))
    #print(dataset_name.describe())
    #print(dataset_name.shape)
    #print(dataset_name.size)
    #print(dataset_name.columns)
    #print(dataset_name.dtypes)

#generate a summary description of a dataset by calling the function with the dataset_name
#zillow_data_summary(monthly_median_sales_price)
#zillow_data_summary(home_value_by_zip_code)
#zillow_data_summary(monthly_num_homes_sold)


#check for duplicates 
'''def check_duplicates(dataset_name):
    print(dataset_name.shape)
    print(dataset_name.drop_duplicates().shape)'''

#(home_value_by_zip_code)
#check_duplicates(monthly_num_homes_sold)
#check_duplicates(monthly_median_sales_price)
#check_duplicates(monthly_sales_inventory)

