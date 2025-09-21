"""
Imputation Pipeline
==================

This module handles missing value imputation:
1. Apply KNN imputation to fill missing values
2. Handle sparse data effectively
3. Maintain biological relevance

Methodology:
- KNN imputation: Uses k=5 nearest neighbors based on validation
- Focus on well-covered mutations (≥5 experiments)
- Maintains z-score distribution properties
"""

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
import json

def load_validation_results():
    """Load validation results to get best parameters."""
    with open('validation_results.json', 'r') as f:
        return json.load(f)

def perform_knn_imputation(df, n_neighbors=5):
    """
    Perform KNN imputation on well-covered mutations.
    
    Args:
        df (pd.DataFrame): Well-covered data
        n_neighbors (int): Number of neighbors for KNN
    
    Returns:
        pd.DataFrame: Imputed data
    """
    mutation_coverage = df.count(axis=1)
    well_covered_mask = mutation_coverage >= 5
    well_covered_df = df[well_covered_mask]
    
    print(f"Imputing {len(well_covered_df)} mutations across {len(well_covered_df.columns)} experiments")
    
    imputer = KNNImputer(n_neighbors=n_neighbors)
    imputed_data = imputer.fit_transform(well_covered_df)
    imputed_df = pd.DataFrame(imputed_data, 
                             index=well_covered_df.index, 
                             columns=well_covered_df.columns)
    
    print(f"Imputation complete!")
    print(f"Final coverage: {imputed_df.count().sum() / imputed_df.size * 100:.1f}%")
    print(f"Value range: {imputed_df.min().min():.3f} to {imputed_df.max().max():.3f}")
    print(f"Mean: {imputed_df.mean().mean():.3f}")
    print(f"Std: {imputed_df.std().mean():.3f}")
    
    return imputed_df

def validate_imputation_quality(original_df, imputed_df):
    """
    Validate imputation quality by comparing statistics.
    
    Args:
        original_df (pd.DataFrame): Original data with missing values
        imputed_df (pd.DataFrame): Imputed data
    
    Returns:
        dict: Quality metrics
    """
    # Focus on well-covered mutations only
    mutation_coverage = original_df.count(axis=1)
    well_covered_mask = mutation_coverage >= 5
    well_covered_original = original_df[well_covered_mask]
    
    # Compare known values
    known_mask = ~well_covered_original.isnull()
    known_values = well_covered_original[known_mask].values.flatten()
    imputed_known = imputed_df[known_mask].values.flatten()
    
    # Calculate correlation
    valid_mask = ~(np.isnan(known_values) | np.isnan(imputed_known))
    if valid_mask.sum() > 0:
        correlation = np.corrcoef(known_values[valid_mask], imputed_known[valid_mask])[0, 1]
    else:
        correlation = 0.0
    
    # Calculate statistics
    quality_metrics = {
        'correlation': correlation,
        'original_mean': well_covered_original[known_mask].mean().mean(),
        'imputed_mean': imputed_df.mean().mean(),
        'original_std': well_covered_original[known_mask].std().mean(),
        'imputed_std': imputed_df.std().mean()
    }
    
    print(f"\nImputation Quality Validation:")
    print(f"  Correlation with known values: {quality_metrics['correlation']:.3f}")
    print(f"  Mean preservation: {quality_metrics['original_mean']:.3f} → {quality_metrics['imputed_mean']:.3f}")
    print(f"  Std preservation: {quality_metrics['original_std']:.3f} → {quality_metrics['imputed_std']:.3f}")
    
    return quality_metrics

def main():
    """Main imputation pipeline."""
    print("=== IMPUTATION PIPELINE ===")
    
    # Load data
    df = pd.read_csv('normalized_heatmap_data.csv', index_col=0)
    
    # Load validation results
    validation_results = load_validation_results()
    best_n_neighbors = validation_results['best_knn_params']['n_neighbors']
    
    # Perform imputation
    imputed_df = perform_knn_imputation(df, best_n_neighbors)
    
    # Validate quality
    quality_metrics = validate_imputation_quality(df, imputed_df)
    
    # Save results
    imputed_df.to_csv('imputed_data.csv')
    
    # Save quality metrics
    with open('imputation_quality.json', 'w') as f:
        json.dump(quality_metrics, f, indent=2)
    
    print("\nSaved imputed_data.csv and imputation_quality.json")
    return imputed_df

if __name__ == "__main__":
    main()
