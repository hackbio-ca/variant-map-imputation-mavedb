import pandas as pd
import glob
import os

# Create a list of the files to process. Replace this with a glob pattern for all 42 files.
# For example: all_files = glob.glob(os.path.join("path/to/your/files/", "*.csv"))
all_files = glob.glob(os.path.join("/Users/cynthiabts/Downloads/MaveDBSPTAN1", "*.csv"))

# Create an empty list to store the dataframes
list_of_dfs = []

# Loop through each file and add an 'experiment_id' column
for file_path in all_files:
    df = pd.read_csv(file_path)
    # Extract a unique identifier from the filename to serve as the experiment ID
    df['experiment_id'] = os.path.basename(file_path).split('.')[0]
    list_of_dfs.append(df)

# Concatenate all dataframes into a single dataframe
combined_df = pd.concat(list_of_dfs, ignore_index=True)

# Function to parse the hgvs_pro string and return all mutations
def parse_hgvs_pro(hgvs_string):
    if pd.isna(hgvs_string) or hgvs_string == 'p.=':
        return []
    # Remove the 'p.' and surrounding brackets, then split by semicolon
    mutations = hgvs_string.replace('p.[', '').replace(']', '').split(';')
    return [m.strip() for m in mutations if m.strip()]

# Apply the parsing function
combined_df['mutation_list'] = combined_df['hgvs_pro'].apply(parse_hgvs_pro)

# Use .explode() to create a new row for each mutation
df_exploded = combined_df.explode('mutation_list')

# Rename the column for clarity
df_exploded.rename(columns={'mutation_list': 'mutation'}, inplace=True)

# Drop rows with no mutation info after the explosion
df_exploded.dropna(subset=['mutation'], inplace=True)

# Calculate the Z-score for the 'score' column, grouped by experiment
df_exploded['z_score'] = df_exploded.groupby('experiment_id')['score'].transform(lambda x: (x - x.mean()) / x.std())

# Pivot the data to get it in the correct format for a heatmap
# Rows are mutations, columns are experiments, and values are the normalized scores
heatmap_data = df_exploded.pivot_table(index='mutation', columns='experiment_id', values='z_score', aggfunc='mean')

# Print the resulting DataFrame which is ready for a heatmap
print("DataFrame for Heatmap (first 5 rows):")
print(heatmap_data.head())

# Save the data to a CSV file for your use
heatmap_data.to_csv("normalized_heatmap_data.csv")
print("\nSaved normalized data to 'normalized_heatmap_data.csv'")
