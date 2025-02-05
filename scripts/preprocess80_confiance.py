import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Gonzague data
# Define the path to the Excel file
file_path = myconfig.extra_path+"INSEE_Confiance/"
file_name = "23_IR_Camme_ELC.xlsx"
all_data = pd.read_excel(file_path+file_name)    
# remove the NaN values
all_data = all_data.dropna()
print(all_data.head())
all_data[myconfig.field_date] = pd.to_datetime(all_data['DATE'])
all_data.index = all_data[myconfig.field_date]
print("non interpolated ", all_data.head())
# fill the rest of the month with interpolated values
all_data = all_data.resample('D').interpolate("linear")
all_data = all_data[all_data[myconfig.field_date] <= myconfig.date_split_test]
all_data = all_data[all_data[myconfig.field_date] >= myconfig.date_minimal]
print("interpolated ", all_data.head())
# reorder columns 
all_data.to_csv(myconfig.git_extra_path+'insee_confiance.csv', index=False)


