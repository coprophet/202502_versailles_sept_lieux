import pandas as pd
import matplotlib.pyplot as plt

import myconfig

# preprocessing script for the Les Sables-d'Olonne
file_path = myconfig.root_path+"23_PetitCommerces/"
file_name = file_path+"petitscommerces_cartescadeaux.csv"

# Initialize an empty DataFrame to hold all the data
all_data = pd.DataFrame()

total_2024 = 0

make_graph = True

# Read the data from the current sheet
all_data = pd.read_csv(file_name)

# parse the date from 2025-02-05 14:42:51.844003Z to 2025-02-05
all_data['Date1'] = all_data['inserted_at'].str.split(' ').str[0]
all_data[myconfig.field_date] = pd.to_datetime(all_data['Date1'])

all_data = all_data[[myconfig.field_date, 'amount']]
# convert the amount column to numeric
all_data['amount'] = pd.to_numeric(all_data['amount'], errors='coerce')
# sum the number of visitors for the year 2024
total_2024 = all_data[all_data[myconfig.field_date].dt.year == 2024]['amount'].sum()

print("total_2024: ", total_2024)
all_data['petitscommerces_cartescadeaux_essonne_base_100k'] = all_data['amount'] / total_2024 * 100000
all_data = all_data.groupby([myconfig.field_date]).sum().reset_index()
# sort by date
all_data = all_data.sort_values(myconfig.field_date, ascending=True)
# group by date and sum the number of transactions and the total revenue
# if make_graph: then make a graph with the total revenue per day and the number of transations per day and save it to a file
if make_graph:
    plt.figure(figsize=(10, 6))
    plt.plot(all_data[myconfig.field_date], all_data['petitscommerces_cartescadeaux_essonne_base_100k'], marker='o', linestyle='-', color='red', label='Total Revenue')
    plt.title('Total Revenue Per Day')
    plt.xlabel('Date')
    plt.ylabel('Revenue')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title='Revenue')
    plt.tight_layout()
    plt.savefig(file_path+"petitscommerces_cartescadeaux_essonne.png")
    plt.close()


# all_data = all_data.rename(columns={'date_standard': myconfig.field_date})
# rename the column "affluence" to "ancienne_poste_affluence_base100k"
all_data = all_data.rename(columns={'petitscommerces_cartescadeaux_essonne_base_100k': myconfig.field_y})

# add a column "y_value" with the value 
all_data[myconfig.field_seriesname]='petitscommerces_cartescadeaux_essonne_base_100k'
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
all_data.to_csv(myconfig.opendata_path+'petitscommerces_cartescadeaux_essonne.csv', index=False)

all_train_valid_data = all_data[all_data[myconfig.field_train_valid_test] != 'test']
all_train_valid_data.to_csv(myconfig.git_path+'petitscommerces_cartescadeaux_essonne.csv', index=False)

# Display the combined DataFrame
print(all_data)