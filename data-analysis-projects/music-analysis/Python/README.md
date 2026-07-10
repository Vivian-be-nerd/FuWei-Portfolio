# Python Version

Converting the R pipeline to Python, stage by stage. Built with a CONFIG/engine
separation so new datasets only require adding a config entry, not new code.

| File | Stage | Status |
|------|-------|--------|
| 01_data_exploration_auto.py | Data Exploration | ✅ Complete |
| 02_data_pattern_analysis.py | Pattern Analysis | 🔜 Planned |
| 03_data_wrangling.py | Data Wrangling | 🔜 Planned |
| 04_data_Joining.py | Data Joining | 🔜 Planned |
| 05_EDA.py | EDA | 🔜 Planned |
| 06_modeling.py | Modeling | 🔜 Planned |
| 07_Final_Report.py | Final Report | 🔜 Planned |

See [`pipeline-guides/01_data_exploration.md`](../../../pipeline-guides/01_data_exploration.md)
for the design principles behind this script (CONFIG/engine separation, and why
statistical outlier detection is reported as `[INFO]` rather than auto-cleaned).
