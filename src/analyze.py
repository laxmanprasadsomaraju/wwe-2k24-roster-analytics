import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data/wwe2k24_ratings.csv"

def load_and_validate(path=DATA):
    df = pd.read_csv(path)
    expected = {"brand", "name", "overall_rating"}
    if not expected.issubset(df.columns):
        raise ValueError(f"Missing columns: {expected - set(df.columns)}")
    if df[list(expected)].isna().any().any():
        raise ValueError("Missing ratings, wrestler names or roster")
    if not df["overall_rating"].between(0, 100).all():
        raise ValueError("Unexpected rating outside 0–100")
    if df.duplicated(["brand", "name"]).any():
        raise ValueError("Duplicate roster + wrestler records")
    return df

def run():
    df = load_and_validate()
    (ROOT / "results").mkdir(exist_ok=True)
    (ROOT / "figures").mkdir(exist_ok=True)
    s = df.groupby("brand")["overall_rating"].agg(["count","mean","median","std","min","max"])
    s.round(2).to_csv(ROOT / "results/roster_summary.csv")
    df.sort_values("overall_rating",ascending=False).to_csv(ROOT / "results/all_entries_ranked.csv",index=False)
    plt.figure(figsize=(8,5))
    s["mean"].sort_values(ascending=False).plot(kind="bar")
    plt.ylim(0,100)
    plt.title("WWE 2K24: Mean Published Overall Rating by Roster")
    plt.ylabel("Overall rating")
    plt.tight_layout()
    plt.savefig(ROOT / "figures/01_mean_rating_by_roster.png",dpi=160)
    plt.close()
    print(s.round(2).to_string())
    return s

if __name__ == "__main__":
    run()
