# 📋 Data Analysis Pipeline Guides

Python-based reusable templates for each stage of the data analysis pipeline.  
Built from real project experience — applicable to any structured dataset.

> These guides are continuously updated as I complete each stage of analysis.

---

## What's This?

When I converted my R-based music analysis project into Python, I documented every decision, common mistake, and best practice into reusable guides.

These templates can be applied to **any structured dataset**, not just music data.

> 💡 **See it in action:**  
> These guides were built from the [Music Hit Analysis: A Six-Decade Study](../data-analysis-projects/music-analysis/proposal.md)  
> — analyzing 60+ years of Billboard Hot 100 with Spotify audio features.

---

## Guides

| Guide | Stage | Description | Status |
|-------|-------|-------------|--------|
| [01 Data Exploration](./01_data_exploration.md) | Explore | Data quality check, validation rules, decision flow | ✅ Available |
| 02 Data Pattern Analysis | Analyze | Distribution, outliers, correlations | 🔜 Coming Soon |
| 03 Data Wrangling | Clean | Missing values, standardization, encoding | 🔜 Coming Soon |
| 04 Data Joining | Merge | Join strategies, key matching, validation | 🔜 Coming Soon |
| 05 EDA | Visualize | Exploratory visualization, trend analysis | 🔜 Coming Soon |
| 06 Modeling | Model | Feature selection, model evaluation | 🔜 Coming Soon |
| 07 Final Report | Report | Storytelling, presentation structure | 🔜 Coming Soon |

---

## How to Use

Each guide includes:
- **Decision Rules** — when to use which method
- **Code Templates** — ready-to-use Python code
- **Common Mistakes** — what to avoid
- **Decision Flow** — step-by-step thinking process

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
