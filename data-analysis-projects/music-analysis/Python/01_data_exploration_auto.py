# %% [markdown]
# ---
# title: "01 Data Exploration"
# author: "Fu Wei Hsu"
# format:
#   html:
#     theme: cosmo
#     toc: true
#     toc-location: right
#     toc-title: "On this page"
#     embed-resources: true
# ---

# %% [markdown]
# # 01 — Data Exploration
#
# **Research question:** before any cleaning or joining happens, is this dataset
# actually usable — right size, right date range, no silent gaps? This stage is
# a health check, not an analysis: it answers "can I trust this data enough to
# build on top of it," and hands off a list of known issues to the next stage.
#
# **This is a runnable CLI script, not a notebook.** Point it at any CSV (or a
# Kaggle dataset) and it prints the same 8-step report — no code changes needed
# to explore a new dataset, only a new CONFIG entry.

# %% [markdown]
# ## Architecture
#
# One generic health-check engine (`run_exploration()`), reused across as many
# datasets as you register in `DATASETS` — that's the whole point of CONFIG/engine
# separation: adding a fourth dataset later means adding one dict entry, not writing
# a fourth copy of this logic.
#
# | | |
# |---|---|
# | **CONFIG** | `DATASETS` dict — one entry per dataset: how to load it, its column definitions, expected ranges, and where to save the validated result |
# | **Engine** | `load_data()` (CSV or Kaggle) + `run_exploration()` (the 8-step report) — both generic, neither one knows anything about Billboard or Spotify specifically |
# | **Entry point** | 3 CLI modes: `--dataset d1/d2/d3/all` (built-in configs), `--csv <path>` (any new CSV, ad hoc), or no args (falls back to the CONFIG block below) |

# %% [markdown]
# ## Step Blueprint
#
# Every step below is machine-concluded ([OK]/[WARN]) — unlike later stages,
# 01 never needs human judgment, because "is this row a duplicate" and "is this
# rank inside 1-100" are objective checks, not interpretation calls.
#
# | Step | What It Checks | Question Answered |
# |------|------|------|
# | **Step 1** | Dataset Size | How many rows/columns, and what are they? |
# | **Step 2** | Date Range | What time period does this data actually cover? |
# | **Step 3** | Duplicate Row Check | Are there exact duplicate rows? |
# | **Step 4** | NaN / Zero / Blank Health Check | Which columns have missing, zero, or blank values? |
# | **Step 5** | Advanced NaN Analysis | Do the missing values follow an expected pattern (e.g. chart debut vs. re-entry), or are they unexplained? |
# | **Step 6** | Column Value Range Validation | Does every value fall inside its expected range (e.g. chart rank 1-100)? |
# | **Step 6b** | IQR Outlier Detection | Are there statistical outliers? Reported as `[INFO]` only — an outlier isn't necessarily an error (a song with an unusually long chart run is real data), so this always needs a human to look, never auto-cleaned. |
# | **Step 7** | Summary | Roll everything above into one health report — what needs fixing in the next stage? |
# | **Step 8** | Save Validated Data | Persist the validated dataframe to `.pkl` so the next stage can load it directly. |

# %%
"""
01_data_exploration_auto.py
============================
Automated Data Exploration Script -- mirrors the structure of 01_data_exploration.ipynb

Two data source modes:
  Mode 1 (SOURCE = "csv")    -> Load from a local CSV file path
  Mode 2 (SOURCE = "kaggle") -> Auto-download from Kaggle API

Getting Kaggle API Key:
  Kaggle -> top-right avatar -> Settings -> API -> Create New Token
  -> Download kaggle.json (contains username and key)
  -> Place at: C:\\Users\\fuwei\\.kaggle\\kaggle.json

Author: Fu Wei Hsu
"""

import sys
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding='utf-8')

import pandas as pd
import os
import argparse

# %% [markdown]
# ## CONFIG — Only edit this section when switching datasets
#
# Everything that changes when you point this script at a *new* dataset lives
# here: where the data comes from, what each column means, and what "valid"
# looks like for it. None of this logic reaches into the engine below —
# `run_exploration()` never hardcodes a column name.

# %%
# ============================================================
# CONFIG -- Only edit this section when switching datasets
# ============================================================

