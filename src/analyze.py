"""Reproducible, source-attributed analysis of publicly reported WWE 2K24 ratings.

No scraping, simulated player behaviour, or private game telemetry is used.
Run: python -m src.analyze
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "wwe2k24_ratings.csv"
RESULTS = ROOT / "results"
FIGURES = ROOT / "figures"
BRANDS = ["Raw", "SmackDown", "NXT"]
BINS = [0, 69, 79, 84, 89, 100]
LABELS = ["<=69", "70-79", "80-84", "85-89", "90+"]


def load_and_validate(path=DATA):
    df = pd.read_csv(path, dtype={"brand": "string", "superstar": "string"})
    assert set(df.columns) == {"brand", "superstar", "overall_rating"}, "Unexpected CSV columns"
    assert not df.isna().any().any(), "Missing data detected"
    assert df["brand"].isin(BRANDS).all(), "Unknown roster label"
    assert df["superstar"].str.strip().ne("").all(), "Empty superstar name"
    assert pd.api.types.is_numeric_dtype(df["overall_rating"]), "Non-numeric rating"
    assert df["overall_rating"].between(0, 100).all(), "Out-of-range rating"
    assert (df["overall_rating"] % 1 == 0).all(), "Expected whole-number ratings"
    assert not df.duplicated(subset=["brand", "superstar"]).any(), "Duplicate entry in same roster"
    return df


def compute_summaries(df):
    g = df.groupby("brand")["overall_rating"]
    s = g.agg(entries="size", mean="mean", median="median", std_dev="std", min="min", max="max").reindex(BRANDS)
    s["q1"] = g.quantile(.25).reindex(BRANDS)
    s["q3"] = g.quantile(.75).reindex(BRANDS)
    s["iqr"] = s["q3"] - s["q1"]
    s["n_85_plus"] = df.assign(high=df.overall_rating >= 85).groupby("brand").high.sum().reindex(BRANDS)
    s["pct_85_plus"] = 100*s["n_85_plus"]/s["entries"]
    s["n_90_plus"] = df.assign(elite=df.overall_rating >= 90).groupby("brand").elite.sum().reindex(BRANDS)
    s["pct_90_plus"] = 100*s["n_90_plus"]/s["entries"]
    return s.reset_index().round(2)


def distribution(df):
    work = df.copy()
    work["rating_band"] = pd.cut(work.overall_rating, bins=BINS, labels=LABELS, include_lowest=True)
    return pd.crosstab(work.brand, work.rating_band).reindex(BRANDS).reindex(columns=LABELS,fill_value=0)


def save_chart(path):
    plt.tight_layout()
    plt.savefig(path, dpi=170, bbox_inches="tight")
    plt.close()


def make_charts(df, summary, bands):
    plt.figure(figsize=(9,4.6))
    plt.bar(summary.brand, summary["mean"], color=["#245B8A", "#E38945", "#58A08B"])
    plt.ylim(0,100);plt.ylabel("Mean overall rating (0–100)")
    for i,row in summary.iterrows():
        plt.text(i,row["mean"]+1,f'{row["mean"]:.2f} (n={int(row["entries"])})',ha="center",fontsize=9)
    plt.title("Average WWE 2K24 overall rating by roster")
    save_chart(FIGURES/"01_mean_rating_by_roster.png")

    plt.figure(figsize=(9,4.8))
    plt.hist([df.loc[df.brand==b,"overall_rating"] for b in BRANDS], bins=range(60,101,5),label=BRANDS,alpha=.82)
    plt.xlabel("Overall rating");plt.ylabel("Roster entries");plt.legend();plt.title("Overall rating distribution by roster")
    save_chart(FIGURES/"02_rating_distributions.png")

    ax=bands.plot(kind="bar",stacked=True,figsize=(9,4.8),rot=0,colormap="viridis")
    ax.set_xlabel("Roster");ax.set_ylabel("Roster entries");ax.set_title("Rating bands by roster")
    ax.legend(title="Rating band",bbox_to_anchor=(1.01,1),loc="upper left")
    save_chart(FIGURES/"03_rating_bands.png")

    plt.figure(figsize=(9,4.6))
    data=[df.loc[df.brand==b,"overall_rating"] for b in BRANDS]
    bp=plt.boxplot(data,tick_labels=BRANDS,patch_artist=True,showmeans=True)
    for patch,c in zip(bp['boxes'],["#245B8A", "#E38945", "#58A08B"]):patch.set_facecolor(c);patch.set_alpha(.7)
    plt.ylim(55,100);plt.ylabel("Overall rating");plt.title("Spread, median and outliers by roster")
    save_chart(FIGURES/"04_rating_spread.png")


def main():
    RESULTS.mkdir(exist_ok=True);FIGURES.mkdir(exist_ok=True)
    df=load_and_validate()
    summary=compute_summaries(df)
    bands=distribution(df)
    summary.to_csv(RESULTS/"roster_summary.csv",index=False)
    bands.to_csv(RESULTS/"rating_bands.csv")
    df.sort_values(["overall_rating","superstar"],ascending=[False,True]).to_csv(RESULTS/"all_entries_ranked.csv",index=False)
    df[df.duplicated("superstar",keep=False)].sort_values("superstar").to_csv(RESULTS/"cross_roster_names.csv",index=False)
    make_charts(df,summary,bands)
    print(f"Rows: {len(df)} | Unique names: {df.superstar.nunique()} | Missing cells: {int(df.isna().sum().sum())}")
    print(summary.to_string(index=False))
    print("\nRating bands:\n",bands.to_string())
    print("\nOutputs saved under figures/ and results/")

if __name__=="__main__":main()
