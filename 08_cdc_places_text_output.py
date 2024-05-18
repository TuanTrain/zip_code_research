import pandas as pd
import os
from scipy.stats import ttest_ind

# Load the urban/rural categorization data
urban_rural_df = pd.read_csv('zip_code_urban_rural.csv', header=0, names=['zip_code', 'lat', 'long', 'urban_rural'])

# Directory where your 40 files are stored
data_files_dir = './cdc_places_data'
data_files = os.listdir(data_files_dir)

# Filter out any non-CSV files if necessary
data_files = [file for file in data_files if file.endswith('.csv')]

# Prepare a list to store results
results = []

# Iterate over each data file, merge with urban/rural data, and calculate statistics
for data_file in data_files:
    data_path = os.path.join(data_files_dir, data_file)
    data_df = pd.read_csv(data_path, header=0, names=['Year', 'zip_code', 'DataSource', 'Category', 'Measure', 'Data_Value_Unit',
        'Data_Value_Type', 'Data_Value', 'Data_Value_Footnote_Symbol', 'Data_Value_Footnote', 'Low_Confidence_Limit',
        'High_Confidence_Limit', 'TotalPopulation', 'Geolocation', 'LocationID', 'CategoryID', 'MeasureId', 'DataValueTypeID', 'Short_Question_Text'])

    # Assuming 'zip_code' is the common column in your datasets
    # Adjust column names as necessary
    merged_df = pd.merge(data_df, urban_rural_df, on='zip_code')
    
    # Calculate the p-value using t-test
    urban_data = merged_df[merged_df['urban_rural'] == 'Urban']['Data_Value']
    rural_data = merged_df[merged_df['urban_rural'] == 'Rural']['Data_Value']
    t_stat, p_value = ttest_ind(urban_data, rural_data, nan_policy='omit')
    
    # Calculate mean and standard deviation for urban and rural areas
    urban_mean = urban_data.mean()
    rural_mean = rural_data.mean()
    urban_std = urban_data.std()
    rural_std = rural_data.std()
    
    # Calculate raw difference
    raw_difference = urban_mean - rural_mean
    
    # Calculate percentage difference
    if raw_difference > 0:
        percentage_difference = (raw_difference / rural_mean) * 100
    else:
        percentage_difference = (raw_difference / urban_mean) * 100
    
    # Append the results to the list
    data_file_title = data_file.replace('_=', '>=')
    results.append({
        'File': data_file_title,
        'Urban Mean': urban_mean,
        'Rural Mean': rural_mean,
        'Urban Std': urban_std,
        'Rural Std': rural_std,
        'P-Value': p_value,
        'Raw Difference': raw_difference,
        'Percentage Difference': percentage_difference
    })

# Convert the results to a DataFrame and sort by Percentage Difference
results_df = pd.DataFrame(results)
results_df.sort_values(by='Percentage Difference', ascending=False, inplace=True)

# Save the results to a CSV file
results_df.to_csv('urban_rural_health_differences.csv', index=False)

# Display the results
print(results_df)
