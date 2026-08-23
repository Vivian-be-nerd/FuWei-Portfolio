# 02 Data Pattern Analysis

```mermaid
flowchart TD
    A[Data Pattern Analysis Guide] --> B[CONFIG: Patterns + column mapping]
    A --> C[Engine: 4 reusable functions — never edited]
    A --> D[Steps 1-5: Machine counts and classifies]
    A --> E[Step 6: Human writes CLEANING_RULES]

    B --> B1[PATTERNS_ARTIST / PATTERNS_SONG\nshared across all datasets]
    B --> B2[DATASETS: column-name mapping\nonly thing that differs per dataset]

    C --> C1[run_pattern_scan — counts]
    C --> C2[show_examples — prints samples]
    C --> C3[classify_symbol_usage — & / , context]
    C --> C4[classify_extracted_content — parens / dash content]

    D --> D1[Step 1: Basic pattern stats\n6 report tables]
    D --> D2[Step 2-4: D1 deep classification\nsymbol, parens, dash]
    D --> D3[Step 5: Cross-dataset comparison]

    E --> E1[CLEANING_RULES dict\nfeeds directly into 03]
```

## What This Stage Did

Looked at the artist/song text columns across all three datasets to figure out what actually needs cleaning: how often symbols like `&`, parentheses, and dashes show up, and what they usually mean (a collaboration marker vs. part of the actual name, a version tag vs. part of the title). The output is `CLEANING_RULES`, a decision dict the next stage executes directly.

## How I Did It

Split it into two parts: count-and-classify, which is fully automatic (four reusable functions shared across all three datasets), and decide-what-to-clean, which is entirely by hand, after reading every report. The classification functions never decide anything on their own. They just produce evidence for a human to read.

Ran the deeper classification on all three datasets, not just one, since the classification functions were already generic — worth getting real evidence for each dataset instead of assuming they all behave the same way. That caught a real gap: one dataset's parenthetical content was being blanket-preserved when the same evidence showed most of it was just as safe to strip as the first dataset's.

## Open Questions / Things I'd Revisit

- The same classification function gets different category rules depending on the column (artist vs. song). Sharing the function is fine, but sharing its rules across columns that answer different questions isn't, and that distinction has to be made by hand every time a new text column gets added.
- Some pattern definitions are close judgment calls, like what counts as a "version tag." Someone else could reasonably draw the line slightly differently.

---

*Part of [Fu Wei's Data Analysis Pipeline](../README.md)*
