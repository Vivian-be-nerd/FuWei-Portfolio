# 📋 Data Analysis Pipeline Guides

Notes from converting a six-stage R analysis pipeline into Python, one stage at a time.

> Updated as each stage is completed.

---

## What's This?

I built a Billboard Hot 100 analysis in R for a graduate coursework project, then converted the whole pipeline to Python. Each guide covers one stage: what it does, how I approached it, and what's still an open question or a judgment call rather than a settled answer.

The design choices (a CONFIG/engine split for the stages that repeat the same logic across datasets, one shared function instead of copy-pasted code, checking every number against the original R output before trusting it) generalize to most structured-data pipelines, not just this one.

> 💡 **See it in action:**  
> These guides were built from the [Music Hit Analysis: A Six-Decade Study](../data-analysis-projects/music-analysis/proposal.md), analyzing 60+ years of Billboard Hot 100 with Spotify audio features.

---

## Guides

| Guide | Stage | Description |
|-------|-------|-------------|
| [01 Data Exploration](./01_data_exploration.md) | Explore | Data quality checks, CONFIG-per-dataset pattern, IQR outlier detection |
| [02 Data Pattern Analysis](./02_data_pattern_analysis.md) | Analyze | Text pattern detection, symbol/content classification, cleaning-rule design |
| [03 Data Wrangling](./03_data_wrangling.md) | Clean | Execute cleaning rules, column alignment, join-key creation |
| [04 Data Joining](./04_data_Joining.md) | Merge | Join strategies, key matching, validation |
| [05 EDA](./05_EDA.md) | Visualize | Exploratory visualization, trend analysis, three research questions |
| 06 Modeling | Model | Feature selection, model evaluation |
| 07 Final Report | Report | Storytelling, presentation structure |

---

## How to Use

Each guide follows the same structure:
- **What This Stage Did** — the goal and scope
- **What I Found** — only in stages that produce an actual analytical result (05 onward). 01–04 are data-engineering stages with nothing to report here.
- **How I Did It** — the approach, and anything real I caught along the way
- **Open Questions** — limitations and judgment calls I'd revisit

---

## Tools

```python
import pandas as pd        # Data manipulation
import numpy as np         # Numerical operations
import matplotlib.pyplot   # Visualization
import scikit-learn        # Machine learning
```

---

*Part of [Fu Wei's Data Analytics Portfolio](../README.md)*