# Data source: "csv" or "kaggle"
SOURCE = "csv"

# -- Mode 1: Local CSV --
CSV_PATH = "../Data/Data1_charts.csv"

# -- Mode 2: Kaggle API --
# Credentials are read automatically from kaggle.json -- do NOT hardcode here
# kaggle.json location: C:\Users\fuwei\.kaggle\kaggle.json
KAGGLE_DATASET  = "dhruvildave/billboard-the-hot-100-songs"
KAGGLE_FILENAME = "charts.csv"

# -- Shared settings --
DATASET_NAME = "D1 Billboard Hot 100"
DATE_COLUMN  = "date"   # Date column name, set None if not applicable
SAVE_PATH    = None     # Where to save the validated data as .pkl for 02+ to read; None = don't save

COLUMN_DEFS = {
    "date":           {"desc": "Weekly date (1958-2021)",   "zero_ok": False, "range": None},
    "rank":           {"desc": "Chart rank",                "zero_ok": False, "range": (1, 100)},
    "song":           {"desc": "Song title",                "zero_ok": False, "range": None},
    "artist":         {"desc": "Artist name",               "zero_ok": False, "range": None},
    "last-week":      {"desc": "Last week rank (NaN=Debut)","zero_ok": False, "range": (1, 100)},
    "peak-rank":      {"desc": "Peak rank (all-time best)", "zero_ok": False, "range": (1, 100)},
    "weeks-on-board": {"desc": "Weeks on chart",            "zero_ok": False, "range": (1, None)},
}

ADVANCED_NAN_CHECK = {
    "nan_col":   "last-week",
    "group_col": "weeks-on-board",
    "debut_val": 1,
}

# %% [markdown]
# ## Engine — No edits needed below this line
#
# `load_data()` and `run_exploration()` are generic: they take a dataframe plus
# a CONFIG dict and produce the 8-step report. Neither function contains a
# dataset-specific `if` branch — that's the test for whether CONFIG/engine
# separation is actually holding, not just claimed.

# %%
# ============================================================
# No edits needed below this line
# ============================================================

def load_data(source, csv_path, kaggle_dataset, kaggle_filename):
    """Load data from CSV or Kaggle."""

    if source == "csv":
        print(f"[INFO] Loading CSV: {csv_path}")
        return pd.read_csv(csv_path)

    elif source == "kaggle":
        print(f"[INFO] Downloading from Kaggle: {kaggle_dataset}")
        print(f"       Credentials: C:\\Users\\fuwei\\.kaggle\\kaggle.json (auto-read)")

        try:
            import kagglehub
            # kagglehub auto-reads ~/.kaggle/kaggle.json -- no credentials in script
            path = kagglehub.dataset_download(kaggle_dataset)
            csv_file = os.path.join(path, kaggle_filename)
            print(f"[OK]   Download complete: {csv_file}")
            return pd.read_csv(csv_file)

        except ImportError:
            print("[WARN] kagglehub not installed, installing now...")
            os.system("pip install kagglehub -q")
            import kagglehub
            path = kagglehub.dataset_download(kaggle_dataset)
            csv_file = os.path.join(path, kaggle_filename)
            return pd.read_csv(csv_file)

        except Exception as e:
            print(f"[ERROR] Download failed: {e}")
            print(f"        Check that kaggle.json is at: C:\\Users\\fuwei\\.kaggle\\kaggle.json")
            raise

    else:
        raise ValueError(f"SOURCE must be 'csv' or 'kaggle', got: {source}")


def _parse_decade_label(label):
    """Convert a 'NNs' decade shorthand (e.g. '60s', '00s') to a starting year.
    Assumes the modern convention: 00-19 = 2000s/2010s, 20-99 = 1900s. Generic
    across any decade-labeled dataset, not specific to D2."""
    n = int(label.rstrip("sS"))
    return 2000 + n if n < 20 else 1900 + n


