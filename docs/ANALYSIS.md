# WWE 2K24 Roster Ratings: Analysis

## Executive summary
Independent analysis of 137 publicly reported WWE 2K24 in-game rating entries across Raw, SmackDown and NXT.

| Roster | Entries | Average rating | Rated 85+ |
|---|---:|---:|---:|
| Raw | 56 | 78.54 | 23.21% |
| SmackDown | 49 | 77.31 | 28.57% |
| NXT | 32 | 73.19 | 0.00% |

There are 136 unique names because Jinder Mahal appears under two rosters. This is retained as a real cross-roster name, not deleted.

## Purpose and questions
How do published WWE 2K24 superstar ratings differ by roster? Which hypotheses could product or game-analytics teams explore using genuine gameplay data?

## Dataset provenance
Ratings manually transcribed from the historical roster tables in Dot Esports: https://dotesports.com/wwe/news/wwe-2k24-complete-roster-and-ratings
Cross-check reference: https://www.thesmackdownhotel.com/news/wwe2k24/wwe-2k24-overall-ratings-list-all-superstars-ranked-by-best-rating
This is a partial publicly reported snapshot, not official 2K player telemetry and not the full WWE 2K24 character roster. Original source spellings were preserved.

## Data model and analytical pipeline
Unit of analysis: one brand-superstar entry. Columns: brand, superstar, overall_rating.
1. Load CSV using pandas with explicit string types for roster/name.
2. Check required columns, nulls, allowed rosters, blank names, integer ratings, 0-100 bounds and duplicate same-roster names.
3. Calculate count, mean, median, standard deviation, minimum, maximum, quartiles, interquartile range, 85+ and 90+ shares.
4. Create roster summary, rating-band matrix, ranked-entry extract and cross-roster repeated-name check.
5. Produce four charts: mean ratings, distribution histogram, stacked rating bands and boxplot/spread.
6. Run automated tests and regenerate all results from the CSV.

## Results and interpretation
NXT's published entries have a lower average and narrower rating distribution than the Raw/SmackDown entries in this sample. SmackDown has a higher share of 85+ entries than Raw although their overall mean ratings are similar. These are descriptive patterns only.

## What this does and does not establish
Overall rating is a character-design attribute. It is not evidence of game fairness, actual player skill, win rate, retention, usage, customer satisfaction or a causal game effect.
No A/B test, cohort experiment or internal player-data analysis was performed in this portfolio project.

## Suggested follow-on game-science study
Collect consented and appropriately governed match-level telemetry: character selected, player skill rating, mode, opponent, difficulty, patch/version, result and repeat-selection behaviour.
Test whether character ratings correlate with match success after adjusting for selection and skill. In a suitably controlled setting, test specific tuning changes with success, usage, engagement and satisfaction guardrails.

## Limitations
Partial non-random published subset; third-party data may contain transcription errors; roster assignments and labels reflect the historical source; several spellings are not standardised. Independently validate original values before using outside a portfolio context. Neither 2K nor WWE endorses the project.

## Reproduce
Install using: python -m pip install -r requirements.txt
Run analysis using: python -m src.analyze
Run tests using: python -m unittest discover -s tests

Generated tables are saved to results/ and PNG charts to figures/.