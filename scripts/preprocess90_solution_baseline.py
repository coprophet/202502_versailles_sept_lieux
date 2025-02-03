import pandas as pd
import matplotlib.pyplot as plt
import myconfig
import os

# Load the training and test data
train_df = pd.read_csv(myconfig.git_kaggle_path+'train.csv', parse_dates=[myconfig.field_date])
test_df = pd.read_csv(myconfig.git_kaggle_path+'test.csv', parse_dates=[myconfig.field_date])

# Compute moving average (last 30 days revenue per shop)
train_df = train_df.sort_values(by=[myconfig.field_seriesname, myconfig.field_date])  # Ensure chronological order
train_df["moving_avg"] = train_df.groupby(myconfig.field_seriesname)[myconfig.field_y].transform(lambda x: x.rolling(window=30, min_periods=1).mean())

# Get the most recent moving average for each shop
latest_avg = train_df.groupby(myconfig.field_seriesname)["moving_avg"].last().reset_index()
latest_avg.rename(columns={"moving_avg": myconfig.field_y}, inplace=True)

# Merge with test data to create predictions
solution_df = test_df.merge(latest_avg, on=myconfig.field_seriesname, how="left")

# Create a unique ID
solution_df[myconfig.field_id] = solution_df[myconfig.field_seriesname]+"_"+solution_df[myconfig.field_date].astype(str)

# Reorder columns to match expected output
solution_df = solution_df[[myconfig.field_id, myconfig.field_y]]

# Save the solution file
solution_df.to_csv(myconfig.git_kaggle_path+"baseline_solution.csv", index=False)

print("✅ Baseline solution.csv generated successfully!")