def run_exploration(df, dataset_name, date_col, col_defs, advanced_nan, chart_size=None,
                     save_path=None, year_col=None, year_col_type=None):
    """Run the full 01 Data Exploration workflow.

    year_col / year_col_type: fallback for datasets with NO full date column but
    that still carry *some* year signal -- e.g. a plain int year column
    (year_col_type='year_int') or a decade-label column (year_col_type='decade_label').
    Never fed through pd.to_datetime() -- that mangles year-only values (see
    Common Mistakes: 'Year-only columns: NEVER use pd.to_datetime()')."""

    sep = "=" * 55

    # Parse date column
    if date_col and date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], errors='coerce')

    print(f"\n{sep}")
    print(f"  {dataset_name}")
    print(f"{sep}")

    # -- STEP 1: Dataset size --
    rows, cols = df.shape
    print(f"\n[STEP 1] Dataset Size")
    print(f"  Datasize : ({rows:,} rows, {cols:,} columns)")
    print(f"  Columns  : {list(df.columns)}")

    # -- STEP 2: Date range --
    print(f"\n[STEP 2] Date Range")
    if date_col and date_col in df.columns and pd.api.types.is_datetime64_any_dtype(df[date_col]):
        min_y = df[date_col].dt.year.min()
        max_y = df[date_col].dt.year.max()
        print(f"  Date range : {min_y} - {max_y}  ({max_y - min_y} years)")
        if chart_size:
            print(f"  ~Weeks     : {rows // chart_size:,} weeks")
    elif year_col and year_col in df.columns and year_col_type == "year_int":
        min_y = int(df[year_col].min())
        max_y = int(df[year_col].max())
        print(f"  Date range : {min_y} - {max_y}  ({max_y - min_y} years)")
        print(f"  Note       : from '{year_col}' (year-only column, not a full date -- no week-level detail)")
    elif year_col and year_col in df.columns and year_col_type == "decade_label":
        starts = sorted(_parse_decade_label(v) for v in df[year_col].unique())
        min_y, max_y = starts[0], starts[-1] + 9
        print(f"  Decade range : {min_y}s - {max_y - 9}s  (~{max_y - min_y} years, {len(starts)} decades represented)")
        print(f"  Note         : from '{year_col}' (decade label only -- no exact per-row year available)")
    else:
        print(f"  No date column, skipping.")

    # -- STEP 3: Duplicate rows --
    print(f"\n[STEP 3] Duplicate Row Check")
    dup = df.duplicated().sum()
    print(f"  Duplicate rows: {dup:,}  {'[OK] No duplicates' if dup == 0 else '[WARN] Duplicates found!'}")

    # -- STEP 4: NaN / Zero / Blank health check --
    print(f"\n[STEP 4] NaN / Zero / Blank Health Check")
    issues = []
    for col in df.columns:
        nan     = df[col].isna().sum()
        zero    = (df[col] == 0).sum() if df[col].dtype not in ["object", "datetime64[ns]"] else 0
        blank   = (df[col].astype(str).str.strip() == "").sum()
        zero_ok = col_defs.get(col, {}).get("zero_ok", False)
        desc    = col_defs.get(col, {}).get("desc", "")
        label   = f"{col}" + (f" ({desc})" if desc else "")

        warn_zero = 0 if zero_ok else zero
        if nan > 0 or warn_zero > 0 or blank > 0:
            print(f"\n  [WARN] {label}")
            if nan       > 0: print(f"         NaN   : {nan:,}")
            if warn_zero > 0: print(f"         Zero  : {warn_zero:,}")
            if blank     > 0: print(f"         Blank : {blank:,}")
            issues.append({"col": col, "nan": nan, "zero": warn_zero, "blank": blank})
        else:
            print(f"  [OK]   {label}")

    # -- STEP 5: Advanced NaN analysis --
    if advanced_nan:
        nan_col   = advanced_nan["nan_col"]
        group_col = advanced_nan["group_col"]
        debut_val = advanced_nan["debut_val"]

        if nan_col in df.columns and group_col in df.columns:
            nan_df  = df[df[nan_col].isna()]
            debut   = nan_df[nan_df[group_col] == debut_val]
            reentry = nan_df[nan_df[group_col] != debut_val]
            total   = len(debut) + len(reentry)
            match   = "[OK]" if total == len(nan_df) else "[ERROR]"

            print(f"\n[STEP 5] Advanced NaN Analysis: '{nan_col}'")
            print(f"  Total NaN rows : {len(nan_df):,}")
            print(f"  Debut          ({group_col}={debut_val})  : {len(debut):,}")
            print(f"  Re-entry       ({group_col}!={debut_val}) : {len(reentry):,}")
            print(f"  Verified total : {total:,}  {match}")

    # -- STEP 6: Column value range validation --
    print(f"\n[STEP 6] Column Value Range Validation")
    has_range = False
    for col, meta in col_defs.items():
        r = meta.get("range")
        if r and col in df.columns and df[col].dtype not in ["object", "datetime64[ns]"]:
            has_range = True
            actual_min = df[col].min()
            actual_max = df[col].max()
            lo, hi = r
            lo_ok = (lo is None) or (actual_min >= lo)
            hi_ok = (hi is None) or (actual_max <= hi)
            status   = "[OK]  " if (lo_ok and hi_ok) else "[WARN]"
            expected = f"{lo if lo is not None else '?'} ~ {hi if hi is not None else 'inf'}"
            print(f"  {status}  {col}: actual {actual_min} ~ {actual_max}  (expected {expected})")
    if not has_range:
        print(f"  No ranges defined, skipping.")

    # -- STEP 6b: IQR outlier detection (statistical, not a business rule) --
    # NOTE: printed as [INFO], never [WARN] -- a statistical outlier is not
    # necessarily an error (e.g. a song with an unusually long chart run is
    # real data, not a mistake). Always needs human judgment, never auto-cleaned.
    print(f"\n[STEP 6b] IQR Outlier Detection (statistical, for reference only)")
    has_outlier_col = False
    for col in df.columns:
        if df[col].dtype in ["object", "datetime64[ns]"]:
            continue
        series = df[col].dropna()
        if len(series) == 0:
            continue
        q1 = series.quantile(0.25)
        q3 = series.quantile(0.75)
        iqr = q3 - q1
        if iqr == 0:
            continue
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        outlier_count = ((series < lower) | (series > upper)).sum()
        if outlier_count > 0:
            has_outlier_col = True
            pct = outlier_count / len(series) * 100
            print(f"  [INFO]  {col}: {outlier_count:,} outliers ({pct:.1f}%), normal range ~{lower:.2f} to {upper:.2f}")
    if not has_outlier_col:
        print(f"  No statistical outliers detected.")

    # -- STEP 7: Summary --
    print(f"\n[STEP 7] Summary")
    print(f"  {'Check':<26} {'Result'}")
    print(f"  {'-'*42}")
    total_nan   = sum(i["nan"]   for i in issues)
    total_zero  = sum(i["zero"]  for i in issues)
    total_blank = sum(i["blank"] for i in issues)
    print(f"  {'Duplicate rows':<26} {'[OK] 0 rows' if dup == 0 else f'[WARN] {dup:,} rows'}")
    print(f"  {'Missing values (NaN)':<26} {'[OK] 0 rows' if total_nan == 0 else f'[WARN] {total_nan:,} rows'}")
    print(f"  {'Zero values':<26} {'[OK] 0 rows' if total_zero == 0 else f'[WARN] {total_zero:,} rows'}")
    print(f"  {'Blank values':<26} {'[OK] 0 rows' if total_blank == 0 else f'[WARN] {total_blank:,} rows'}")

    if issues:
        print(f"\n  [NOTE] Columns to address in 03_data_wrangling:")
        for i in issues:
            parts = []
            if i["nan"]   > 0: parts.append(f"NaN:{i['nan']:,}")
            if i["zero"]  > 0: parts.append(f"Zero:{i['zero']:,}")
            if i["blank"] > 0: parts.append(f"Blank:{i['blank']:,}")
            print(f"     -> {i['col']}  ({', '.join(parts)})")
    else:
        print(f"\n  [OK] No issues found. Data quality is good.")

    # -- STEP 8: Save validated data to pickle (so 02+ can pick it up) --
    print(f"\n[STEP 8] Save Validated Data")
    if save_path:
        df.to_pickle(save_path)
        print(f"  [OK]  Saved to: {save_path}")
    else:
        print(f"  No save_path given, skipping. (02+ will not find a .pkl file for this dataset)")

    print(f"\n{sep}\n")
    return df

