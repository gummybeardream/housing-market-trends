# 🏡 Housing Market Dashboard

An interactive Tableau dashboard built with Zillow data (2008 - 2024) to help homebuyers to identify high growth ZIP codes, assess affordability, and observe seasonal price trends.

## Project Objective

This dashboard empowers homebuyers with data-driven insights to make informed decisions based on answers to these questions: 
- Which month/season has the highest number of active listings? lowest?
- In terms of number of sales, when is the housing market the busiest? 
- When are home prices typically at their lowest? highest?
- Which zip codes are growing fastest in value?
- Which areas fit within a specific budget using a 20% down payment rule?

## Data Source

- [Zillow Home Value Index (ZHVI)](https://www.zillow.com/research/data/)
    - Home Values by Zip Code Dataset: ZHVI All Homes (SFR, Condo/Co-Op) Times Series, Smoothed, Seasonally Adjusted($)
    - Home Values by City Dataset: ZHVI All Homes (SFR, Condo/Co-Op) Times Series, Smoothed, Seasonally Adjusted($)
    - For-Sale Listings Dataset: For-Sale Inventory (Smooth, All Homes, Monthly)
    - Sales Price Dataset: Sales Count(Nowcast, All Homes, Monthly)

## Key Features

- **Seasonal Price Trends** - Monthly home value changes over time
- **Growth Analysis** - Year-over-year price increases by zip code and city
- **Affordability Filters** - Highlights zip codes within budget range
- **Homebuyer Scenario** - Explore best areas by price, growth, and timing 

## Tech Stack

- Python (pandas, matplotlib, SQLAlchemy, dotenv)
- PostgreSQL
- Tableau
- Jupyter Notebooks

