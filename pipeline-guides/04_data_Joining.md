# 🔗 04 Data Joining Guide

```mermaid
flowchart TD
    A[🔗 Data Joining Guide] --> B[CONFIG: JOIN_STAGES]
    A --> C[Engine: one dedup_and_left_join function]
    A --> D[Steps 1-6: join, evaluate, save]

    B --> B1[D1_D2: carry Spotify audio features + target + decade]
    B --> B2[D1D2_D3: carry D3's genre + lyric-theme columns only]

    C --> C1[Dedup right table on join_key, keep first]
    C --> C2[Left join requested columns, report match rate]

    D --> D1[Step 2: D1+D2 primary join]
    D --> D2[Step 3-4: match rate by decade, unmatched sample]
    D --> D3[Step 5: D1+D2+D3 auxiliary join + full validation]
    D --> D4[Step 6: save for 05/06]
```

## Universal Data Joining Template

**Applicable to:** Any pipeline stage that merges an asymmetric set of tables (one primary/base table, one or more secondary tables joined in for extra features) rather than looping the same transform across equivalent datasets
**Purpose:** Turn 03's cleaned, key-bearing datasets into one analysis-ready table, with match-rate evidence at every join — not just "it ran without an error"
**Last Updated:** July 2026

---

## The Core Design Principle: CONFIG/Engine Still Applies, Even When the Shape Isn't a Loop

Stages 01–03 apply the *same* logic to three equivalent datasets. Stage 04 doesn't — it's two genuinely different join operations (D1+D2 primary, then D1D2+D3 auxiliary). The temptation is to abandon CONFIG/engine separation here since "it's not a loop anymore." It doesn't have to be:

```python
JOIN_STAGES = {
    "D1_D2":   {"right_df": d2, "carry_columns": [...], "match_indicator_col": "target"},
    "D1D2_D3": {"right_df": d3, "carry_columns": [...], "match_indicator_col": "genre"},
}

dedup_and_left_join(d1, **JOIN_STAGES["D1_D2"])
dedup_and_left_join(d1_d2_joined, **JOIN_STAGES["D1D2_D3"])
```

One join-and-report function, called twice with different config. The lesson generalizes: CONFIG/engine separation is about *where a decision lives*, not about *how many times a loop runs*.

### A critical-thinking catch: avoiding a silent column collision

D3 happens to have its own columns named `danceability`, `energy`, `valence`, etc. — same names as D2's Spotify audio features, completely different source. R's original `select()` deliberately excludes them from the D3 join. Blindly "helping" by carrying over all of D3's columns would have let `pandas.merge` silently append `_x`/`_y` suffixes, producing two differently-sourced "energy" columns that look interchangeable but aren't. `JOIN_STAGES["D1D2_D3"]["carry_columns"]` intentionally lists only the 12 non-colliding columns — verified against the R source, not assumed.

---

## What Happens — 6 Steps

