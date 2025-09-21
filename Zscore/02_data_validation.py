"""
Data Validation Pipeline
=======================

This module validates data quality and imputation parameters:
1. Analyze data coverage and quality
2. Identify well-covered mutations
3. Validate KNN imputation parameters
4. Perform cross-validation

Methodology:
- Well-covered mutations: ≥5 experiments (23.24% coverage)
- Cross-validation: Hide 20% of known values, test imputation accuracy
- Quality metrics: MSE and R² for imputation validation
"""

import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.metrics import mean_squared_error, r2_score

def analyze_data_coverage(df):
    """
    Analyze data coverage and identify well-covered mutations.
    
    Args:
        df (pd.DataFrame): Normalized heatmap data
    
    Returns:
        tuple: (well_covered_df, coverage_stats)
    """
    mutation_coverage = df.count(axis=1)
    well_covered_mask = mutation_coverage >= 5
    well_covered_df = df[well_covered_mask]
    
    coverage_stats = {
        'total_mutations': len(df),
        'well_covered_mutations': len(well_covered_df),
        'total_coverage': df.count().sum() / df.size * 100,
        'well_covered_coverage': well_covered_df.count().sum() / well_covered_df.size * 100
    }
    
    print(f"Data Coverage Analysis:")
    print(f"  Total mutations: {coverage_stats['total_mutations']:,}")
    print(f"  Well-covered (≥5 experiments): {coverage_stats['well_covered_mutations']:,}")
    print(f"  Total coverage: {coverage_stats['total_coverage']:.2f}%")
    print(f"  Well-covered coverage: {coverage_stats['well_covered_coverage']:.2f}%")
    
    return well_covered_df, coverage_stats

def validate_knn_imputation(df, n_neighbors_list=[3, 5, 7, 10], n_splits=5):
    """
    Validate KNN imputation using cross-validation.
    
    Args:
        df (pd.DataFrame): Well-covered data
        n_neighbors_list (list): List of neighbor counts to test
        n_splits (int): Number of cross-validation splits
    
    Returns:
        dict: Best parameters and validation results
    """
    known_mask = ~df.isnull()
    validation_results = []
    
    for n_neighbors in n_neighbors_list:
        print(f"\nTesting KNN with {n_neighbors} neighbors...")
        
        mse_scores = []
        r2_scores = []
        
        for split in range(n_splits):
            np.random.seed(split)
            hide_mask = np.random.random(df.shape) < 0.2
            hide_mask = hide_mask & known_mask
            
            test_data = df.copy()
            test_data[hide_mask] = np.nan
            
            imputer = KNNImputer(n_neighbors=n_neighbors)
            imputed_data = imputer.fit_transform(test_data)
            imputed_df = pd.DataFrame(imputed_data, index=df.index, columns=df.columns)
            
            true_values = df[hide_mask].values
            predicted_values = imputed_df[hide_mask].values
            
            if len(true_values) > 0:
                # Remove any NaN values
                valid_mask = ~(np.isnan(true_values) | np.isnan(predicted_values))
                if valid_mask.sum() > 0:
                    mse = mean_squared_error(true_values[valid_mask], predicted_values[valid_mask])
                    r2 = r2_score(true_values[valid_mask], predicted_values[valid_mask])
                    mse_scores.append(mse)
                    r2_scores.append(r2)
        
        if mse_scores:
            avg_mse = np.mean(mse_scores)
            avg_r2 = np.mean(r2_scores)
            validation_results.append({
                'n_neighbors': n_neighbors,
                'mse': avg_mse,
                'r2': avg_r2
            })
            print(f"  Average MSE: {avg_mse:.4f}")
            print(f"  Average R²: {avg_r2:.4f}")
    
    best_result = min(validation_results, key=lambda x: x['mse'])
    print(f"\nBest KNN configuration: {best_result['n_neighbors']} neighbors")
    
    return best_result

def analyze_experiment_consistency(df):
    """
    Analyze consistency between experiments.
    
    Args:
        df (pd.DataFrame): Well-covered data
    
    Returns:
        dict: Consistency statistics
    """
    mean_effects = df.mean(axis=1)
    std_effects = df.std(axis=1)
    consistency_scores = 1 / (1 + std_effects)
    
    experiment_means = df.mean(axis=0)
    experiment_stds = df.std(axis=0)
    
    consistency_stats = {
        'mean_consistency': consistency_scores.mean(),
        'high_consistency_count': (consistency_scores >= 0.7).sum(),
        'high_consistency_pct': (consistency_scores >= 0.7).sum() / len(consistency_scores) * 100,
        'experiment_mean_range': (experiment_means.min(), experiment_means.max()),
        'mean_experiment_std': experiment_stds.mean()
    }
    
    print(f"\nExperiment Consistency Analysis:")
    print(f"  Mean consistency score: {consistency_stats['mean_consistency']:.3f}")
    print(f"  High consistency (≥0.7): {consistency_stats['high_consistency_count']} ({consistency_stats['high_consistency_pct']:.1f}%)")
    print(f"  Experiment mean range: {consistency_stats['experiment_mean_range'][0]:.3f} to {consistency_stats['experiment_mean_range'][1]:.3f}")
    print(f"  Mean experiment std: {consistency_stats['mean_experiment_std']:.3f}")
    
    return consistency_stats

def main():
    """Main data validation pipeline."""
    print("=== DATA VALIDATION PIPELINE ===")
    
    # Load data
    df = pd.read_csv('normalized_heatmap_data.csv', index_col=0)
    
    # Analyze coverage
    well_covered_df, coverage_stats = analyze_data_coverage(df)
    
    # Validate KNN imputation
    best_params = validate_knn_imputation(well_covered_df)
    
    # Analyze consistency
    consistency_stats = analyze_experiment_consistency(well_covered_df)
    
    # Save validation results
    validation_results = {
        'coverage_stats': {k: float(v) if isinstance(v, (np.integer, np.floating)) else v 
                          for k, v in coverage_stats.items()},
        'best_knn_params': {k: float(v) if isinstance(v, (np.integer, np.floating)) else v 
                           for k, v in best_params.items()},
        'consistency_stats': {k: float(v) if isinstance(v, (np.integer, np.floating)) else v 
                             for k, v in consistency_stats.items()}
    }
    
    import json
    with open('validation_results.json', 'w') as f:
        json.dump(validation_results, f, indent=2)
    
    print("\nSaved validation_results.json")
    return validation_results

if __name__ == "__main__":
    main()
