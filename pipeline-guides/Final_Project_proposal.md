# Advanced Business Analytics – Final Project Proposal

## Team Members
Fu Wei Hsu

## Project Title
What Makes a Hit? Analyzing Six Decades of Billboard Hot 100 with Spotify Audio Features

## Type of Final Project
Type 1 – Data Analysis Project

## Executive Summary of the Proposed Project

This project explores what makes a song a hit on the U.S. Billboard Hot 100 over the past six decades (1960–2019). Focusing exclusively on the U.S. market, and by combining Billboard chart data with Spotify audio features, I aim to uncover how musical characteristics — such as danceability, energy, valence, and speechiness — have shifted over time, and which of these features are most predictive of chart success.

The analysis will be organized around four research questions:  

**1. How has the genre distribution of Billboard Hot 100 songs changed across decades?**  

**2. Does musical mood (valence) decline during periods of social unrest, such as the Vietnam War era or post-9/11?**  

**3. Does the rise of speechiness in popular music reflect the mainstreaming of Hip-Hop?**  

**4. Which audio features best predict whether a song will become a chart hit?**  

The project will primarily use R, leveraging tidyverse for data wrangling, ggplot2 for visualization, and both Logistic Regression and Random Forest for predictive modeling. Results will be presented as an R Markdown HTML report accompanied by a short video walkthrough.

## Data Needs and Sources

Three datasets will be used, all publicly available on Kaggle:

- **Billboard Hot 100 (1958–2021)** – Weekly chart rankings including song title, artist, rank, peak rank, and weeks on board. Source: `dhruvildave/billboard-the-hot-100-songs`
- **Spotify Hit Predictor Dataset (1960–2019)** – Over 40,000 tracks labeled as hits or flops, with 14 Spotify audio features (danceability, energy, valence, speechiness, acousticness, tempo, etc.) organized by decade. Source: `theoverman/the-spotify-hit-predictor-dataset`
- **Music Dataset 1950–2019** – Contains genre labels, lyrics, and additional audio features for over 28,000 songs. Source: `saurabhshahane/music-dataset-1950-to-2019`

All three datasets have already been downloaded and organized. The analysis scope will be limited to the U.S. market by anchoring all datasets to the Billboard Hot 100.

## Anticipated Challenges

- **Dataset joining**: The three datasets use inconsistent artist and song name formatting, which will require fuzzy matching or manual cleaning to merge reliably.
- **Genre coverage**: The Music Dataset only contains 7 broad genre labels (pop, rock, hip hop, country, blues, jazz, reggae), which may limit the granularity of genre trend analysis.
- **Class imbalance in modeling**: The hit/flop classification in the Spotify dataset may be imbalanced, requiring resampling techniques or adjusted evaluation metrics.
- **Temporal comparability**: Spotify audio features are computed algorithmically and may not be fully consistent across songs from different eras due to changes in recording quality and production style. This limitation will be acknowledged in the final report.

## Personal Learning Objectives

- **R Markdown**: Produce a well-structured, reproducible HTML report that integrates code, visualizations, and narrative.
- **Machine Learning in R**: Apply and compare Logistic Regression and Random Forest classification models to predict chart success, including feature importance analysis.
- **Data Visualization**: Build clear and compelling time-series and comparison charts using ggplot2 to communicate trends across six decades.
