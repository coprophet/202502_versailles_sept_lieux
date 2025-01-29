import pandas as pd
import matplotlib.pyplot as plt

# preprocessing script for the Gonzague data

# Define the path to the Excel file
series_names=["volailler_paris","volailler_versailles"]
# create a dictionary with the file names

files = {"volailler_paris":"Tableau croisé dynamique_ELC.xlsx",
         "volailler_versailles":"Tableau croisé dynamique versailles_ELC.xlsx"}

root_file_path = r"C:\Sync\namsor Dropbox\Elian CARSENAT\0_Coprophet\8_HackathonVersailles\CommerçantsConfidentiel\TristanB"

# if we should make a graph 
make_graph = True

for series_name in series_names: 
    file = files[series_name]
    file_path = root_file_path+"\\"+file
    print("Open file: ", file_path)
    # Load each Excel file in the list
    total_ca_2024 = 0

    #excel_file = pd.ExcelFile(file_path)
    # read the data from the current sheet, from the sheet "Sheet0", starting from the 4th row
    sheet_data = pd.read_excel(file_path, sheet_name='A')
    sheet_data.head()
    # convert the date which is in the format "24/12/2019" to "2024-12-19"
    sheet_data['date'] = pd.to_datetime(sheet_data['date'], format='%d/%m/%Y')

    total_2024 = sheet_data[sheet_data['date'].dt.year == 2024]['total_ca'].sum()
    print("Total 2024: ", total_2024)

 
    # create a column "affluence" with the number of visitors per day divided by total_2024 multiplied by 100
    column_name = series_name+'_ca_ttc_base_100k'
    sheet_data[column_name] = sheet_data['total_ca'] * 100000 / total_2024 
    print(sheet_data)
    # drop all columns except "date_standard" and "affluence"
    sheet_data = sheet_data[['date', column_name]]
    # add a column train_valid_test
    sheet_data['train_valid_test'] = 'train'
    # set 'train_valid_test' to 'valid' for dates between 2024-12-01 and 2024-12-14 inclusive
    sheet_data.loc[(sheet_data['date'] >= '2024-12-01') & (sheet_data['date'] <= '2024-12-14'), 'train_valid_test'] = 'valid'
    # set 'train_valid_test' to 'test' for dates 2024-12-15 and after
    sheet_data.loc[sheet_data['date'] >= '2024-12-15', 'train_valid_test'] = 'test'
    # reorder by date ascending
    sheet_data = sheet_data.sort_values('date', ascending=True)
    # save the DataFrame to a CSV file
    sheet_data.to_csv(series_name+'.csv', index=False)

    # if make_graph: then make a graph with the total revenue per day and the number of transations per day and save it to a file
    if make_graph:
        plt.figure(figsize=(10, 6))
        plt.plot(sheet_data['date'], sheet_data[column_name], marker='o', linestyle='-', color='blue', label='Total Revenue')
        plt.title('Total Revenue Per Day')
        plt.xlabel('Date')
        plt.ylabel('Total Revenue')
        plt.grid(True)
        plt.xticks(rotation=45)
        plt.legend(title='Revenue (base 100k)')
        plt.tight_layout()
        plt.savefig(series_name+".png")
        plt.close()

    # Display the combined DataFrame
    print(sheet_data)