from flask import Blueprint, render_template, request
import json, plotly
from .utils import generate_variant_map

main = Blueprint("main", __name__)

genes = ["SPTAN1", "SPG"]

@main.route("/")
def index():
    return render_template("index.html", genes=genes)

@main.route("/map")
def map_view():
    gene = request.args.get("gene")

    fig = generate_variant_map(gene)
    graphJSON = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template("map.html", graphJSON=graphJSON, gene=gene)
