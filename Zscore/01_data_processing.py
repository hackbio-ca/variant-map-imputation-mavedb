"""
Data Processing Pipeline
=======================

This module handles the initial data processing steps:
1. Load raw CSV files from SPTAN1Data/
2. Parse HGVS protein notation
3. Calculate z-scores within each experiment
4. Create normalized heatmap data

Methodology:
- Z-score normalization: (value - mean) / std within each experiment
- This enables comparison across different experimental conditions
- HGVS parsing extracts individual mutations from complex notation
"""

import pandas as pd
import glob
import os
import numpy as np

def parse_hgvs_pro(hgvs_string):
    """
    Parse HGVS protein notation to extract individual mutations.
    
    Args:
        hgvs_string (str): HGVS protein notation (e.g., "p.[Val57Gln;Tyr9Pro]")
    
    Returns:
        list: List of individual mutations
    """
    if pd.isna(hgvs_string) or hgvs_string == 'p.=':
        return []
    
    mutations = hgvs_string.replace('p.[', '').replace(']', '').split(';')
    return [m.strip() for m in mutations if m.strip()]

def load_raw_data(data_dir="../SPTAN1Data/"):
    """
    Load all raw CSV files from the data directory.
    
    Args:
        data_dir (str): Path to directory containing CSV files
    
    Returns:
        pd.DataFrame: Combined dataframe with experiment_id column
    """
    all_files = glob.glob(os.path.join(data_dir, "*.csv"))
    
    if not all_files:
        raise FileNotFoundError(f"No CSV files found in {data_dir}")
    
    list_of_dfs = []
    for file_path in all_files:
        df = pd.read_csv(file_path)
        df['experiment_id'] = os.path.basename(file_path).split('.')[0]
        list_of_dfs.append(df)
    
    combined_df = pd.concat(list_of_dfs, ignore_index=True)
    print(f"Loaded {len(all_files)} files with {len(combined_df)} total rows")
    
    return combined_df

def process_mutations(df):
    """
    Process HGVS notation and explode mutations.
    
    Args:
        df (pd.DataFrame): Raw data with hgvs_pro column
    
    Returns:
        pd.DataFrame: Processed data with individual mutations
    """
    df['mutation_list'] = df['hgvs_pro'].apply(parse_hgvs_pro)
    df_exploded = df.explode('mutation_list')
    df_exploded.rename(columns={'mutation_list': 'mutation'}, inplace=True)
    df_exploded.dropna(subset=['mutation'], inplace=True)
    
    print(f"Exploded to {len(df_exploded)} mutation rows")
    return df_exploded

def calculate_z_scores(df):
    """
    Calculate z-scores within each experiment.
    
    Args:
        df (pd.DataFrame): Data with score and experiment_id columns
    
    Returns:
        pd.DataFrame: Data with z_score column
    """
    df['z_score'] = df.groupby('experiment_id')['score'].transform(
        lambda x: (x - x.mean()) / x.std()
    )
    
    print("Calculated z-scores within each experiment")
    return df

def create_heatmap_data(df):
    """
    Create pivoted heatmap data for visualization.
    
    Args:
        df (pd.DataFrame): Data with mutation, experiment_id, and z_score columns
    
    Returns:
        pd.DataFrame: Pivoted heatmap data
    """
    heatmap_data = df.pivot_table(
        index='mutation', 
        columns='experiment_id', 
        values='z_score', 
        aggfunc='mean'
    )
    
    print(f"Created heatmap data: {heatmap_data.shape}")
    print(f"Coverage: {heatmap_data.count().sum() / heatmap_data.size * 100:.2f}%")
    
    return heatmap_data

def main():
    """Main data processing pipeline."""
    print("=== DATA PROCESSING PIPELINE ===")
    
    # Load raw data
    df = load_raw_data()
    
    # Process mutations
    df_processed = process_mutations(df)
    
    # Calculate z-scores
    df_scored = calculate_z_scores(df_processed)
    
    # Create heatmap data
    heatmap_data = create_heatmap_data(df_scored)
    
    # Save results
    heatmap_data.to_csv("normalized_heatmap_data.csv")
    print("Saved normalized_heatmap_data.csv")
    
    return heatmap_data

if __name__ == "__main__":
    main()
