import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Gonzague data
# Define the path to the Excel file
file_path = myconfig.root_path+"18_Rémi/"
# read from the filesystem the list of all files in the directory file_path
# Get the list of all files in the directory
files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f)) and f.endswith('.xlsx') and not f.startswith('~')]

# Initialize an empty DataFrame to hold all the data
all_data = pd.DataFrame()

# if we should make a graph 
make_graph = True


for file in files: 
    # read the data from the current sheet, from the sheet "Sheet0", starting from the 4th row
    sheet_data = pd.read_excel(file_path+file)    
    # filter out the rows with missing values in the "Services" column, or the rows with "TOTAL" values in the "Services" column
    sheet_data = sheet_data.dropna(subset=['Date'])
    # parse the date in format 28/08/2024 to 2024-08-28
    sheet_data[myconfig.field_date] = pd.to_datetime(sheet_data['Date'], format='%m/%d/%Y')

    # Append the data to the all_data DataFrame
    all_data = pd.concat([all_data, sheet_data], axis=0)


total_2024 = all_data[all_data[myconfig.field_date].dt.year == 2024]['Production kW'].sum()
print("total_2024: ", total_2024)
# chance the type of the column "Date" to datetime
# create a column "affluence" with the number of visitors per day divided by total_2024 multiplied by 100
all_data['limoges_moulinhydro_prod_base_100k'] = all_data['Production kW'] / total_2024 * 100000

# drop all columns except "date_standard" and "affluence"
all_data = all_data[[myconfig.field_date, 'limoges_moulinhydro_prod_base_100k']]
# sort by date
all_data = all_data.sort_values(myconfig.field_date, ascending=True)
# add a column "outlier" with the value 0
all_data['outlier'] = 0
# if the value of "affluence" is less than 0 then set the value of "outlier" to 1
all_data.loc[all_data['limoges_moulinhydro_prod_base_100k'] < 100, 'outlier'] = 1


if make_graph:
    # set the point color to blue if the value of "outlier" is 0, otherwise set it to red
    all_data['color'] = 'blue'
    all_data.loc[all_data['outlier'] == 1, 'color'] = 'red'
    plt.figure(figsize=(10, 6))
    plt.plot(all_data[myconfig.field_date], all_data['limoges_moulinhydro_prod_base_100k'], marker='o', linestyle='-', color='blue', label='Total Production')
    plt.title('Total Production')
    plt.xlabel('Date')
    plt.ylabel('Production')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title='Production')
    # plot the outliers
    plt.scatter(all_data[myconfig.field_date], all_data['limoges_moulinhydro_prod_base_100k'], c=all_data['color'], marker='o', s=200)
    plt.tight_layout()
    plt.savefig(file_path+"limoges_moulinhydro.png")
    plt.close()


all_data = all_data[[myconfig.field_date, 'limoges_moulinhydro_prod_base_100k']]
# rename the column "affluence" to "ancienne_poste_affluence_base100k"
all_data = all_data.rename(columns={'limoges_moulinhydro_prod_base_100k': myconfig.field_y})
# add a column "y_value" with the value 
all_data[myconfig.field_seriesname]='limoges_moulinhydro_prod_base_100k'
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
all_data.to_csv(myconfig.opendata_path+'limoges_moulinhydro.csv', index=False)
# save the public DataFrame to a CSV file
all_train_valid_data = all_data[all_data[myconfig.field_train_valid_test] != 'test']
all_train_valid_data.to_csv(myconfig.git_path+'limoges_moulinhydro.csv', index=False)

# Display the combined DataFrame
print(all_data)