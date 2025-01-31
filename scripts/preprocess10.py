import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Gonzague data
# Define the path to the Excel file
file_path = myconfig.root_path+"10_Sébastien1/"
# read from the filesystem the list of all files in the directory file_path
# Get the list of all files in the directory
files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f)) and f.endswith('.xlsx') and f.startswith('Z de caisse')]

# Initialize an empty DataFrame to hold all the data
all_data = pd.DataFrame()

# if we should make a graph 
make_graph = True


for file in files: 
    # read the data from the current sheet, from the sheet "Sheet0", starting from the 4th row
    sheet_data = pd.read_excel(file_path+file, sheet_name='Détails par service', skiprows=5)    
    # filter out the rows with missing values in the "Services" column, or the rows with "TOTAL" values in the "Services" column
    sheet_data = sheet_data.dropna(subset=['Services'])
    # filter out the rows "TOTAL" values in the "Services" column
    sheet_data = sheet_data[sheet_data['Services'] != 'Total']
    sheet_data['date_fr'] = sheet_data['Services'].str.extract(r'Du (\d{2}/\d{2}/\d{4})')
    # parse the date in format 28/08/2024 to 2024-08-28
    sheet_data[myconfig.field_date] = pd.to_datetime(sheet_data['date_fr'], format='%d/%m/%Y')

    # Append the data to the all_data DataFrame
    all_data = pd.concat([all_data, sheet_data], axis=0)


total_2024 = all_data[all_data[myconfig.field_date].dt.year == 2024]['Total TTC Net'].sum()
# chance the type of the column "Date" to datetime
# create a column "affluence" with the number of visitors per day divided by total_2024 multiplied by 100
all_data['versailles_restaurant2_ca_ttc_base_100k'] = all_data['Total TTC Net'] / total_2024 * 100000

# drop all columns except "date_standard" and "affluence"
all_data = all_data[[myconfig.field_date, 'versailles_restaurant2_ca_ttc_base_100k']]
# sort by date
all_data = all_data.sort_values(myconfig.field_date, ascending=True)
# if make_graph: then make a graph with the total revenue per day and the number of transations per day and save it to a file
if make_graph:
    plt.figure(figsize=(10, 6))
    plt.plot(all_data[myconfig.field_date], all_data['versailles_restaurant2_ca_ttc_base_100k'], marker='o', linestyle='-', color='blue', label='Total Revenue')
    plt.title('Total Revenue and Number of Transactions Per Day')
    plt.xlabel('Date')
    plt.ylabel('Total Revenue / Number of Transactions')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title='Revenue / Transactions')
    plt.tight_layout()
    plt.savefig(file_path+"versailles_restaurant_2.png")
    plt.close()


all_data = all_data[[myconfig.field_date, 'versailles_restaurant2_ca_ttc_base_100k']]
# rename the column "affluence" to "ancienne_poste_affluence_base100k"
all_data = all_data.rename(columns={'versailles_restaurant2_ca_ttc_base_100k': myconfig.field_y})
# add a column "y_value" with the value 
all_data[myconfig.field_seriesname]='versailles_restaurant2_ca_ttc_base_100k'
# add a column train_valid_test
all_data[myconfig.field_train_valid_test] = 'train'
# set 'train_valid_test' to 'valid' for dates between 2024-12-01 and 2024-12-14 inclusive
all_data.loc[(all_data[myconfig.field_date] >= myconfig.date_split_train) & (all_data[myconfig.field_date] < myconfig.date_split_valid), myconfig.field_train_valid_test] = 'valid'
# set 'train_valid_test' to 'test' for dates 2024-12-15 and after
all_data.loc[all_data[myconfig.field_date] >= myconfig.date_split_valid, myconfig.field_train_valid_test] = 'test'
# reorder by date ascending
all_data = all_data.sort_values(myconfig.field_date, ascending=True)


# save the DataFrame to a CSV file
all_data.to_csv(myconfig.opendata_path+'versailles_restaurant_2.csv', index=False)
# save the public DataFrame to a CSV file
all_train_valid_data = all_data[all_data[myconfig.field_train_valid_test] != 'test']
all_train_valid_data.to_csv(myconfig.git_path+'versailles_restaurant_2.csv', index=False)

# Display the combined DataFrame
print(all_data)