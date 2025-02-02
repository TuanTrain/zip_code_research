import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.stats import ttest_ind

# Load the urban/rural categorization data
urban_rural_df = pd.read_csv('zip_code_urban_rural.csv', header=0, names=['zip_code', 'lat', 'long', 'urban_rural'])

# Directory where your 40 files are stored
data_files_dir = './cdc_places_data'
data_files = os.listdir(data_files_dir)

# Filter out any non-CSV files if necessary
data_files = [file for file in data_files if file.endswith('.csv')]

# Directory to save graphs
output_dir = 'cdc_places_data_graphs2'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Iterate over each data file, merge with urban/rural data, and create violin plots
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
    
    # Plotting
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='urban_rural', y='Data_Value', data=merged_df)
    data_file_title = data_file.replace('_=', '>=')
    plt.title(f'{data_file_title} (p-value: {p_value:.8f})')
    plt.xlabel('Area Type')
    plt.ylabel('Data Value')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, data_file + ".jpg"))
    # plt.show()