# %% [markdown]
# ## Built-in Dataset Configs
#
# This is the same CONFIG idea as above, just registered for all three project
# datasets at once. Adding a fourth dataset later means adding one more key here
# — `load`, `col_defs`, and everything else follow the same shape.

# %%
# -- Built-in dataset configs --------------------------------------
DATASETS = {
    "d1": {
        "name": "D1 Billboard Hot 100",
        "date_col": "date",
        "chart_size": 100,
        "save_path": r"..\Data\cleaned_D1.pkl",
        "load": lambda base: pd.read_csv(os.path.join(base, "Data1_charts.csv"), parse_dates=["date"]),
        "col_defs": {
            "date":           {"desc": "Weekly date",        "zero_ok": False, "range": None},
            "rank":           {"desc": "Chart rank",         "zero_ok": False, "range": (1, 100)},
            "song":           {"desc": "Song title",         "zero_ok": False, "range": None},
            "artist":         {"desc": "Artist name",        "zero_ok": False, "range": None},
            "last-week":      {"desc": "Last week rank",     "zero_ok": False, "range": (1, 100)},
            "peak-rank":      {"desc": "Peak rank",          "zero_ok": False, "range": (1, 100)},
            "weeks-on-board": {"desc": "Weeks on chart",     "zero_ok": False, "range": (1, None)},
        },
        "advanced_nan": {"nan_col": "last-week", "group_col": "weeks-on-board", "debut_val": 1},
    },
    "d2": {
        "name": "D2 Spotify Hit Predictor",
        "date_col": None,
        "year_col": "decade",
        "year_col_type": "decade_label",
        "save_path": r"..\Data\cleaned_D2.pkl",
        "load": lambda base: pd.concat([
            pd.read_csv(os.path.join(base, f"Data2_dataset-of-{d}.csv")).assign(decade=d)
            for d in ["60s", "70s", "80s", "90s", "00s", "10s"]
        ], ignore_index=True),
        "col_defs": {
            "track":            {"desc": "Track title",      "zero_ok": False},
            "artist":           {"desc": "Artist name",      "zero_ok": False},
            "danceability":     {"desc": "Danceability",     "zero_ok": True,  "range": (0, 1)},
            "energy":           {"desc": "Energy",           "zero_ok": True,  "range": (0, 1)},
            "key":              {"desc": "Key",              "zero_ok": True,  "range": (0, 11)},
            "loudness":         {"desc": "Loudness",         "zero_ok": True},
            "mode":             {"desc": "Mode (maj/min)",   "zero_ok": True,  "range": (0, 1)},
            "speechiness":      {"desc": "Speechiness",      "zero_ok": True,  "range": (0, 1)},
            "acousticness":     {"desc": "Acousticness",     "zero_ok": True,  "range": (0, 1)},
            "instrumentalness": {"desc": "Instrumentalness", "zero_ok": True,  "range": (0, 1)},
            "liveness":         {"desc": "Liveness",         "zero_ok": True,  "range": (0, 1)},
            "valence":          {"desc": "Valence",          "zero_ok": True,  "range": (0, 1)},
            "tempo":            {"desc": "Tempo (BPM)",      "zero_ok": False, "range": (1, None)},
            "duration_ms":      {"desc": "Duration (ms)",    "zero_ok": False, "range": (1, None)},
            "time_signature":   {"desc": "Time signature",   "zero_ok": False, "range": (1, None)},
            "chorus_hit":       {"desc": "Chorus hit time",  "zero_ok": False},
            "sections":         {"desc": "Sections count",   "zero_ok": False, "range": (1, None)},
            "target":           {"desc": "Hit/Flop (0/1)",   "zero_ok": True,  "range": (0, 1)},
        },
        "advanced_nan": None,
    },
    "d3": {
        "name": "D3 Music Dataset 1950-2019",
        "date_col": None,
        "year_col": "release_date",
        "year_col_type": "year_int",
        "save_path": r"..\Data\cleaned_D3.pkl",
        "load": lambda base: pd.read_csv(os.path.join(base, "Data3_tcc_ceds_music.csv"), index_col=0),
        "col_defs": {
            "artist_name":      {"desc": "Artist name",      "zero_ok": False},
            "track_name":       {"desc": "Track title",      "zero_ok": False},
            "release_date":     {"desc": "Release year",     "zero_ok": False, "range": (1950, 2019)},
            "genre":            {"desc": "Genre",            "zero_ok": False},
            "len":              {"desc": "Lyrics length",    "zero_ok": False, "range": (1, None)},
            "loudness":         {"desc": "Loudness",         "zero_ok": False},
            "instrumentalness": {"desc": "Instrumentalness", "zero_ok": True,  "range": (0, 1)},
            "valence":          {"desc": "Valence",          "zero_ok": False, "range": (0, 1)},
            "energy":           {"desc": "Energy",           "zero_ok": False, "range": (0, 1)},
            "danceability":     {"desc": "Danceability",     "zero_ok": True,  "range": (0, 1)},
            "acousticness":     {"desc": "Acousticness",     "zero_ok": True,  "range": (0, 1)},
            "topic":            {"desc": "Main topic",       "zero_ok": False},
        },
        "advanced_nan": None,
    },
}

