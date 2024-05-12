import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import ttest_ind
import os

# Load the datasets
zip_code_urban_rural = pd.read_csv('zip_code_urban_rural.csv', header=0, names=['zip_code', 'lat', 'long', 'Urban_Rural'])
family_practice_cost_by_zip_code = pd.read_csv('general_surgery.csv')

# Merge the datasets on zip code
merged_data = pd.merge(family_practice_cost_by_zip_code, zip_code_urban_rural, on='zip_code')

cols = ["min_medicare_pricing_for_new_patient", 
"max_medicare_pricing_for_new_patient", 
"mode_medicare_pricing_for_new_patient", 
"min_copay_for_new_patient", 
"max_copay_for_new_patient", 
"mode_copay_for_new_patient", 
"most_utilized_procedure_code_for_new_patient", 
"min_medicare_pricing_for_established_patient", 
"max_medicare_pricing_for_established_patient", 
"mode_medicare_pricing_for_established_patient", 
"min_copay_for_established_patient", 
"max_copay_for_established_patient", 
"mode_copay_for_established_patient", 
"most_utilized_procedure_code_for_established_patient"]


for c in cols:
    # Create the violin plot
    plt.figure(figsize=(10, 6))
    sns.violinplot(x='Urban_Rural', y=c, data=merged_data)

    # Customize the plot
    plt.title('Distribution of ' + c)
    plt.xlabel('Location Type')
    plt.ylabel(c)
    plt.grid(True)

    # Show the plot
    plt.savefig("general_surgery/" + c + ".jpg")
