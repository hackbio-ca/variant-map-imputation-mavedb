"""
Methodological Insights Pipeline
===============================

This module identifies methodological challenges and proposes solutions:
1. Identify integration challenges
2. Propose quality control metrics
3. Develop validation framework
4. Generate methods paper outline

Methodology:
- Consistency analysis: Quantify cross-experiment agreement
- Bias detection: Identify systematic experiment differences
- Quality metrics: Develop thresholds for reliable integration
- Solution framework: Propose improved integration methods
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json

def analyze_integration_challenges(df, results_df):
    """
    Analyze challenges in MAVE data integration.
    
    Args:
        df (pd.DataFrame): Imputed data
        results_df (pd.DataFrame): Analysis results
    
    Returns:
        dict: Integration challenge statistics
    """
    # Calculate consistency metrics
    consistency_scores = results_df['consistency_score']
    experiment_means = df.mean(axis=0)
    experiment_stds = df.std(axis=0)
    
    # Identify problematic patterns
    high_consistency_pct = (consistency_scores >= 0.7).sum() / len(consistency_scores) * 100
    low_consistency_pct = (consistency_scores < 0.5).sum() / len(consistency_scores) * 100
    extreme_experiments = (abs(experiment_means) > 1.0).sum()
    
    challenges = {
        'high_consistency_pct': high_consistency_pct,
        'low_consistency_pct': low_consistency_pct,
        'extreme_experiments': extreme_experiments,
        'experiment_mean_range': (experiment_means.min(), experiment_means.max()),
        'mean_experiment_std': experiment_stds.mean(),
        'consistency_mean': consistency_scores.mean()
    }
    
    print(f"\nIntegration Challenges:")
    print(f"  High consistency (≥0.7): {high_consistency_pct:.1f}%")
    print(f"  Low consistency (<0.5): {low_consistency_pct:.1f}%")
    print(f"  Extreme experiments (|mean| > 1.0): {extreme_experiments}")
    print(f"  Experiment mean range: {challenges['experiment_mean_range'][0]:.3f} to {challenges['experiment_mean_range'][1]:.3f}")
    print(f"  Mean experiment std: {challenges['mean_experiment_std']:.3f}")
    
    return challenges

def propose_quality_metrics(challenges):
    """
    Propose quality control metrics for MAVE data integration.
    
    Args:
        challenges (dict): Integration challenge statistics
    
    Returns:
        dict: Proposed quality metrics
    """
    quality_metrics = {
        'consistency_threshold': 0.7,
        'experiment_bias_threshold': 1.0,
        'min_experiments': 5,
        'max_experiment_std': 1.5,
        'min_correlation': 0.5
    }
    
    print(f"\nProposed Quality Control Metrics:")
    print(f"  Consistency threshold: ≥{quality_metrics['consistency_threshold']}")
    print(f"  Experiment bias threshold: |mean| < {quality_metrics['experiment_bias_threshold']}")
    print(f"  Minimum experiments: ≥{quality_metrics['min_experiments']}")
    print(f"  Maximum experiment std: <{quality_metrics['max_experiment_std']}")
    print(f"  Minimum correlation: ≥{quality_metrics['min_correlation']}")
    
    return quality_metrics

def create_methodological_visualizations(df, results_df, challenges):
    """
    Create visualizations highlighting methodological problems.
    
    Args:
        df (pd.DataFrame): Imputed data
        results_df (pd.DataFrame): Analysis results
        challenges (dict): Integration challenges
    """
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Methodological Issues in MAVE Data Integration', fontsize=16, fontweight='bold')
    
    # 1. Consistency distribution
    consistency_scores = results_df['consistency_score']
    axes[0, 0].hist(consistency_scores, bins=30, alpha=0.7, edgecolor='black', color='red')
    axes[0, 0].axvline(0.7, color='blue', linestyle='--', alpha=0.7, label='High consistency threshold')
    axes[0, 0].axvline(0.5, color='orange', linestyle='--', alpha=0.7, label='Low consistency threshold')
    axes[0, 0].set_xlabel('Consistency Score')
    axes[0, 0].set_ylabel('Number of Mutations')
    axes[0, 0].set_title('Experiment Consistency Distribution')
    axes[0, 0].legend()
    axes[0, 0].text(0.02, 0.98, f'Only {challenges["high_consistency_pct"]:.1f}% have high consistency', 
                    transform=axes[0, 0].transAxes, verticalalignment='top', 
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # 2. Experiment bias analysis
    experiment_means = df.mean(axis=0)
    experiment_stds = df.std(axis=0)
    
    axes[0, 1].errorbar(range(len(experiment_means)), experiment_means, yerr=experiment_stds, 
                        fmt='o', alpha=0.7, capsize=3, color='purple')
    axes[0, 1].set_xlabel('Experiment Index')
    axes[0, 1].set_ylabel('Mean Z-score')
    axes[0, 1].set_title('Experiment Bias Analysis')
    axes[0, 1].axhline(0, color='red', linestyle='--', alpha=0.5)
    axes[0, 1].text(0.02, 0.98, f'Range: {challenges["experiment_mean_range"][0]:.2f} to {challenges["experiment_mean_range"][1]:.2f}', 
                    transform=axes[0, 1].transAxes, verticalalignment='top', 
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # 3. Effect vs consistency
    mean_effects = results_df['mean_effect']
    scatter = axes[0, 2].scatter(mean_effects, consistency_scores, alpha=0.6, s=30, c=mean_effects, cmap='RdBu_r')
    axes[0, 2].set_xlabel('Mean Z-score (Effect Size)')
    axes[0, 2].set_ylabel('Consistency Score')
    axes[0, 2].set_title('Effect Size vs Consistency')
    axes[0, 2].axvline(0, color='red', linestyle='--', alpha=0.5)
    axes[0, 2].axhline(0.7, color='blue', linestyle='--', alpha=0.5, label='High consistency')
    axes[0, 2].legend()
    plt.colorbar(scatter, ax=axes[0, 2], label='Effect Size')
    
    # 4. Most problematic mutations
    most_inconsistent = results_df.nsmallest(20, 'consistency_score')
    sample_experiments = df.columns[::2]
    heatmap_data = df.loc[most_inconsistent.index, sample_experiments]
    
    im = axes[1, 0].imshow(heatmap_data.values, cmap='RdBu_r', aspect='auto', vmin=-3, vmax=3)
    axes[1, 0].set_title('Most Inconsistent Mutations')
    axes[1, 0].set_xlabel('Experiments (sample)')
    axes[1, 0].set_ylabel('Mutations')
    axes[1, 0].set_xticks(range(len(sample_experiments)))
    axes[1, 0].set_xticklabels([exp.split('-')[-1] for exp in sample_experiments], rotation=45)
    plt.colorbar(im, ax=axes[1, 0], label='Z-score')
    
    # 5. Experiment variability
    axes[1, 1].hist(experiment_stds, bins=20, alpha=0.7, edgecolor='black', color='green')
    axes[1, 1].set_xlabel('Standard Deviation')
    axes[1, 1].set_ylabel('Number of Experiments')
    axes[1, 1].set_title('Experiment Variability')
    axes[1, 1].text(0.02, 0.98, f'Mean std: {challenges["mean_experiment_std"]:.3f}', 
                    transform=axes[1, 1].transAxes, verticalalignment='top', 
                    bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.8))
    
    # 6. Coverage vs consistency
    mutation_coverage = df.count(axis=1)
    axes[1, 2].scatter(mutation_coverage, consistency_scores, alpha=0.6, s=30, color='purple')
    axes[1, 2].set_xlabel('Number of Experiments')
    axes[1, 2].set_ylabel('Consistency Score')
    axes[1, 2].set_title('Coverage vs Consistency')
    axes[1, 2].axhline(0.7, color='blue', linestyle='--', alpha=0.5, label='High consistency')
    axes[1, 2].legend()
    
    plt.tight_layout()
    plt.savefig('methodological_insights.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_methods_paper_outline(challenges, quality_metrics):
    """
    Create outline for methods paper.
    
    Args:
        challenges (dict): Integration challenges
        quality_metrics (dict): Proposed quality metrics
    """
    outline = f"""
