import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Gonzague data
# Define the path to the Excel file
file_path = myconfig.extra_path+"MeteoFrance/manual_downloads/"

# read from the filesystem the list of all files in the directory file_path
files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f)) and f.endswith('.csv')]

all_data = pd.DataFrame()
# iterate over the files in the directory
for file in files:
    # the department number is in the filename Q_75_latest-2024-2025_RR-T-Vent.csv
    # extract the department number from the filename
    department_code = file.split('_')[1]
    # read the CSV file
    file_data = pd.read_csv(file_path+file, sep=';')
    # check only keep the simplest columns
    file_data = file_data[['NUM_POSTE', 'NOM_USUEL', 'AAAAMMJJ', 'RR', 'TM', 'FFM']]
    
    # oarse the data in the column "AAAAMMJJ" to a standard date format "YYYY-MM-DD"
    file_data[myconfig.field_date] = pd.to_datetime(file_data['AAAAMMJJ'], format='%Y%m%d')
    # filter all rows with missing values in the column "RR" or "TM" or "FFM"
    file_data = file_data.dropna(subset=['RR', 'TM', 'FFM'])
    file_data['department_code'] = department_code
    print(file_data.head())  
    # Append the data to the all_data DataFrame
    all_data = pd.concat([all_data, file_data], axis=0)

all_data = all_data[[myconfig.field_date, 'department_code', 'RR', 'TM', 'FFM']]
# rename columns RR to RR_precipitaton, TM to TM_temperature, FFM to FFM_vent
all_data = all_data.rename(columns={'RR': 'RR_precipitation', 'TM': 'TM_temperature', 'FFM': 'FFM_vent'})

all_data = all_data.groupby([myconfig.field_date, 'department_code']).mean().reset_index()

print(all_data.head())
# keep the meteo till 2024-12-31
all_data = all_data[all_data[myconfig.field_date] <= myconfig.date_split_test]
all_data.to_csv(myconfig.git_extra_path+'france_meteo.csv', index=False)




    
