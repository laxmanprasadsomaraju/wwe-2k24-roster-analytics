# WWE 2K24 — Superstar Ratings & Roster Balance Analytics

Independent sports game analytics using publicly published ratings for 137 WWE 2K24 Raw, SmackDown and NXT roster entries. Analysis uses Python, pandas, matplotlib, descriptive KPIs and unit tests. It does **not** use official player telemetry and does not establish actual gameplay balance.

## Project structure
- `data/wwe2k24_ratings.csv`: published ratings transcription
- `src/analyze.py`: analysis and visualization script
- `tests/test_analysis.py`: data checks
- `results/`: calculated CSV summaries
- `figures/`: four visualization charts
- `docs/ANALYSIS.md`: detailed analytical findings

Install `pip install -r requirements.txt`; run `python -m src.analyze`; run tests with `python -m unittest discover -s tests`.

Data originally transcribed from [Dot Esports WWE 2K24 roster and ratings](https://dotesports.com/wwe/news/wwe-2k24-complete-roster-and-ratings). The data is a limited, historical, third-party sample and not an official 2K dataset.
