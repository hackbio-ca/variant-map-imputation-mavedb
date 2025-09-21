"""
Visualization Pipeline
=====================

This module creates comprehensive visualizations:
1. Create comprehensive plots
2. Generate interactive heatmaps
3. Produce publication-ready figures

Methodology:
- Effect distribution: Histogram of mean z-scores
- Consistency analysis: Scatter plot of effect vs consistency
- Experiment comparison: Error bars showing experiment variability
- Interactive heatmaps: Plotly-based exploration tools
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import json

def create_summary_visualization(df, results_df):
    """
    Create comprehensive summary visualization.
    
    Args:
        df (pd.DataFrame): Imputed data
        results_df (pd.DataFrame): Analysis results
    """
    fig, axes = plt.subplots(2, 3, figsize=(20, 12))
    fig.suptitle('Variant Effect Analysis: Comprehensive Summary', fontsize=16, fontweight='bold')
    
    # 1. Effect distribution
    axes[0, 0].hist(results_df['mean_effect'], bins=50, alpha=0.7, edgecolor='black', color='skyblue')
    axes[0, 0].axvline(0, color='red', linestyle='--', alpha=0.7, label='Neutral (0)')
    axes[0, 0].axvline(-1, color='orange', linestyle='--', alpha=0.7, label='Deleterious (-1)')
    axes[0, 0].axvline(1, color='green', linestyle='--', alpha=0.7, label='Beneficial (+1)')
    axes[0, 0].set_xlabel('Mean Z-score (Effect Size)')
    axes[0, 0].set_ylabel('Number of Mutations')
    axes[0, 0].set_title('Distribution of Mutation Effects')
    axes[0, 0].legend()
    
    # 2. Effect categories pie chart
    category_counts = results_df['effect_category'].value_counts()
    colors = ['red', 'orange', 'gray', 'lightgreen', 'green']
    axes[0, 1].pie(category_counts.values, labels=category_counts.index, autopct='%1.1f%%', 
                   colors=colors, startangle=90)
    axes[0, 1].set_title('Mutation Effect Categories')
    
    # 3. Consistency vs Effect
    scatter = axes[0, 2].scatter(results_df['mean_effect'], results_df['consistency_score'], 
                                alpha=0.6, s=30, c=results_df['mean_effect'], cmap='RdBu_r')
    axes[0, 2].set_xlabel('Mean Z-score (Effect Size)')
    axes[0, 2].set_ylabel('Consistency Score')
    axes[0, 2].set_title('Effect vs Consistency')
    axes[0, 2].axvline(0, color='red', linestyle='--', alpha=0.5)
    axes[0, 2].axhline(0.7, color='blue', linestyle='--', alpha=0.5, label='High consistency')
    axes[0, 2].legend()
    plt.colorbar(scatter, ax=axes[0, 2], label='Effect Size')
    
    # 4. Heatmap of top mutations
    top_mutations = results_df.nlargest(20, 'mean_effect').index
    sample_experiments = df.columns[::2]
    heatmap_data = df.loc[top_mutations, sample_experiments]
    
    im = axes[1, 0].imshow(heatmap_data.values, cmap='RdBu_r', aspect='auto', vmin=-3, vmax=3)
    axes[1, 0].set_title('Top 20 Beneficial Mutations')
    axes[1, 0].set_xlabel('Experiments (sample)')
    axes[1, 0].set_ylabel('Mutations')
    axes[1, 0].set_xticks(range(len(sample_experiments)))
    axes[1, 0].set_xticklabels([exp.split('-')[-1] for exp in sample_experiments], rotation=45)
    plt.colorbar(im, ax=axes[1, 0], label='Z-score')
    
    # 5. Experiment comparison
    experiment_means = df.mean(axis=0)
    experiment_stds = df.std(axis=0)
    
    axes[1, 1].errorbar(range(len(experiment_means)), experiment_means, yerr=experiment_stds, 
                        fmt='o', alpha=0.7, capsize=3, color='purple')
    axes[1, 1].set_xlabel('Experiment Index')
    axes[1, 1].set_ylabel('Mean Z-score')
    axes[1, 1].set_title('Experiment Comparison')
    axes[1, 1].axhline(0, color='red', linestyle='--', alpha=0.5)
    
    # 6. Consistency distribution
    axes[1, 2].hist(results_df['consistency_score'], bins=30, alpha=0.7, edgecolor='black', color='lightcoral')
    axes[1, 2].axvline(0.7, color='red', linestyle='--', alpha=0.7, label='High consistency threshold')
    axes[1, 2].set_xlabel('Consistency Score')
    axes[1, 2].set_ylabel('Number of Mutations')
    axes[1, 2].set_title('Consistency Distribution')
    axes[1, 2].legend()
    
    plt.tight_layout()
    plt.savefig('comprehensive_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def create_interactive_heatmap(df):
    """
    Create interactive heatmap for data exploration.
    
    Args:
        df (pd.DataFrame): Imputed data
    """
    # Sample data for performance
    sample_mutations = df.index[::10]  # Every 10th mutation
    sample_experiments = df.columns[::2]  # Every other experiment
    sample_data = df.loc[sample_mutations, sample_experiments]
    
    fig = go.Figure(data=go.Heatmap(
        z=sample_data.values,
        x=sample_data.columns,
        y=sample_data.index,
        colorscale='RdBu_r',
        zmid=0,
        hoverongaps=False,
        hovertemplate='Mutation: %{y}<br>Experiment: %{x}<br>Z-score: %{z:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        title='Interactive Variant Effect Heatmap',
        xaxis_title='Experiments',
        yaxis_title='Mutations',
        width=1000,
        height=600
    )
    
    fig.write_html('interactive_heatmap.html')
    print("Created interactive_heatmap.html")

def create_consistency_analysis(df, results_df):
    """
    Create detailed consistency analysis visualization.
    
    Args:
        df (pd.DataFrame): Imputed data
        results_df (pd.DataFrame): Analysis results
    """
    fig, axes = plt.subplots(2, 2, figsize=(16, 12))
    fig.suptitle('Consistency Analysis: Methodological Insights', fontsize=16, fontweight='bold')
    
    # 1. Consistency distribution
    axes[0, 0].hist(results_df['consistency_score'], bins=30, alpha=0.7, edgecolor='black', color='red')
    axes[0, 0].axvline(0.7, color='blue', linestyle='--', alpha=0.7, label='High consistency threshold')
    axes[0, 0].axvline(0.5, color='orange', linestyle='--', alpha=0.7, label='Low consistency threshold')
    axes[0, 0].set_xlabel('Consistency Score')
    axes[0, 0].set_ylabel('Number of Mutations')
    axes[0, 0].set_title('Experiment Consistency Distribution')
    axes[0, 0].legend()
    
    # 2. Experiment variability
    experiment_means = df.mean(axis=0)
    experiment_stds = df.std(axis=0)
    
    axes[0, 1].errorbar(range(len(experiment_means)), experiment_means, yerr=experiment_stds, 
                        fmt='o', alpha=0.7, capsize=3, color='purple')
    axes[0, 1].set_xlabel('Experiment Index')
    axes[0, 1].set_ylabel('Mean Z-score')
    axes[0, 1].set_title('Experiment Bias Analysis')
    axes[0, 1].axhline(0, color='red', linestyle='--', alpha=0.5)
    
    # 3. Coverage vs consistency
    mutation_coverage = df.count(axis=1)
    axes[1, 0].scatter(mutation_coverage, results_df['consistency_score'], alpha=0.6, s=30, color='purple')
    axes[1, 0].set_xlabel('Number of Experiments')
    axes[1, 0].set_ylabel('Consistency Score')
    axes[1, 0].set_title('Coverage vs Consistency')
    axes[1, 0].axhline(0.7, color='blue', linestyle='--', alpha=0.5, label='High consistency')
    axes[1, 0].legend()
    
    # 4. Most problematic mutations
    most_inconsistent = results_df.nsmallest(20, 'consistency_score')
    sample_experiments = df.columns[::2]
    heatmap_data = df.loc[most_inconsistent.index, sample_experiments]
    
    im = axes[1, 1].imshow(heatmap_data.values, cmap='RdBu_r', aspect='auto', vmin=-3, vmax=3)
    axes[1, 1].set_title('Most Inconsistent Mutations')
    axes[1, 1].set_xlabel('Experiments (sample)')
    axes[1, 1].set_ylabel('Mutations')
    axes[1, 1].set_xticks(range(len(sample_experiments)))
    axes[1, 1].set_xticklabels([exp.split('-')[-1] for exp in sample_experiments], rotation=45)
    plt.colorbar(im, ax=axes[1, 1], label='Z-score')
    
    plt.tight_layout()
    plt.savefig('consistency_analysis.png', dpi=300, bbox_inches='tight')
    plt.show()

def main():
    """Main visualization pipeline."""
    print("=== VISUALIZATION PIPELINE ===")
    
    # Load data
    df = pd.read_csv('imputed_data.csv', index_col=0)
    results_df = pd.read_csv('analysis_results.csv', index_col=0)
    
    # Create visualizations
    create_summary_visualization(df, results_df)
    create_interactive_heatmap(df)
    create_consistency_analysis(df, results_df)
    
    print("\nGenerated visualization files:")
    print("- comprehensive_analysis.png")
    print("- interactive_heatmap.html")
    print("- consistency_analysis.png")

if __name__ == "__main__":
    main()
