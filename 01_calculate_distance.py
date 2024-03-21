import pandas as pd
import numpy as np

# Haversine formula to calculate distance between two lat/long points in miles
def haversine(lon1, lat1, lon2, lat2):
    # Radius of the Earth in miles
    R = 3958.8
    # Convert degrees to radians
    lon1, lat1, lon2, lat2 = map(np.radians, [lon1, lat1, lon2, lat2])
    # Difference in coordinates
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    # Haversine formula
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    distance = R * c
    return distance

# Load the data
zip_codes = pd.read_csv('zip_code_lat_long.csv')
top_500_zip_codes = pd.read_csv('zip_code_top_500_pop.csv')

# Prepare an empty DataFrame to hold the distances
distances = pd.DataFrame()

# Calculate distances from each zip code to each of the top 500 zip codes
for i, top_zip in top_500_zip_codes.iterrows():
    col_name = f"Distance_to_{top_zip['zip_code']}"
    distances[col_name] = zip_codes.apply(lambda x: haversine(top_zip['longitude'], top_zip['latitude'], x['LNG'], x['LAT']), axis=1)

# Determine urban/rural status based on distance
urban_rural = distances.min(axis=1).apply(lambda x: 'Urban' if x <= 20 else 'Rural')

# Add urban/rural classification to the zip_codes DataFrame
zip_codes['Urban_Rural'] = urban_rural

# Save or use the DataFrame as needed
# print(zip_codes.head())
output_file="zip_code_urban_rural.csv"
zip_codes.to_csv(output_file, index=False)

