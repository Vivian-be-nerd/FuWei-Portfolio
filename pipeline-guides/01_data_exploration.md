# 📊 01 Data Exploration Guide


## Universal Data Exploration Template

**Applicable to:** Any structured dataset (CSV, Excel, Database)  
**Purpose:** Understand data quality and characteristics to prepare for further analysis  
**Last Updated:** June 2026

---

## 📋 Preparation

### Before you start, ask yourself:
1. Where does this dataset come from?
2. Is there official documentation?
3. What does each column represent?
4. What is the expected value range?

> ⚠️ **Important: Understand your data before you start coding!**

---

## Step 1: Import Package

```python
import pandas as pd
```

---

## Step 2: Read Data

### Basic Read
```python
df = pd.read_csv("file.csv")
```

### Decision Rules

| Situation | Method | Example | Dataset Source |
|-----------|--------|---------|----------------|
| Regular CSV | `pd.read_csv("file.csv")` | D1 Billboard | [Link →](https://www.kaggle.com/datasets/dhruvildave/billboard-the-hot-100-songs) |
| Multiple files to merge | `loop + pd.concat()` | D2 Spotify | [Link →](https://www.kaggle.com/datasets/theoverman/the-spotify-hit-predictor-dataset) |
| CSV with extra index column | `pd.read_csv("file.csv", index_col=0)` | D3 Music Dataset | [Link →](https://www.kaggle.com/datasets/saurabhshahane/music-dataset-1950-to-2019) |

---

## Step 3: Validation — Quick Check

### 3.1 Size of DataFrame

```python
rows, cols = df.shape
print(f'Datasize: ({rows:,}, {cols:,})')
```

#### Date Range Validation

> ⚠️ **Key Decision: Is the column a full date or year only?**

| Column Format | Example | Method |
|--------------|---------|--------|
| Full date | `2021-01-15` | `pd.to_datetime()` → `.dt.year` |
| Year only | `1950` | Use `.min()` / `.max()` directly |

```python
# ✅ Full date (e.g. D1 Billboard)
df['date'] = pd.to_datetime(df['date'])
min_year = df['date'].dt.year.min()
max_year = df['date'].dt.year.max()

# ✅ Year only (e.g. D3 Music Dataset)
min_year = df['release_date'].min()
max_year = df['release_date'].max()

# ❌ Wrong! Never use pd.to_datetime() on year-only columns
# 1950 will become 1970-01-01 00:00:00.000001950
```

---

### 3.2 Column Names

```python
list(df)
```

---

### 3.3 Column Value Check

#### a. Duplicate Check
> ⚠️ **Always do this first! Confirm data is clean before other checks.**

```python
dup_count = df.duplicated().sum()
print(f"Duplicate rows: {dup_count:,}")

if dup_count == 0:
    print("✅ Data is clean, no duplicates!")
else:
    print(f"⚠️ Found {dup_count:,} duplicate rows!")
```

#### b. Column Reference
Before running the health check, understand what each column means:

| Column | Description | Normal Range | Is 0 Valid? |
|--------|-------------|-------------|-------------|
| (fill in based on dataset) | | | |

> 💡 **Tip:** Check the official documentation or Kaggle dataset description
> to understand each column's meaning and expected range.

#### c. check_data_quality — Health Check

```python
def check_data_quality(df, name):
    print(f"{'='*50}")
    print(f"📊 {name} Data Quality Check")
    print(f"{'='*50}")

    for col in df.columns:
        nan   = df[col].isna().sum()
        zero  = (df[col] == 0).sum()
        blank = (df[col].astype(str).str.strip() == '').sum()

        if nan > 0 or zero > 0 or blank > 0:
            print(f"\n⚠️ {col}")
            if nan   > 0: print(f"  NaN  : {nan:,}")
            if zero  > 0: print(f"  0    : {zero:,}")
            if blank > 0: print(f"  Blank: {blank:,}")

    print("\n✅ Check complete!")

# Usage
check_data_quality(df, "Dataset Name")
```

> ⚠️ **Whether 0 is valid depends on the business logic of each column!**

| 0 is NOT valid | 0 IS valid |
|----------------|-----------|
| `tempo = 0` (no song has 0 BPM) | `mode = 0` (0 = minor key) |
| `rank = 0` (no rank 0 on charts) | `target = 0` (0 = Flop) |
| `sections = 0` (at least 1 section) | `danceability = 0` (valid) |

---

### 3.4 Detailed Info

```python
df.info()
df.isna().sum()
```

---

## Step 4: Summary Template

### Validation Results

| Check Item | Method | Result |
|-----------|--------|--------|
| Row Duplicates | df.duplicated().sum() | ✅ 0 rows |
| Missing Values | df.isna().sum() | ✅ / ⚠️ |
| Zero Values | check_data_quality() | ✅ / ⚠️ |
| Blank Values | check_data_quality() | ✅ / ⚠️ |

### ✅ No Issues Found
- (List all columns with no problems)

### ⚠️ Issues Found
| Column | Issue | Description | Action |
|--------|-------|-------------|--------|
|        |       |             |        |

### 🔜 Next Step
- Above issues will be handled in `03_data_wrangling`.
- Patterns and distributions worth analyzing will be explored in `02_data_pattern_analysis`.

---

## ⚠️ Common Mistakes

| Mistake | Cause | Fix |
|---------|-------|-----|
| Using `pd.to_datetime()` on year-only columns | Assumed it was a full date | Check column format first |
| Outputting large DataFrame directly | No output control | Use `print()` or `.shape[0]` |
| Overwriting original variables during practice | Same variable name | Use `_exe` suffix for practice |
| Kernel crash | Rendering too much data | Stop execution, add `print()` |
| Treating all NaN as errors | No understanding of business logic | Understand column meaning first |
| Assuming no 0/blank issues when NaN = 0 | Only checked NaN | Always check all three: NaN, 0, blank |

---

## 📝 Decision Flow

```
// Step 1: Read Data //
        ↓

// Step 2: Multiple files? //
  → Yes → loop + pd.concat()
  → No  → pd.read_csv()
        ↓

// Step 3: Extra index column? //
  → Yes → index_col=0
  → No  → Normal read
         ↓

// 3.1 Size of DataFrame //
  → Does the column have dates?
    → Full date   → pd.to_datetime()
    → Year only   → Use numbers directly
         ↓
3.2 Column Names
  → list(df)
  ↓
3.3 Column Value Check
  1. Duplicate Check      ← Always first!
  2. Column Reference     ← Understand each column
  3. check_data_quality   ← Health check (NaN, 0, blank)
  ↓
3.4 Detailed Info
  → df.info()
  → df.isna().sum()
  ↓
Is 0 valid?
  → Check business logic of that column
  → Not sure → Check official documentation
         ↓

// Step 4: Summary //
  → List all check results
  → Flag problem columns
  → State next steps
```

---


*Part of [Fu Wei's Data Analysis Pipeline](../README.md)*
