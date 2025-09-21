import pandas as pd

# Load the pivoted data
df_pivoted = pd.read_csv('normalized_heatmap_data.csv')

# The melt function requires the index to be a column, so we'll reset it.
# The 'mutation' column is often loaded as the index, so we'll treat the first column as such.
df_pivoted = df_pivoted.rename(columns={df_pivoted.columns[0]: 'mutation'})

# Use pd.melt() to unpivot the DataFrame.
# 'id_vars' are the columns you want to keep as is (the mutation IDs).
# 'var_name' is the new column for the old column headers (the experiment IDs).
# 'value_name' is the new column for the cell values (the Z-scores).
df_unpivoted = pd.melt(
    df_pivoted,
    id_vars=['mutation'],
    var_name='experiment_id',
    value_name='z_score'
)

# Display a sample of the unpivoted data
print("Unpivoted DataFrame (first 5 rows):")
print(df_unpivoted.head())

# Save the unpivoted DataFrame to a new CSV file
df_unpivoted.to_csv("unpivoted_data.csv", index=False)
print("\nSuccessfully unpivoted data and saved to 'unpivoted_data.csv'")

#a NaN/empty cell in the z_score column means that a specific mutation was not observed
# in that particular experiment. This is a common occurrence when dealing with
# large-scale experimental data where not every possible mutation is tested or
# found in every experiment.
