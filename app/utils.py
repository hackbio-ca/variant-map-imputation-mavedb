import pandas as pd
import plotly.express as px

def generate_variant_map(gene: str):
    """
    Given a gene name, load its variant-effect data and return a Plotly figure.
    """
    # TODO: replace with real dataset loading
    df = pd.DataFrame({
        "position": [1, 1, 2, 2, 3, 3],
        "amino_acid": ["A", "T", "A", "T", "A", "T"],
        "score": [0.1, -0.2, 0.3, -0.1, 0.5, 0.0]
    })

    fig = px.density_heatmap(
        df,
        x="amino_acid",
        y="position",
        z="score",
        color_continuous_scale="RdBu",
        title=f"Variant Effect Map for {gene}"
    )
    return fig