# %% [markdown]
# ## Entry Point — CLI Usage
#
# Three modes, in priority order:
#
# 1. **`--dataset d1 / d2 / d3 / all`** — run one or all of the built-in configs above
# 2. **`--csv <path>`** — point at any new CSV ad hoc, using the CONFIG block's defaults
# 3. **No arguments** — fall back entirely to the CONFIG block's `SOURCE` / `CSV_PATH` settings, including Kaggle auto-download if `SOURCE = "kaggle"`
#
# ```
# python 01_data_exploration_auto.py --dataset all
# python 01_data_exploration_auto.py --dataset d1
# python 01_data_exploration_auto.py --csv path/to/new_data.csv --name "My Dataset"
# ```

# %%
# -- Entry point -----------------------------------------------
if __name__ == "__main__":

    if "ipykernel" in sys.modules:
        # Running inside a notebook/Quarto render, not a real terminal -- sys.argv
        # holds the kernel's own launcher flags, not ours. Demo all 3 built-in
        # datasets instead of parsing them as CLI args.
        args = argparse.Namespace(dataset="all", csv=None, name=None, data_dir=r"..\Data")
    else:
        parser = argparse.ArgumentParser(description="Automated Data Exploration Script")
        parser.add_argument("--dataset",  type=str, default=None,
                            help="Choose dataset: d1 / d2 / d3 / all (uses --csv mode if omitted)")
        parser.add_argument("--csv",      type=str, default=None, help="Custom CSV file path")
        parser.add_argument("--name",     type=str, default=None, help="Custom dataset name")
        parser.add_argument("--data-dir", type=str, default=r"..\Data",
                            help="Path to Data folder (default: ..\\Data)")
        args = parser.parse_args()

    # -- Mode 1: built-in dataset(s) via --dataset --
    if args.dataset:
        targets = list(DATASETS.keys()) if args.dataset == "all" else [args.dataset.lower()]
        for key in targets:
            if key not in DATASETS:
                print(f"[ERROR] Unknown dataset: {key}  -- use d1 / d2 / d3 / all")
                continue
            cfg = DATASETS[key]
            print(f"\n[INFO] Loading {cfg['name']}...")
            try:
                df = cfg["load"](args.data_dir)
                run_exploration(df, cfg["name"], cfg["date_col"], cfg["col_defs"], cfg["advanced_nan"],
                                 cfg.get("chart_size"), cfg.get("save_path"),
                                 cfg.get("year_col"), cfg.get("year_col_type"))
            except FileNotFoundError as e:
                print(f"[ERROR] File not found: {e}")
                print(f"        Check your Data folder path: {args.data_dir}")

    # -- Mode 2: custom CSV via --csv --
    elif args.csv:
        df = load_data(source="csv", csv_path=args.csv,
                       kaggle_dataset=KAGGLE_DATASET, kaggle_filename=KAGGLE_FILENAME)
        run_exploration(df, args.name or DATASET_NAME, DATE_COLUMN, COLUMN_DEFS, ADVANCED_NAN_CHECK,
                         save_path=SAVE_PATH)

    # -- Mode 3: fallback to CONFIG defaults --
    else:
        df = load_data(source=SOURCE, csv_path=CSV_PATH,
                       kaggle_dataset=KAGGLE_DATASET, kaggle_filename=KAGGLE_FILENAME)
        run_exploration(df, DATASET_NAME, DATE_COLUMN, COLUMN_DEFS, ADVANCED_NAN_CHECK, save_path=SAVE_PATH)
