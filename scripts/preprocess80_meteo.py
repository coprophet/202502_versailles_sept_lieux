import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Gonzague data
# Define the path to the Excel file
file_path = myconfig.extra_path+"MeteoFrance/"
file = "donnees-synop-essentielles-omm.csv"
# read the CSV file sample.txt
all_data = pd.read_csv(file_path+file, sep=';')

print(all_data.head())  

# only keep the columns "Date" and "Température (°C)" "Précipitations dans les 24 dernières heures" "Vitesse du vent moyen 10 mn (m/s)" "Nebulosité totale"
all_data = all_data[['Date', 'Température (°C)', 'Précipitations dans les 24 dernières heures', 'Vitesse du vent moyen 10 mn', 'Nebulosité totale', 'region (name)', 'department (code)']]
# filter out the rows with missing values in the region or department column
all_data = all_data.dropna(subset=['region (name)', 'department (code)'])
# filter out the rows with missing values in the temperature column
all_data = all_data.dropna(subset=['Température (°C)', 'Vitesse du vent moyen 10 mn'])
# set precipitation to 0 if missing
all_data['Précipitations dans les 24 dernières heures'] = all_data['Précipitations dans les 24 dernières heures'].fillna(0)
# set Nebulosité totale to 0 if missing
all_data['Nebulosité totale'] = all_data['Nebulosité totale'].fillna(0)
# find the columns with missing values or with non numeric values
print(all_data.isnull().sum())


# create a date_std column with the date in the format "2024-12-24" by truncating the time part from Date as string
all_data['date_std'] = all_data['Date'].str.slice(0, 10)
all_data[myconfig.field_date] = pd.to_datetime(all_data['date_std'])
# drop the column date_std
all_data = all_data.drop(columns=['date_std', 'Date'])
# average the data by date, region and department
all_data = all_data.groupby([myconfig.field_date, "region (name)", "department (code)"]).mean().reset_index()
print(all_data.head())
# keep the meteo till 2024-12-31
all_data = all_data[all_data[myconfig.field_date] <= myconfig.date_split_test]
all_data.to_csv(myconfig.git_extra_path+'france_meteo.csv', index=False)


