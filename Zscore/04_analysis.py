"""
Analysis Pipeline
================

This module performs biological analysis of variant effects:
1. Categorize mutations by effect (deleterious/neutral/beneficial)
2. Calculate consistency scores across experiments
3. Identify most significant variants
4. Generate analysis results

Methodology:
- Effect categories based on mean z-score thresholds
- Consistency score: 1 / (1 + std) - higher = more consistent
- Statistical significance based on effect size and consistency
"""

import pandas as pd
import numpy as np
import json

def categorize_mutations(df):
    """
    Categorize mutations by their effect size.
    
    Args:
        df (pd.DataFrame): Imputed data
    
    Returns:
        pd.DataFrame: Data with effect categories
    """
    mean_effects = df.mean(axis=1)
    std_effects = df.std(axis=1)
    
    # Categorize by effect size
    effect_categories = pd.cut(mean_effects, 
                              bins=[-np.inf, -1, -0.5, 0.5, 1, np.inf],
                              labels=['Strong Deleterious', 'Deleterious', 'Neutral', 'Beneficial', 'Strong Beneficial'])
    
    # Calculate consistency
    consistency_scores = 1 / (1 + std_effects)
    
    # Create results dataframe
    results_df = pd.DataFrame({
        'mutation': df.index,
        'mean_effect': mean_effects,
        'std_effect': std_effects,
        'consistency_score': consistency_scores,
        'effect_category': effect_categories,
        'high_consistency': consistency_scores >= 0.7
    })
    
    return results_df

def analyze_effect_distribution(results_df):
    """
    Analyze the distribution of mutation effects.
    
    Args:
        results_df (pd.DataFrame): Analysis results
    
    Returns:
        dict: Distribution statistics
    """
    category_counts = results_df['effect_category'].value_counts()
    total_mutations = len(results_df)
    
    distribution_stats = {
        'total_mutations': total_mutations,
        'deleterious_count': (results_df['effect_category'].isin(['Deleterious', 'Strong Deleterious'])).sum(),
        'neutral_count': (results_df['effect_category'] == 'Neutral').sum(),
        'beneficial_count': (results_df['effect_category'].isin(['Beneficial', 'Strong Beneficial'])).sum(),
        'high_consistency_count': results_df['high_consistency'].sum(),
        'mean_effect': results_df['mean_effect'].mean(),
        'std_effect': results_df['std_effect'].mean()
    }
    
    # Calculate percentages
    distribution_stats['deleterious_pct'] = distribution_stats['deleterious_count'] / total_mutations * 100
    distribution_stats['neutral_pct'] = distribution_stats['neutral_count'] / total_mutations * 100
    distribution_stats['beneficial_pct'] = distribution_stats['beneficial_count'] / total_mutations * 100
    distribution_stats['high_consistency_pct'] = distribution_stats['high_consistency_count'] / total_mutations * 100
    
    print(f"\nMutation Effect Distribution:")
    print(f"  Total mutations: {distribution_stats['total_mutations']:,}")
    print(f"  Deleterious: {distribution_stats['deleterious_count']:,} ({distribution_stats['deleterious_pct']:.1f}%)")
    print(f"  Neutral: {distribution_stats['neutral_count']:,} ({distribution_stats['neutral_pct']:.1f}%)")
    print(f"  Beneficial: {distribution_stats['beneficial_count']:,} ({distribution_stats['beneficial_pct']:.1f}%)")
    print(f"  High consistency: {distribution_stats['high_consistency_count']:,} ({distribution_stats['high_consistency_pct']:.1f}%)")
    
    return distribution_stats

def identify_significant_mutations(results_df, n_top=10):
    """
    Identify most significant mutations.
    
    Args:
        results_df (pd.DataFrame): Analysis results
        n_top (int): Number of top mutations to identify
    
    Returns:
        dict: Significant mutations
    """
    # Most deleterious
    most_deleterious = results_df.nsmallest(n_top, 'mean_effect')
    
    # Most beneficial
    most_beneficial = results_df.nlargest(n_top, 'mean_effect')
    
    # Most variable (inconsistent)
    most_variable = results_df.nlargest(n_top, 'std_effect')
    
    # Most consistent
    most_consistent = results_df.nlargest(n_top, 'consistency_score')
    
    significant_mutations = {
        'most_deleterious': most_deleterious[['mutation', 'mean_effect', 'consistency_score']].to_dict('records'),
        'most_beneficial': most_beneficial[['mutation', 'mean_effect', 'consistency_score']].to_dict('records'),
        'most_variable': most_variable[['mutation', 'mean_effect', 'std_effect']].to_dict('records'),
        'most_consistent': most_consistent[['mutation', 'mean_effect', 'consistency_score']].to_dict('records')
    }
    
    print(f"\nSignificant Mutations (Top {n_top}):")
    print(f"  Most Deleterious:")
    for mut in significant_mutations['most_deleterious'][:5]:
        print(f"    {mut['mutation']}: {mut['mean_effect']:.3f} (consistency: {mut['consistency_score']:.3f})")
    
    print(f"  Most Beneficial:")
    for mut in significant_mutations['most_beneficial'][:5]:
        print(f"    {mut['mutation']}: {mut['mean_effect']:.3f} (consistency: {mut['consistency_score']:.3f})")
    
    return significant_mutations

def main():
    """Main analysis pipeline."""
    print("=== ANALYSIS PIPELINE ===")
    
    # Load imputed data
    df = pd.read_csv('imputed_data.csv', index_col=0)
    
    # Categorize mutations
    results_df = categorize_mutations(df)
    
    # Analyze distribution
    distribution_stats = analyze_effect_distribution(results_df)
    
    # Identify significant mutations
    significant_mutations = identify_significant_mutations(results_df)
    
    # Save results
    results_df.to_csv('analysis_results.csv')
    
    # Save summary statistics
    def convert_numpy(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    summary_stats = {
        'distribution_stats': {k: convert_numpy(v) for k, v in distribution_stats.items()},
        'significant_mutations': significant_mutations
    }
    
    with open('analysis_summary.json', 'w') as f:
        json.dump(summary_stats, f, indent=2)
    
    print("\nSaved analysis_results.csv and analysis_summary.json")
    return results_df

if __name__ == "__main__":
    main()
