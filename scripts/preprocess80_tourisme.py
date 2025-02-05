import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Gonzague data
# Define the path to the Excel file
file_path = myconfig.extra_path+"FrequentationTourisme/"
file_name = file_path+"valeurs_mensuelles.csv"

# read from the filesystem the list of all files in the directory file_path
fr_tourism = pd.read_csv(file_name, sep=";", encoding="utf-8",dtype={'idBank': str})

# define a function which takes an array of three values and redturn the DataFrame for the department with the code 78
def get_department_data(fr_tourism, department_code, series_specs):    
    fr_tourism_resident_78 = fr_tourism[fr_tourism['idBank'] == series_specs[0]]
    fr_tourism_nonresident_78 = fr_tourism[fr_tourism['idBank'] == series_specs[1]]
    fr_tourism_occupation_78 = fr_tourism[fr_tourism['idBank'] == series_specs[2]]

    fr_tourism_78 = pd.concat([fr_tourism_resident_78,fr_tourism_nonresident_78,fr_tourism_occupation_78])
    fr_tourism_78=fr_tourism_78.transpose()
    fr_tourism_78.columns = ['résident', 'non-résident','occupation']
    # remove the first three rows
    fr_tourism_78 = fr_tourism_78[3:]
    # remove the NaN values
    fr_tourism_78 = fr_tourism_78.dropna()
    # convert the data to numeric
    fr_tourism_78 = fr_tourism_78.apply(pd.to_numeric)
    # create a new column with the index string value
    fr_tourism_78[myconfig.field_date] = pd.to_datetime(fr_tourism_78.index+'-01')
    fr_tourism_78.index = fr_tourism_78[myconfig.field_date]
    print("non interpolated ", fr_tourism_78.head())
    # fill the rest of the month with interpolated values
    fr_tourism_78 = fr_tourism_78.resample('D').interpolate("linear")
    print("interpolated ", fr_tourism_78.head())
    fr_tourism_78['department_code'] = department_code
    return fr_tourism_78

fr_tourism_78=get_department_data(fr_tourism, '78', ['010598725','010598724','010599008'])
fr_tourism_75= get_department_data(fr_tourism, '75', ['010598707','010598706','010599005'])

all_data = pd.concat([fr_tourism_78, fr_tourism_75])
# normalize the data, dividing each value by the average value
all_data['occupation'] = all_data['occupation'] / 100
all_data['résident'] = all_data['résident'] / all_data['résident'].mean()
all_data['non-résident'] = all_data['non-résident'] / all_data['non-résident'].mean()

all_data = all_data[all_data[myconfig.field_date] <= myconfig.date_split_test]
# reorder columns 
all_data = all_data[[myconfig.field_date, 'department_code', 'résident', 'non-résident', 'occupation']]
all_data.to_csv(myconfig.git_extra_path+'tourisme.csv', index=False)


