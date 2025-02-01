import pandas as pd
import matplotlib.pyplot as plt

import myconfig

# preprocessing script for the Espace Richaud data
file_path = myconfig.root_path+"/1_EspaceRichaud/"
file_name = file_path+"Fréquentation journalière année par année_ELC.xlsx"

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
    sheet_data = sheet_data.dropna(subset=['DATES'])
    # filter out the rows with "TOTAL" values in the DATES column
    sheet_data = sheet_data[sheet_data['DATES'] != 'TOTAL']
    sheet_data = sheet_data[sheet_data['DATES'] != 'NOMBRE TOTAL DE VISITEURS']
    sheet_data = sheet_data[sheet_data['DATES'] != 'Total']   
    # filter out the rows with "NOMBRE DE VISITEURS" values is NaN
    sheet_data = sheet_data.dropna(subset=['NOMBRE DE VISITEURS'])
    # drop the column "TOTAL VISITEURS/SEMAINE"
    sheet_data = sheet_data.drop(columns=['TOTAL VISITEURS/SEMAINE'])
    # convert the "NOMBRE DE VISITEURS" column to integer
    sheet_data['NOMBRE DE VISITEURS'] = sheet_data['NOMBRE DE VISITEURS'].astype(int)
    sheet_data['date_standard'] = pd.to_datetime(sheet_data['DATES'], format='%A %d %B %Y')

    # sum the number of visitors for the year 2024
    total_2024 += sheet_data[sheet_data['date_standard'].dt.year == 2024]['NOMBRE DE VISITEURS'].sum()


    if make_graph:
        # make a graph with the number of visitors per day and show it, change the line color based on the column "EXPOSITION ÉVÉNEMENT"    
        unique_events = sheet_data['EXPOSITION ÉVÉNEMENT'].unique()
        colors = plt.cm.get_cmap('tab10', len(unique_events))
        plt.figure(figsize=(10, 6))
        for i, event in enumerate(unique_events):
            event_data = sheet_data[sheet_data['EXPOSITION ÉVÉNEMENT'] == event]
            plt.plot(event_data['date_standard'], event_data['NOMBRE DE VISITEURS'], marker='o', linestyle='-', color=colors(i), label=event)

        plt.title('Number of Visitors Per Day (' + sheet_name + ')')
        plt.xlabel('Date')
        plt.ylabel('Number of Visitors')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title='Exposition Événement')
        plt.tight_layout()
        # save the graph to a file with the name of the sheet
        plt.savefig(file_path+"EspaceRichaud_"+sheet_name + '.png')
        #plt.show()
        plt.close()
    

    # print(sheet_data)
    # Append the data to the all_data DataFrame
    all_data = pd.concat([all_data, sheet_data], axis=0)

# create a column "affluence" with the number of visitors per day divided by total_2024 multiplied by 100
all_data['affluence'] = all_data['NOMBRE DE VISITEURS'] / total_2024 * 100000
# filter all rows with "affluence" <= 0
all_data = all_data[all_data['affluence'] > 0]

# replace the values of column "EXPOSITION ÉVÉNEMENT" with EXPO1, EXPO2, etc.
all_data['expo'] = 'EXPO' + (all_data.groupby('EXPOSITION ÉVÉNEMENT').ngroup() + 1).astype(str)
all_data['expo'] = all_data['expo'].str.replace('.0', '')
# drop all columns except "date_standard" and "affluence"
all_data = all_data[['date_standard', 'affluence','expo']]
# convert date to a date time
all_data[myconfig.field_date] = pd.to_datetime(all_data['date_standard'])

# all_data = all_data.rename(columns={'date_standard': myconfig.field_date})
# rename the column "affluence" to "ancienne_poste_affluence_base100k"
all_data = all_data.rename(columns={'affluence': myconfig.field_y})

# add a column "y_value" with the value 
all_data[myconfig.field_seriesname]='versailles_espace_richaud_affluence_base100k'
# add a column train_valid_test
all_data[myconfig.field_train_valid_test] = 'train'
# set 'train_valid_test' to 'valid' for dates between 2024-12-01 and 2024-12-14 inclusive
all_data.loc[(all_data[myconfig.field_date] >= myconfig.date_split_train) & (all_data[myconfig.field_date] < myconfig.date_split_valid), myconfig.field_train_valid_test] = 'valid'
# set 'train_valid_test' to 'test' for dates 2024-12-15 and after
all_data.loc[all_data[myconfig.field_date] >= myconfig.date_split_valid, myconfig.field_train_valid_test] = 'test'
# remove all data after the test date
all_data = all_data[all_data[myconfig.field_date] <= myconfig.date_split_test]
# drop all columns except "date_standard" and "affluence"
all_data = all_data[[myconfig.field_date, myconfig.field_y, myconfig.field_seriesname, myconfig.field_train_valid_test, 'expo']]
# sort by date
all_data = all_data.sort_values(myconfig.field_date, ascending=True)
# save the DataFrame to a CSV file
all_data.to_csv(myconfig.opendata_path+'versailles_espace_richaud_lieuculturel.csv', index=False)

all_train_valid_data = all_data[all_data[myconfig.field_train_valid_test] != 'test']
all_train_valid_data.to_csv(myconfig.git_path+'versailles_espace_richaud_lieuculturel.csv', index=False)

# Display the combined DataFrame
print(all_data)