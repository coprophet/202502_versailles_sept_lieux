import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# preprocessing script for the Gonzague data
# Define the path to the Excel file
file_path = myconfig.extra_path+"CalendrierScolaire/"
file_name = "fr-en-calendrier-scolaire.csv"
all_data = pd.read_csv(file_path+file_name,delimiter=';')
all_data['ToDateTimeStart'] = pd.to_datetime(all_data['Date de début'], format='%Y-%m-%dT%H:%M:%S%z', utc=True)
all_data['ToDateTimeEnd'] = pd.to_datetime(all_data['Date de fin'], format='%Y-%m-%dT%H:%M:%S%z', utc=True)


zones = ['Zone A', 'Zone B', 'Zone C']
my_df = []
# for each zone
for zone in zones :
    print("zone", zone)
    # select the data for the zone
    zone_data = all_data.loc[all_data['Zones'] == zone]
    print("zone_data", zone_data)
    # iterate over all dates between 2010-01-01 and 2023-12-31 
    date = pd.to_datetime(myconfig.date_minimal, format='%Y-%m-%d', utc=True)
    date_max = pd.to_datetime(myconfig.date_split_test, format='%Y-%m-%d', utc=True)
    while date < date_max:
        date = date + pd.DateOffset(days=1)
        fr_school_is_holiday = zone_data.loc[all_data['ToDateTimeEnd'] >= date]
        fr_school_is_holiday = fr_school_is_holiday.loc[fr_school_is_holiday['ToDateTimeStart'] <= date]
        if fr_school_is_holiday.empty:
            #print("no school holiday", date)
            d = {
                myconfig.field_date : date,
                'zone' : zone,
                'vacance_scolaire' : 0
            }
            my_df.append(d)
        else:
            #print("school holiday", date)
            d = {
                myconfig.field_date : date,
                'zone' : zone,
                'vacance_scolaire' : 1
            }
            my_df.append(d)
all_data = pd.DataFrame(my_df)
print(all_data.head())

#all_data['ToDateString'] = all_data['ToDate'].dt.strftime('%Y-%m-%d')
# drop all colums except ToDateString and IsSchoolHoliday
#all_data.drop(columns={'ToDate'},inplace=True)

all_data = all_data[all_data[myconfig.field_date] <= myconfig.date_split_test]
all_data = all_data[all_data[myconfig.field_date] >= myconfig.date_minimal]
print(all_data.head())
# reorder columns 
all_data.to_csv(myconfig.git_extra_path+'vacances_scolaires.csv', index=False)
