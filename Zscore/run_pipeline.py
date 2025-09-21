"""
Master Pipeline Runner
=====================

This script runs the complete variant effect analysis pipeline:
1. Data Processing
2. Data Validation
3. Imputation
4. Analysis
5. Visualization
6. Methodological Insights

Usage:
    python run_pipeline.py [--steps 1,2,3,4,5,6] [--cleanup]
"""

import sys
import subprocess
import argparse
import os
import glob

def run_step(step_number, step_name):
    """Run a specific pipeline step."""
    print(f"\n{'='*60}")
    print(f"RUNNING STEP {step_number}: {step_name}")
    print(f"{'='*60}")
    
    script_name = f"0{step_number}_{step_name.lower().replace(' ', '_')}.py"
    
    if not os.path.exists(script_name):
        print(f"Error: {script_name} not found!")
        return False
    
    try:
        result = subprocess.run([sys.executable, script_name], 
                              capture_output=True, text=True, check=True)
        print(result.stdout)
        if result.stderr:
            print("Warnings/Errors:")
            print(result.stderr)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error running {script_name}:")
        print(e.stdout)
        print(e.stderr)
        return False

def cleanup_old_files():
    """Remove redundant files from previous analyses."""
    print("\nCleaning up old files...")
    
    # Files to remove
    old_files = [
        'advanced_analysis.py',
        'analyze_data_coverage.py',
        'clean_lda_imputation.py',
        'debug_parsing.py',
        'experimental_heatmap_analysis.py',
        'final_lda_imputation.py',
        'focused_mutation_analysis.py',
        'lda_imputation.py',
        'simple_lda_imputation.py',
        'simple_validation.py',
        'validation_and_interpretation.py',
        'unpivot_data.py'
    ]
    
    removed_count = 0
    for file in old_files:
        if os.path.exists(file):
            os.remove(file)
            print(f"Removed: {file}")
            removed_count += 1
    
    print(f"Removed {removed_count} old files")

def main():
    """Main pipeline runner."""
    parser = argparse.ArgumentParser(description='Run variant effect analysis pipeline')
    parser.add_argument('--steps', default='1,2,3,4,5,6', 
                       help='Comma-separated list of steps to run (default: 1,2,3,4,5,6)')
    parser.add_argument('--cleanup', action='store_true', 
                       help='Clean up old files before running pipeline')
    
    args = parser.parse_args()
    
    # Clean up if requested
    if args.cleanup:
        cleanup_old_files()
    
    # Parse steps
    steps_to_run = [int(s.strip()) for s in args.steps.split(',')]
    
    # Step definitions
    steps = {
        1: "Data Processing",
        2: "Data Validation", 
        3: "Imputation",
        4: "Analysis",
        5: "Visualization",
        6: "Methodological Insights"
    }
    
    print("VARIANT EFFECT ANALYSIS PIPELINE")
    print("=" * 60)
    print(f"Running steps: {', '.join([f'{s}: {steps[s]}' for s in steps_to_run])}")
    
    # Run steps
    success_count = 0
    for step_num in steps_to_run:
        if step_num in steps:
            if run_step(step_num, steps[step_num]):
                success_count += 1
            else:
                print(f"\nStep {step_num} failed! Stopping pipeline.")
                break
        else:
            print(f"Error: Step {step_num} not defined!")
            break
    
    # Summary
    print(f"\n{'='*60}")
    print(f"PIPELINE COMPLETE")
    print(f"{'='*60}")
    print(f"Successfully completed {success_count}/{len(steps_to_run)} steps")
    
    if success_count == len(steps_to_run):
        print("\n🎉 All steps completed successfully!")
        print("\nGenerated files:")
        print("- normalized_heatmap_data.csv")
        print("- imputed_data.csv") 
        print("- analysis_results.csv")
        print("- comprehensive_analysis.png")
        print("- interactive_heatmap.html")
        print("- methodological_insights.png")
        print("- methods_paper_outline.md")
    else:
        print(f"\n❌ Pipeline incomplete. {len(steps_to_run) - success_count} steps failed.")

if __name__ == "__main__":
    main()
