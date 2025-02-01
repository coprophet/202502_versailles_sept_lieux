import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Gonzague data
# Define the path to the Excel file
file_path = myconfig.root_path+"13_Renaud1/"
file_name = file_path+"Renaud_ELC.xlsx"


# Initialize an empty DataFrame to hold all the data

all_data = pd.read_excel(file_name, sheet_name='Paiements par services', skiprows=5)
# if we should make a graph 
make_graph = True


all_data['date_fr'] = all_data['DateStr'].str.extract(r'Du (\d{2}/\d{2}/\d{4})')
# parse the date in format 28/08/2024 to 2024-08-28
all_data[myconfig.field_date] = pd.to_datetime(all_data['date_fr'], format='%d/%m/%Y')

print(all_data)

total_2024 = all_data[all_data[myconfig.field_date].dt.year == 2024]['CA Total'].sum()
# chance the type of the column "Date" to datetime
# create a column "affluence" with the number of visitors per day divided by total_2024 multiplied by 100
all_data['versailles_restaurant3_ca_ttc_base_100k'] = all_data['CA Total'] / total_2024 * 100000

# drop all columns except "date_standard" and "affluence"
all_data = all_data[[myconfig.field_date, 'versailles_restaurant3_ca_ttc_base_100k']]
# sort by date
all_data = all_data.sort_values(myconfig.field_date, ascending=True)
# if make_graph: then make a graph with the total revenue per day and the number of transations per day and save it to a file
if make_graph:
    plt.figure(figsize=(10, 6))
    plt.plot(all_data[myconfig.field_date], all_data['versailles_restaurant3_ca_ttc_base_100k'], marker='o', linestyle='-', color='blue', label='Total Revenue')
    plt.title('Total Revenue and Number of Transactions Per Day')
    plt.xlabel('Date')
    plt.ylabel('Total Revenue / Number of Transactions')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title='Revenue / Transactions')
    plt.tight_layout()
    plt.savefig(file_path+"versailles_restaurant_3.png")
    plt.close()


all_data = all_data[[myconfig.field_date, 'versailles_restaurant3_ca_ttc_base_100k']]
# rename the column "affluence" to "ancienne_poste_affluence_base100k"
all_data = all_data.rename(columns={'versailles_restaurant3_ca_ttc_base_100k': myconfig.field_y})
# add a column "y_value" with the value 
all_data[myconfig.field_seriesname]='versailles_restaurant3_ca_ttc_base_100k'
# add a column train_valid_test
all_data[myconfig.field_train_valid_test] = 'train'
# set 'train_valid_test' to 'valid' for dates between 2024-12-01 and 2024-12-14 inclusive
all_data.loc[(all_data[myconfig.field_date] >= myconfig.date_split_train) & (all_data[myconfig.field_date] < myconfig.date_split_valid), myconfig.field_train_valid_test] = 'valid'
# set 'train_valid_test' to 'test' for dates 2024-12-15 and after
all_data.loc[all_data[myconfig.field_date] >= myconfig.date_split_valid, myconfig.field_train_valid_test] = 'test'
# remove all data after the test date
all_data = all_data[all_data[myconfig.field_date] <= myconfig.date_split_test]
# reorder by date ascending
all_data = all_data.sort_values(myconfig.field_date, ascending=True)


# save the DataFrame to a CSV file
all_data.to_csv(myconfig.opendata_path+'versailles_restaurant_3.csv', index=False)
# save the public DataFrame to a CSV file
all_train_valid_data = all_data[all_data[myconfig.field_train_valid_test] != 'test']
all_train_valid_data.to_csv(myconfig.git_path+'versailles_restaurant_3.csv', index=False)

# Display the combined DataFrame
print(all_data)