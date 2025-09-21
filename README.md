# variant-map-imputation-mavedb

Calibrated Variant Maps and Lightweight Imputation for Clinically Useful Scores using MaveDB

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

## Abstract

This project addresses methodological challenges in integrating multiplexed assay of variant effect (MAVE) data across multiple experiments. Using SPTAN1 variant data as a case study, we identify significant issues with cross-experiment consistency and propose quality control frameworks for reliable data integration. The pipeline implements z-score normalization, consistency-based filtering, and baseline imputation methods while acknowledging limitations and proposing generative models for future work. Our analysis reveals that only 60.2% of mutations show high consistency across experiments, highlighting the need for improved integration methods in MAVE data analysis.

## Installation

Install the required Python dependencies and prepare the environment for running the analysis pipeline.

```bash
# Install Python dependencies
pip install -r requirements.txt

# Ensure SPTAN1Data directory contains raw CSV files
# The pipeline expects data files in ../SPTAN1Data/ directory
```

## Quick Start

Run the complete analysis pipeline to process SPTAN1 variant data and identify methodological challenges in MAVE data integration.

```bash
# Run complete pipeline
cd Zscore
python run_pipeline.py --cleanup

# Or run individual steps
python 01_data_processing.py
python 02_data_validation.py
python 03_imputation.py
python 04_analysis.py
python 05_visualization.py
python 06_methodological_insights.py
```

## Usage

The pipeline consists of six main analysis steps that can be run individually or as a complete workflow:

### Pipeline Steps

1. **Data Processing** (`01_data_processing.py`): Loads raw CSV files, parses HGVS protein notation, and calculates z-scores for cross-experiment comparison.

2. **Data Validation** (`02_data_validation.py`): Analyzes data coverage, validates imputation parameters through cross-validation, and quantifies consistency across experiments.

3. **Imputation** (`03_imputation.py`): Implements KNN imputation as baseline method while acknowledging limitations with high missing data rates (88.49%).

4. **Analysis** (`04_analysis.py`): Categorizes mutations by effect size, calculates consistency scores, and identifies significant variants.

5. **Visualization** (`05_visualization.py`): Creates comprehensive plots and interactive heatmaps for data exploration.

6. **Methodological Insights** (`06_methodological_insights.py`): Identifies integration challenges and proposes quality control frameworks.

### Key Features

- **Z-score normalization** for cross-experiment comparison
- **Consistency-based filtering** for reliable mutations
- **Quality control metrics** for experiment validation
- **Baseline imputation** with acknowledged limitations
- **Proposed generative models** for future improvements

## Contribute

Contributions are welcome! If you'd like to contribute, please open an issue or submit a pull request. See the [contribution guidelines](CONTRIBUTING.md) for more information.

## Support

If you have any issues or need help, please open an [issue](https://github.com/hackbio-ca/demo-project/issues) or contact the project maintainers.

## License

This project is licensed under the [MIT License](LICENSE).
