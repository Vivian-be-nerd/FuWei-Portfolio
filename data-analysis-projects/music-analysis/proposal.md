# Music Hit Analysis: A Six-Decade Study
### Billboard Hot 100 × Spotify Audio Features × Lyrical Themes (1960–2019)

---

## Project Overview

This project explores what makes a song a hit on the U.S. Billboard Hot 100 over the past six decades (1960–2019). Focusing exclusively on the U.S. market, and by combining Billboard chart data with Spotify audio features, I aim to uncover how musical characteristics — such as danceability, energy, valence, and speechiness — have shifted over time, and which of these features are most associated of chart success.

---

## Research Questions

1. How has the genre distribution of Billboard Hot 100 songs changed across decades?
2. Does musical mood (valence) decline during periods of social unrest, such as the Vietnam War era or post-9/11?
3. Does the rise of speechiness in popular music reflect the mainstreaming of Hip-Hop?
4. Which audio features best classify whether a song is a chart hit?

---

## Data Sources

Three datasets are used, all publicly available on Kaggle:

| Dataset | Description | Source |
|---------|-------------|--------|
| **Billboard Hot 100 (1958–2021)** | Weekly chart rankings: song title, artist, rank, peak rank, weeks on board | `dhruvildave/billboard-the-hot-100-songs` |
| **Spotify Hit Predictor (1960–2019)** | 40,000+ tracks labeled as hits or flops, with 14 Spotify audio features organized by decade | `theoverman/the-spotify-hit-predictor-dataset` |
| **Music Dataset 1950–2019** | Genre labels, lyrics, and audio features for 28,000+ songs | `saurabhshahane/music-dataset-1950-to-2019` |

All three datasets have been downloaded and organized. The analysis scope is limited to the U.S. market by anchoring all datasets to the Billboard Hot 100.

---

## Data Quality Notes

During the initial data exploration phase, the following observations were made:

**Billboard Hot 100 (`last-week` column)**
- 32,312 NaN values were identified in the `last-week` column
- These represent two types of entries:
  - **Debut tracks** (`weeks-on-board = 1`): 29,684 songs appearing on the chart for the first time
  - **Re-entry songs** (`weeks-on-board > 1`): 2,628 songs returning to the chart after an absence
- These NaN values are expected and do not indicate data errors

**Spotify Hit Predictor**
- No missing values detected
- Minor anomalies found in `tempo`, `time_signature`, `chorus_hit`, and `sections` (values = 0)
- These will be addressed in the data wrangling phase

**Music Dataset 1950–2019**
- No missing values detected
- Contains an extra index column (`Unnamed: 0`) that will be removed during data wrangling

---

## Project Pipeline

```
01 Data Exploration    → Understand data quality and structure
02 Pattern Analysis    → Identify distributions and trends
03 Data Wrangling      → Clean and standardize datasets
04 Data Joining        → Merge three datasets on song/artist
05 EDA                 → Visualize six decades of music trends
06 Modeling            → Classify chart success with ML models
07 Final Report        → Integrate findings into narrative report
```

---

## Anticipated Challenges

- **Dataset joining**: The three datasets use inconsistent artist and song name formatting, which will require fuzzy matching or manual cleaning to merge reliably.
- **Genre coverage**: The Music Dataset only contains 7 broad genre labels (pop, rock, hip hop, country, blues, jazz, reggae), which may limit the granularity of genre trend analysis.
- **Class imbalance in modeling**: The hit/flop classification in the Spotify dataset may be imbalanced, requiring resampling techniques or adjusted evaluation metrics.
- **Temporal comparability**: Spotify audio features are computed algorithmically and may not be fully consistent across songs from different eras due to changes in recording quality and production style. This limitation will be acknowledged in the final report.

---

## Tools & Technologies

| Category | Tools |
|----------|-------|
| Data Wrangling | R (tidyverse, dplyr), Python (pandas) |
| Visualization | R (ggplot2), Python (matplotlib) |
| Modeling | R (caret), Python (scikit-learn) |
| Reporting | R Markdown (HTML), Jupyter Notebook |

---

## Technical Objectives

- **R Markdown**: Produce a well-structured, reproducible HTML report that integrates code, visualizations, and narrative.
- **Machine Learning**: Apply and compare Logistic Regression and Random Forest classification models to classify chart success.
- **Data Visualization**: Build clear and compelling time-series and comparison charts to communicate trends across six decades.
- **Python Pipeline**: Convert the R-based analysis into a reusable Python pipeline using pandas and scikit-learn.
