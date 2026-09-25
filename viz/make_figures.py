"""
Charts rebuilt from the report's own tables (data/*.csv). Nothing is estimated.
Run:  python make_figures.py   -> PNGs in ../images/
"""
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

HERE = Path(__file__).parent
DATA, OUT = HERE / "data", HERE.parent / "images"
plt.rcParams.update({
    "font.family": "DejaVu Sans", "font.size": 9, "axes.titlesize": 10, "axes.titleweight": "bold",
    "axes.spines.top": False, "axes.spines.right": False, "savefig.dpi": 200,
    "savefig.bbox": "tight", "figure.facecolor": "white",
})
# 10 factor groups -> Okabe-Ito + two neutral greys
GROUP_COL = {
    "Distance from central city": "#0072B2", "Topography": "#E69F00", "Transportation": "#56B4E9",
    "Community services": "#CC79A7", "Security": "#D55E00", "Utilities": "#F0E442",
    "Flood level": "#009E73", "Vegetation": "#7FBF7B", "Salinity": "#999999", "Drainage": "#444444",
}
NOTE = "Rebuilt from report Table 10 (weighted score = weight % x score / 100)."


def suitability():
    d = pd.read_csv(DATA / "final_analysis_table.csv", comment="#")
    sites = ["site2", "site4", "site5", "site7", "site9"]
    ws = d[sites].mul(d.weight_pct, axis=0) / 100
    ws["group"] = d.group
    g = ws.groupby("group", sort=False).sum()
    totals = g.sum().sort_values()
    fig, ax = plt.subplots(figsize=(7.2, 3.4))
    left = pd.Series(0.0, index=totals.index)
    for grp in g.index:
        vals = g.loc[grp, totals.index]
        ax.barh([s.replace("site", "Site ") for s in totals.index], vals, left=left,
                color=GROUP_COL[grp], edgecolor="white", linewidth=0.5, height=0.62, label=grp)
        left += vals
    for y, s in enumerate(totals.index):
        ax.text(totals[s] + 0.06, y, f"{totals[s]:.2f}", va="center", fontweight="bold", fontsize=8.5)
    ax.set_xlim(0, 7.4)
    ax.set_xlabel("Weighted suitability score (out of 10)")
    ax.set_title("Site 9 scores highest of the five shortlisted sites", loc="left")
    ax.legend(ncol=2, fontsize=7, frameon=False, loc="upper left", bbox_to_anchor=(1.01, 1.0))
    fig.text(0, -0.04, NOTE, fontsize=7, color="#555")
    fig.savefig(OUT / "site-suitability-weighted-scores.png")
    plt.close(fig)


def land_budget():
    d = pd.read_csv(DATA / "site9_land_budget.csv", comment="#")
    total = d.area_acre.sum()
    c = d.groupby("category", sort=False).area_acre.sum().sort_values()
    fig, ax = plt.subplots(figsize=(6.2, 3.0))
    cols = ["#0072B2" if k == "Residential" else "#56B4E9" for k in c.index]
    ax.barh(c.index, c.values, color=cols, height=0.6)
    for y, v in enumerate(c.values):
        ax.text(v + 1, y, f"{v:.1f} ac ({v / total * 100:.1f}%)", va="center", fontsize=7.5)
    ax.set_xlim(0, 120)
    ax.set_xlabel("Area (acres)")
    ax.set_title(f"Land budget for Site 9 ({total:.0f} acres, ~58,450 people)", loc="left")
    fig.text(0, -0.05, "Rebuilt from report Table 12 (Gazette 2012 standards, 350 persons/acre).",
             fontsize=7, color="#555")
    fig.savefig(OUT / "site-9-land-budget.png")
    plt.close(fig)


if __name__ == "__main__":
    suitability()
    land_budget()
    print("written to", OUT.resolve())