| Step | What it does | Why |
|---|---|---|
| 1. Load | Read 03's `wrangled_D1/D2/D3.pkl` | Confirms row counts and unique `join_key` counts before merging |
| 2. Primary Join | Dedup D2 on `join_key`, left-join Spotify audio features + `target` + `decade` onto D1 | D1 stays the base — every chart-week row is preserved |
| 3. Match Rate Evaluation | Overall %, plus by `decade_d1` (computed from D1's own chart date, not the D2-sourced `decade` column) | Are older decades systematically under-matched? |
| 4. Unmatched Sample | A readable sample of D1 rows with no D2 match | Sanity check — do these look like real non-matches, or a cleaning gap? |
| 5. Auxiliary Join + Validation | Dedup D3, left-join genre/lyric-theme columns; report D2-matched, D3-matched, both-matched | Full picture before handing off |
| 6. Save | `.pkl` | Hands off to 05/06 |

### A validation win worth calling out — and the debugging story behind it

The first run showed the D1+D2 match rate about 0.04% off from R's reported number (264,348 vs 264,478 rows). The instinct was to chalk it up to floating-point rounding or an unresolvable edge case and move on. That would have been wrong to stop at.

This machine actually has a full R installation (`Rscript.exe`, tidyverse included) — it just isn't registered as a Jupyter kernel. Running R's *actual* join logic directly (not just reading its pre-rendered HTML output) produced exact `join_key` sets to diff against Python's, which surfaced two real gaps in `CLEANING_RULES` (inherited from stage 02) that had been invisible at the aggregate-number level:

1. **A missing word boundary.** `remove_after_marker` treated `"with"` as a bare substring, so "Bill Withers" and "Men Without Hats" got truncated to "bill" and "men" (the marker matched *inside* "Withers"/"Without"). This affected both D1 and D2 identically, so it never showed up as a match-rate discrepancy — both sides were wrong the same way, and still matched each other. Fixed by scoping the boundary to the specific marker (`"with\b"`) rather than blanket-adding `\b` to every marker (a first attempt at a blanket fix broke `"feat."` and `"ft."`, which end in a literal period — `\b` immediately after a non-word character behaves differently than expected).

2. **A rule generalized from statistics, not from R's source.** `CLEANING_RULES` for D2's track column listed a bare `"live"` tag. R's actual regex only strips an *exact* `"(live version)"` parenthetical, or a dash clause that is *exactly* `"live"`/`"version live"`/`"live version"` (anchored to end-of-string) — not "contains live anywhere." The bare tag caused Python to strip legitimate content like `"(Live)"`, `"- Live @ Wacken"`, and `"- Live / Take 1"` that R leaves untouched. Once corrected to match R's actual regex precision, the D1+D2 match rate became **exact** — 264,478 rows, 80.12%, to the decimal point.

A small residual gap remained on the D3 join (0.03%) with a known, precisely diagnosed cause (R exact-matches bare `"(live)"`; the current engine can only do substring-contains matching for that pattern). A quick test proved that "fixing" it with a looser tag introduces a real false positive (`"life's too long (to live like this)"` — a lyric, not a live-performance tag — would get wrongly stripped). Leaving a small, understood, verified-safe gap beat forcing a fix that trades one bug for another.

---

## Decision Flow

```
03 hands off wrangled_D1/D2/D3.pkl (with join_key already built)
    ↓
Dedup + left-join D2 onto D1 → match rate looks reasonable?
    → No, and the gap is small → don't guess. Run R directly, diff the actual join_key sets.
    → Diff shows a real config gap → fix CLEANING_RULES against R's literal source regex, not the stats-derived summary
    → Re-verify: did the fix change the numbers? No change on a symmetric bug is expected, not a failure.
    ↓
Dedup + left-join D3 → full validation → save
```

---

## ⚠️ Common Mistakes

| Mistake | Cause | Fix |
|---|---|---|
| Accepting a small numeric mismatch as "probably rounding" | No R environment assumed to be available | Check first — a local R install (even without a Jupyter kernel) can run the original logic directly for an exact diff |
| Trusting a config that "looks statistically reasonable" | Previous stage derived cleaning rules from aggregate patterns in the data, not line-by-line from the source language's regex | Read the original R (or other source) function itself before trusting a config that was *inspired by* it |
| Blanket-fixing a regex bug across every case it might apply to | Assuming the fix is uniform | Test the fix against every affected case first — a boundary fix that's correct for one marker (`with`) broke another (`feat.`) because they don't share the same shape |
| Forcing a fix to close the last few percentage points of a gap | Treating "100% match" as the goal instead of "correctly matching" | If the closest safe approximation still introduces new false positives, a small, diagnosed, deliberately-left gap is the better outcome |
| Carrying over every column a secondary table offers | Not checking for name collisions with columns already in the base table | Explicitly select only the columns that don't collide — verified against what the original pipeline actually selected, not assumed |

---

*Part of [Fu Wei's Data Analysis Pipeline](../README.md)*
