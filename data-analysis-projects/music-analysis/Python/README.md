# Python Version

Converting the R pipeline to Python, stage by stage. Built with a CONFIG/engine
separation so new datasets only require adding a config entry, not new code.

| File | Stage | What It Demonstrates | Status |
|------|-------|-----------------------|--------|
| 01_data_exploration_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/01_data_exploration_auto.html)) | Data Exploration | Reusable data-quality workflow — swap the config, not the code, to point it at a new dataset | ✅ Complete |
| 02_data_pattern_analysis_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/02_data_pattern_analysis_auto.html)) | Pattern Analysis | Reusable text-pattern detection and cleaning-rule design, independent of domain | ✅ Complete |
| 03_data_wrangling_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/03_data_wrangling_auto.html)) | Data Wrangling | One generic cleaning engine driven entirely by config, not per-column code | ✅ Complete |
| 04_data_Joining_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/04_data_Joining_auto.html)) | Data Joining | Reusable multi-source join logic with built-in match-rate validation | ✅ Complete |
| 05_EDA_auto.ipynb | EDA | A hypothesis → verify → correct analytical discipline, not tied to this dataset | ✅ Complete |
| 06_modeling_auto.ipynb ([preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/06_modeling_auto.html)) | Modeling | Reusable binary-classification explanatory workflow (LR + RF, feature-importance comparison) — swap the config to test any Hit/Flop-style problem | ✅ Complete |
| 07_Final_Report.py | Final Report | Structuring technical findings into a decision-ready narrative for a non-technical audience | 🔜 Planned |

See [`pipeline-guides/01_data_exploration.md`](../../../pipeline-guides/01_data_exploration.md)
for the design principles behind this script (CONFIG/engine separation, and why
statistical outlier detection is reported as `[INFO]` rather than auto-cleaned).

See [`pipeline-guides/02_data_pattern_analysis.md`](../../../pipeline-guides/02_data_pattern_analysis.md)
for how `02_data_pattern_analysis_auto.ipynb` extends this design with a fourth
layer — human judgment — since deciding what a text pattern *means* isn't
something a regex can conclude on its own.

See [`pipeline-guides/03_data_wrangling.md`](../../../pipeline-guides/03_data_wrangling.md)
for how `03_data_wrangling_auto.ipynb` collapses R's six hand-written cleaning
functions into one generic `clean_column()`, and how its cross-dataset join-key
overlap independently reproduced R's reported match rate almost exactly.

See [`pipeline-guides/04_data_Joining.md`](../../../pipeline-guides/04_data_Joining.md)
for how `04_data_Joining_auto.ipynb` merges an asymmetric pair of joins with one
shared engine function, and the debugging story behind tracking a 0.04% match-rate
gap against R down to two real config bugs — using R's actual regex source, not
just its rendered output — until the primary join matched exactly.

See [`pipeline-guides/05_EDA.md`](../../../pipeline-guides/05_EDA.md) for why
`05_EDA_auto.ipynb` deliberately does *not* use CONFIG/engine (three research
questions are three different analyses, not one transform looped over
interchangeable datasets), and for three issues caught by not trusting R's
rendered output at face value: a chart label that had gone stale relative to
R's own text, a mean-of-means statistic that overstated Hip-Hop's speechiness
ratio (4.8x reported vs. 3.86x on a proper grand mean), and a hardcoded
"divergence begins here" annotation that took three rounds of checking
against the rendered chart (not just the data) to land on the right year.
