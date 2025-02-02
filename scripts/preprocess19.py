import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Gonzague data
# Define the path to the Excel file
file_path = myconfig.root_path+"19_Vélos/"
file = "sample.txt"
# read the CSV file sample.txt
all_data = pd.read_csv(file_path+file, sep=';')

# if we should make a graph 
make_graph = True



# filter out the rows with missing values in the "Services" column, or the rows with "TOTAL" values in the "Services" column
all_data = all_data.dropna(subset=['Date et heure de comptage','Comptage horaire'])
all_data[myconfig.field_date] = pd.to_datetime(all_data['Date et heure de comptage'])

# change the date from a datetime to a date
all_data[myconfig.field_date] = all_data[myconfig.field_date].dt.date

# only keep the columne : Identifiant du compteur;Nom du compteur;Identifiant du site de comptage;Nom du site de comptage;Comptage horaire;Date et heure de comptage
all_data = all_data[['Nom du compteur', 'Comptage horaire', myconfig.field_date]]
# fiter out data with a Comptage horaire of 0
all_data = all_data[all_data['Comptage horaire'] > 0]

# group by date and sum the Comptahe horaire by Nom du compteur and by date
all_data = all_data.groupby([myconfig.field_date]).sum().reset_index()
print(all_data.head())

all_data[myconfig.field_date] = pd.to_datetime(all_data[myconfig.field_date])

total_2024 = all_data[all_data[myconfig.field_date].dt.year == 2024]['Comptage horaire'].sum()
print("total_2024: ", total_2024)



# chance the type of the column "Date" to datetime
# create a column "affluence" with the number of visitors per day divided by total_2024 multiplied by 100
all_data['paris_biking_base_100k'] = all_data['Comptage horaire'] / total_2024 * 100000

# drop all columns except "date_standard" and "affluence"
all_data = all_data[[myconfig.field_date, 'paris_biking_base_100k']]
# sort by date
all_data = all_data.sort_values(myconfig.field_date, ascending=True)

if make_graph:
    all_data['color'] = 'blue'
    plt.figure(figsize=(10, 6))
    plt.plot(all_data[myconfig.field_date], all_data['paris_biking_base_100k'], marker='o', linestyle='-', color='blue', label='Total Production')
    plt.title('Total Production')
    plt.xlabel('Date')
    plt.ylabel('Production')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title='Production') 
    plt.tight_layout()
    plt.savefig(file_path+"paris_biking.png")
    plt.close()


all_data = all_data[[myconfig.field_date, 'paris_biking_base_100k']]
# rename the column "affluence" to "ancienne_poste_affluence_base100k"
all_data = all_data.rename(columns={'paris_biking_base_100k': myconfig.field_y})
# add a column "y_value" with the value 
all_data[myconfig.field_seriesname]='paris_biking_base_100k'
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
all_data.to_csv(myconfig.opendata_path+'paris_biking.csv', index=False)
# save the public DataFrame to a CSV file
all_train_valid_data = all_data[all_data[myconfig.field_train_valid_test] != 'test']
all_train_valid_data.to_csv(myconfig.git_path+'paris_biking.csv', index=False)

# Display the combined DataFrame
print(all_data)