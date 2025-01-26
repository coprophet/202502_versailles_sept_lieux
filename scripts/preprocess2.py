import pandas as pd
import matplotlib.pyplot as plt

# preprocessing script for the Gonzague data

# Define the path to the Excel file
files = ["Zettle-Raw-Data-Report-20240101-20241231.xlsx","Zettle-Raw-Data-Report-20230101-20231231.xlsx","Zettle-Raw-Data-Report-20220101-20221231.xlsx"]
root_file_path = r"C:\Sync\namsor Dropbox\Elian CARSENAT\0_Coprophet\8_HackathonVersailles\CommerçantsConfidentiel\Gonzague"

# Initialize an empty DataFrame to hold all the data
all_data = pd.DataFrame()

# if we should make a graph 
make_graph = True

# Load each Excel file in the list
total_ca_2024 = 0
total_aff_2024 = 0

for file in files: 
    file_path = root_file_path+"\\"+file
    #excel_file = pd.ExcelFile(file_path)
    # read the data from the current sheet, from the sheet "Sheet0", starting from the 4th row
    sheet_data = pd.read_excel(file_path, sheet_name='Sheet0', skiprows=5)
    sheet_data.head()
    # convert the date which is in the format "2024-01-01 00:00:00" to "2024-01-01"
    sheet_data['Date'] = sheet_data['Date'].dt.date

    # group the data by the "Date" column and sum the "Prix final (EUR)" column and count the number of transactions
    sheet_data = sheet_data.groupby('Date').agg({'Prix final (EUR)': 'sum', 'Reçu n°': 'count'}).reset_index()

    # calculate the total revenue for the year 2024
    if( total_ca_2024 == 0):
        total_ca_2024 += sheet_data['Prix final (EUR)'].sum()
    if( total_aff_2024 == 0):
        total_aff_2024 += sheet_data['Reçu n°'].sum()

    # print(sheet_data)
    # Append the data to the all_data DataFrame
    all_data = pd.concat([all_data, sheet_data], axis=0)

# chance the type of the column "Date" to datetime
all_data['Date'] = pd.to_datetime(all_data['Date']) 
# create a column "affluence" with the number of visitors per day divided by total_2024 multiplied by 100
all_data['onenation_shop_ca_ttc_base_100k'] = all_data['Prix final (EUR)'] / total_ca_2024 * 100000
all_data['onenation_shop_affluence_base100k'] = all_data['Reçu n°'] / total_aff_2024 * 100000
# rename column "Reçu n°" to "transactions" and column Date to date
all_data = all_data.rename(columns={'Date': 'date'})
# drop all columns except "date_standard" and "affluence"
all_data = all_data[['date', 'onenation_shop_ca_ttc_base_100k','onenation_shop_affluence_base100k']]
# add a column train_valid_test
all_data['train_valid_test'] = 'train'
# set 'train_valid_test' to 'valid' for dates between 2024-12-01 and 2024-12-14 inclusive
all_data.loc[(all_data['date'] >= '2024-12-01') & (all_data['date'] <= '2024-12-14'), 'train_valid_test'] = 'valid'
# set 'train_valid_test' to 'test' for dates 2024-12-15 and after
all_data.loc[all_data['date'] >= '2024-12-15', 'train_valid_test'] = 'test'
# reorder by date ascending
all_data = all_data.sort_values('date', ascending=True)
# save the DataFrame to a CSV file
all_data.to_csv('onenation_shop.csv', index=False)

# if make_graph: then make a graph with the total revenue per day and the number of transations per day and save it to a file
if make_graph:
    plt.figure(figsize=(10, 6))
    plt.plot(all_data['date'], all_data['onenation_shop_ca_ttc_base_100k'], marker='o', linestyle='-', color='blue', label='Total Revenue')
    plt.plot(all_data['date'], all_data['onenation_shop_affluence_base100k'], marker='o', linestyle='-', color='red', label='Number of Transactions')
    plt.title('Total Revenue and Number of Transactions Per Day')
    plt.xlabel('Date')
    plt.ylabel('Total Revenue / Number of Transactions')
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.legend(title='Revenue / Transactions')
    plt.tight_layout()
    plt.savefig("onenation_shop.png")
    plt.close()

# Display the combined DataFrame
print(all_data)