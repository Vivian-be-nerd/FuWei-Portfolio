# Python Version

An end-to-end pipeline, stage by stage. Built with a CONFIG/engine
separation so new datasets only require adding a config entry, not new code.

| File | Stage | What It Demonstrates |
|------|-------|-----------------------|
| 01_data_exploration_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/01_data_exploration_auto.html)) | Data Exploration | Reusable data-quality workflow — swap the config, not the code, to point it at a new dataset |
| 02_data_pattern_analysis_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/02_data_pattern_analysis_auto.html)) | Pattern Analysis | Reusable text-pattern detection and cleaning-rule design, independent of domain |
| 03_data_wrangling_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/03_data_wrangling_auto.html)) | Data Wrangling | One generic cleaning engine driven entirely by config, not per-column code |
| 04_data_Joining_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/04_data_Joining_auto.html)) | Data Joining | Reusable multi-source join logic with built-in match-rate validation |
| 05_EDA_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/05_EDA_auto.html)) | EDA | A hypothesis → verify → correct analytical discipline, not tied to this dataset |
| 06_modeling_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/06_modeling_auto.html)) | Modeling | Reusable binary-classification explanatory workflow (LR + RF, feature-importance comparison) — swap the config to test any Hit/Flop-style problem |
| 07_Final_Report_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/07_Final_Report_auto.html)) | Final Report | Structuring technical findings into a decision-ready narrative for a non-technical audience |

See [`pipeline-guides/01_data_exploration.md`](../../../pipeline-guides/01_data_exploration.md)
for the design principles behind this script (CONFIG/engine separation, and why
statistical outlier detection is reported as `[INFO]` rather than auto-cleaned).

See [`pipeline-guides/02_data_pattern_analysis.md`](../../../pipeline-guides/02_data_pattern_analysis.md)
for how `02_data_pattern_analysis_auto.ipynb` extends this design with a fourth
layer — human judgment — since deciding what a text pattern *means* isn't
something a regex can conclude on its own.

See [`pipeline-guides/03_data_wrangling.md`](../../../pipeline-guides/03_data_wrangling.md)
for how `03_data_wrangling_auto.ipynb` collapses six hand-written, per-column
cleaning functions into one generic `clean_column()`, and how its cross-dataset
join-key overlap independently reproduced the expected match rate almost exactly.

See [`pipeline-guides/04_data_Joining.md`](../../../pipeline-guides/04_data_Joining.md)
for how `04_data_Joining_auto.ipynb` merges an asymmetric pair of joins with one
shared engine function — including a real critical-thinking case around two
datasets that share column names from completely different sources, and a known
dedup limitation (whichever row appears first wins) that's flagged rather than
silently treated as correct.

See [`pipeline-guides/05_EDA.md`](../../../pipeline-guides/05_EDA.md) for why
`05_EDA_auto.ipynb` deliberately does *not* use CONFIG/engine (three research
questions are three different analyses, not one transform looped over
interchangeable datasets), and for two issues caught by not trusting a
first-pass calculation at face value: a stale chart label that had never been
updated to match the data behind it, and a mean-of-means statistic that
overstated Hip-Hop's speechiness ratio (a naive 4.8x vs. 3.86x on a proper,
row-weighted average).

See [`pipeline-guides/06_modeling.md`](../../../pipeline-guides/06_modeling.md)
for how `06_modeling_auto.ipynb` runs Logistic Regression and Random Forest
through the same shared evaluation pipeline, and why Random Forest's clear edge
(AUC 0.867 vs. 0.807) pointed toward testing feature-interaction terms — one of
which (`danceability × energy`) turned out to outweigh every individual feature
once added.

See [`pipeline-guides/07_Final_Report.md`](../../../pipeline-guides/07_Final_Report.md)
for how `07_Final_Report_auto.ipynb` assembles 05's and 06's findings into one
report. No CONFIG/engine here — the reusable part isn't the code, it's the report
*structure*: state a finding, show the chart, add a caveat, repeated once per
research question.
