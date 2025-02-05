import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Gonzague data
# Define the path to the Excel file
file_path = myconfig.extra_path+"JoursFériésFrance/"
file_name = "jours_feries_metropole.csv"

all_data = pd.read_csv(file_path+file_name,delimiter=',')
all_data['ToDateTime'] = pd.to_datetime(all_data['date'], format='%Y-%m-%d', utc=True)
all_data['ToDate'] = all_data['ToDateTime'].dt.date
all_data['ToDateString'] = all_data['ToDateTime'].dt.strftime('%Y-%m-%d')
all_data['jour_ferie'] = 1
print(all_data.head())
# drop all colums except ToDateString and IsHoliday
all_data[myconfig.field_date] = pd.to_datetime(all_data['ToDateString'])
all_data.drop(columns={'ToDateString','annee','zone','nom_jour_ferie','ToDateTime','ToDate'},inplace=True)

all_data = all_data[all_data[myconfig.field_date] <= myconfig.date_split_test]
all_data = all_data[all_data[myconfig.field_date] >= myconfig.date_minimal]
print(all_data.head())
# reorder columns 
all_data.to_csv(myconfig.git_extra_path+'jours_ferie.csv', index=False)

