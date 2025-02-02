import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Kaggle competition
file_path = myconfig.opendata_path
# read from the filesystem the list of all files in the directory file_path
# Get the list of all files in the directory
files = [f for f in os.listdir(file_path) if os.path.isfile(os.path.join(file_path, f)) and f.endswith('.csv')]

# Initialize a empty DataFrames to hold all the data
all_data = pd.DataFrame()

for file in files:
    print(file)
    # read the CSV file sample.txt
    shop_data = pd.read_csv(file_path+file, sep=',')
    # check that the data has been read correctly with hearder date,y_value,series_name,train_valid_test
    print(shop_data.head())

    # append the data 
    all_data = pd.concat([all_data, shop_data], axis=0)

# create a column id with the date and the series_name
all_data[myconfig.field_id] = all_data[myconfig.field_seriesname]+"_"+all_data[myconfig.field_date].astype(str)

# check that the id is unique
print(all_data[myconfig.field_id].is_unique)
# show all cases where the id is not unique
print(all_data[all_data[myconfig.field_id].duplicated()])

all_data_train = all_data[all_data[myconfig.field_train_valid_test] == 'train']
all_data_test = all_data[all_data[myconfig.field_train_valid_test] != 'train']

# drop the columns train_valid_test from the DataFrame and only keep date,series_name,y_value in that order
all_train_data = all_data_train[[myconfig.field_id,myconfig.field_date, myconfig.field_seriesname, myconfig.field_y]]
solution_data = all_data_test[[myconfig.field_id,myconfig.field_date, myconfig.field_seriesname, myconfig.field_y, myconfig.field_train_valid_test]]
all_test_data = all_data_test[[myconfig.field_id,myconfig.field_date, myconfig.field_seriesname]]

# save the DataFrame to a CSV file for Kaggle competition
all_train_data.to_csv(myconfig.kaggle_path+'train.csv', index=False)
all_test_data.to_csv(myconfig.kaggle_path+'test.csv', index=False)

# solution for the Kaggle competition
# set the solution_data usage to public if the column train_valid_test is 'valid' 
solution_data.loc[solution_data[myconfig.field_train_valid_test] == 'valid', myconfig.field_usage] = 'Public'
solution_data.loc[solution_data[myconfig.field_train_valid_test] == 'test', myconfig.field_usage] = 'Private'
solution_data = solution_data[[myconfig.field_id, myconfig.field_usage, myconfig.field_y]]
solution_data.to_csv(myconfig.kaggle_path+'solution.csv', index=False)

solution_data[myconfig.field_y] = 100
solution_data = solution_data[[myconfig.field_id, myconfig.field_y]]
solution_data.to_csv(myconfig.kaggle_path+'sample_submission.csv', index=False)