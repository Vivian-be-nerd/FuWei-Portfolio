# 03 Data Wrangling

```mermaid
flowchart TD
    A[Data Wrangling Guide] --> B[CONFIG: CLEANING_RULES inherited from 02]
    A --> C[Engine: one clean_column function]
    A --> D[Steps 1-6: execute, verify, save]

    B --> B1[Copied verbatim from 02's Step 6 output\nno re-analysis here]
    B --> B2[DATASETS: column rename map + lowercase flag]

    C --> C1[clean_column reads whichever rule keys exist\nsame function for artist AND song columns]

    D --> D1[Step 1-2: rename columns, apply rules]
    D --> D2[Step 3: before/after health report]
    D --> D3[Step 4-5: join_key + cross-dataset overlap]
    D --> D4[Step 6: save for 04]
```

**See it in action:** [`03_data_wrangling_auto.ipynb`](../data-analysis-projects/music-analysis/Python/03_data_wrangling_auto.ipynb) · [rendered preview](https://vivian-be-nerd.github.io/FuWei-Portfolio/data-analysis-projects/music-analysis/Python/03_data_wrangling_auto.html)

## What This Stage Did

Executed the cleaning decisions from 02: stripped the noise out of artist/song text, standardized column names across the three datasets, and built a join key for merging them in the next stage.

## How I Did It

The naive approach hand-writes six separate cleaning functions, one per dataset per column type. Replaced all of them with one generic `clean_column()` that just reads whichever rules apply from `CLEANING_RULES`. It doesn't know or care which dataset it's cleaning. That only works because 02 already settled on one consistent rule format across every dataset; if it hadn't, this stage would've needed dataset-specific branching.

One quirk I checked instead of just "fixing": the third dataset's raw text was never lowercased upstream, unlike the other two — looked like a possible oversight that could hurt downstream matching. Checked the raw data directly: it's already 100% lowercase, so the missing step was harmless, not a bug. Kept the lowercase step here anyway, as a zero-cost safeguard, not a correction to something that was actually broken.

## Open Questions / Things I'd Revisit

- This stage assumes 02's rules are correct and only executes them. If cleaned output ever looks wrong, the fix almost always belongs in 02's rules, not here. A bug can look like it's "in wrangling" when it's actually upstream.

---

*Part of [Fu Wei's Data Analysis Pipeline](../README.md)*