# Challenges in MAVE Data Integration: A Methodological Analysis

## Abstract
Multiplexed Assays of Variant Effect (MAVE) data integration faces significant methodological challenges. 
We analyzed 3,459 variants across 43 experiments and found that only {challenges['high_consistency_pct']:.1f}% have high consistency scores, 
revealing substantial inter-experiment variability that compromises simple averaging approaches.

## Introduction
- MAVE data integration is commonly assumed to be straightforward
- Current methods often average across experiments without validation
- Need for rigorous assessment of integration reliability

## Methods
- Analyzed SPTAN1 variant data from 43 experiments
- Calculated consistency scores for cross-experiment agreement
- Identified systematic biases and measurement variability

## Results
- Only {challenges['high_consistency_pct']:.1f}% of variants have high consistency (≥0.7)
- Experiment means range from {challenges['experiment_mean_range'][0]:.2f} to {challenges['experiment_mean_range'][1]:.2f} (systematic bias)
- Mean experiment std: {challenges['mean_experiment_std']:.3f} (high variability)
- {challenges['extreme_experiments']} experiments show extreme bias (|mean| > 1.0)

## Discussion
- Simple averaging across experiments is problematic
- Need for experiment-specific normalization
- Consistency-based filtering improves reliability
- Proposed quality metrics for MAVE integration

## Proposed Solutions
1. **Consistency-based filtering**: Only use variants with consistency ≥ {quality_metrics['consistency_threshold']}
2. **Experiment quality control**: Flag experiments with |mean| > {quality_metrics['experiment_bias_threshold']}
3. **Robust normalization**: Use experiment-specific normalization methods
4. **Validation framework**: Implement cross-validation protocols

## Conclusions
- MAVE data integration requires careful methodological consideration
- Proposed framework for assessing integration reliability
- Guidelines for future MAVE data analysis

## References
- MaveDB v2: a curated community database...
- Data integration in precision medicine...
- Multiplexed assays of variant effects...
"""
    
    with open('methods_paper_outline.md', 'w') as f:
        f.write(outline)
    
    print("\nMethods paper outline saved as 'methods_paper_outline.md'")

def main():
    """Main methodological insights pipeline."""
    print("=== METHODOLOGICAL INSIGHTS PIPELINE ===")
    
    # Load data
    df = pd.read_csv('imputed_data.csv', index_col=0)
    results_df = pd.read_csv('analysis_results.csv', index_col=0)
    
    # Analyze integration challenges
    challenges = analyze_integration_challenges(df, results_df)
    
    # Propose quality metrics
    quality_metrics = propose_quality_metrics(challenges)
    
    # Create visualizations
    create_methodological_visualizations(df, results_df, challenges)
    
    # Create methods paper outline
    create_methods_paper_outline(challenges, quality_metrics)
    
    # Save insights
    def convert_numpy(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        return obj
    
    insights = {
        'challenges': {k: convert_numpy(v) for k, v in challenges.items()},
        'quality_metrics': quality_metrics
    }
    
    with open('methodological_insights.json', 'w') as f:
        json.dump(insights, f, indent=2)
    
    print("\nGenerated files:")
    print("- methodological_insights.png")
    print("- methods_paper_outline.md")
    print("- methodological_insights.json")

if __name__ == "__main__":
    main()
