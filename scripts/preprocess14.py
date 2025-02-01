import pandas as pd
import matplotlib.pyplot as plt

import myconfig

# preprocessing script for the Espace Richaud data
file_path = myconfig.root_path+"14_Renaud2/"
file_name = file_path+"RECETTES_2024_ELC.xlsx"

# Load the Excel file
excel_file = pd.ExcelFile(file_name)

# Initialize an empty DataFrame to hold all the data
all_data = pd.DataFrame()

total_2024 = 0

make_graph = True

# Iterate through each sheet in the Excel file
for sheet_name in excel_file.sheet_names:
    # Read the data from the current sheet
    sheet_data = pd.read_excel(file_name, sheet_name=sheet_name)
    # filter out the rows with missing values in the DATES column
    sheet_data = sheet_data.dropna(subset=['Dates','Total caisse'])
    # filter out the rows with "TOTAUX" values in the DATES column
    sheet_data = sheet_data[sheet_data['Dates'] != 'TOTAUX']
    # only keep Dates "Total caisse" columnes
    sheet_data = sheet_data[['Dates','Total caisse']]

    # Append the data to the all_data DataFrame
    all_data = pd.concat([all_data, sheet_data], axis=0)

all_data[myconfig.field_date] = pd.to_datetime(all_data['Dates'])

total_2024 = all_data[all_data[myconfig.field_date].dt.year == 2024]['Total caisse'].sum()

# create a column "affluence" with the number of visitors per day divided by total_2024 multiplied by 100
all_data['versailles_photoshop_ca_ttc_base_100k'] = all_data['Total caisse'] / total_2024 * 100000
# filter all rows with "affluence" <= 0
all_data = all_data[all_data['versailles_photoshop_ca_ttc_base_100k'] > 0]

if make_graph:
    plt.figure(figsize=(10, 6))
    plt.plot(all_data[myconfig.field_date], all_data['versailles_photoshop_ca_ttc_base_100k'], marker='o', linestyle='-', color='blue', label='Total Revenue')
    plt.title('Total Revenue and Number of Transactions Per Day')
    plt.xlabel('Date')
    plt.ylabel('Total Revenue / Number of Transactions')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title='Revenue / Transactions')
    plt.tight_layout()
    plt.savefig(file_path+"versailles_photoshop.png")
    plt.close()

# all_data = all_data.rename(columns={'date_standard': myconfig.field_date})
all_data = all_data.rename(columns={'versailles_photoshop_ca_ttc_base_100k': myconfig.field_y})

# add a column "y_value" with the value 
all_data[myconfig.field_seriesname]='versailles_photoshop_ca_ttc_base_100k'
# add a column train_valid_test
all_data[myconfig.field_train_valid_test] = 'train'
# set 'train_valid_test' to 'valid' for dates between 2024-12-01 and 2024-12-14 inclusive
all_data.loc[(all_data[myconfig.field_date] >= myconfig.date_split_train) & (all_data[myconfig.field_date] < myconfig.date_split_valid), myconfig.field_train_valid_test] = 'valid'
# set 'train_valid_test' to 'test' for dates 2024-12-15 and after
all_data.loc[all_data[myconfig.field_date] >= myconfig.date_split_valid, myconfig.field_train_valid_test] = 'test'
# drop all columns except "date_standard" and "affluence"
all_data = all_data[[myconfig.field_date, myconfig.field_y, myconfig.field_seriesname, myconfig.field_train_valid_test]]
# remove all data after the test date
all_data = all_data[all_data[myconfig.field_date] <= myconfig.date_split_test]
# sort by date
all_data = all_data.sort_values(myconfig.field_date, ascending=True)
# save the DataFrame to a CSV file
all_data.to_csv(myconfig.opendata_path+'versailles_photoshop.csv', index=False)

all_train_valid_data = all_data[all_data[myconfig.field_train_valid_test] != 'test']
all_train_valid_data.to_csv(myconfig.git_path+'versailles_photoshop.csv', index=False)

# Display the combined DataFrame
print(all_data)