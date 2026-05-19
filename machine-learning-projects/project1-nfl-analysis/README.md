# NFL Game Outcome Analysis

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![SAS](https://img.shields.io/badge/SAS-9.4+-1f425f.svg)
![scikit-learn](https://img.shields.io/badge/scikit--learn-ML-orange.svg)
![Team Project](https://img.shields.io/badge/Team-4%20Members-blue.svg)

> **Team Collaboration Project** | MIS5560 Data Science | Oakland University

**Research Question**: Which offensive and defensive performance metrics have the greatest impact on winning in the NFL?

---

## 👥 Team & Contributions

This was a collaborative team project where each member implemented a different classification model.

| Team Member | Model | Tool | Accuracy |
|-------------|-------|------|----------|
| **Fu Wei (Me)** | **Decision Tree** | **Python** | **87.03%** |
| Jalen | Neural Network | SAS | 92.66% |
| Keila | Logistic Regression | SAS | 92.00% |
| Darshil | Random Forest | Python | 87.61% |

---

## 🎯 My Contribution: Decision Tree Implementation

### What I Did

I was responsible for developing and optimizing the **Decision Tree classification model** to identify which performance metrics most strongly predict NFL game outcomes.

### My Technical Work

#### 1. **Data Specification Testing**
Compared two approaches to feature engineering:
- **V1 (Seasonal Averages)**: Team cumulative season statistics
- **V2 (Single-Game Statistics)**: Game-level data with engineered features like `turnover_differential`

**Result**: V2 dramatically outperformed V1 (87.03% vs 76-77% accuracy)

#### 2. **Model Optimization**
Tested multiple configurations:
- **80/20 split** (training/validation)
- **70/30 split** (training/validation)
- Hyperparameter tuning for optimal tree depth and split criteria

**Best Configuration**: V2 with 80/20 split → **87.03% validation accuracy**

#### 3. **Feature Importance Analysis**
Used Gini impurity to rank predictive features:

| Rank | Feature | Importance | Description |
|------|---------|-----------|-------------|
| 1 | `def_total_off_points` | **51.39%** | Opponent points scored |
| 2 | `off_pass_td_pct` | 13.95% | Passing TD percentage |
| 3 | `off_rush_touchdown` | 13.70% | Rushing touchdowns |
| 4 | `off_total_off_yards` | 8.32% | Total offensive yards |
| 5 | `off_pass_touchdown` | 7.03% | Passing touchdowns |

**Key Insight**: Defense dominates the model—over half of the tree's predictive power comes from a single defensive metric.

#### 4. **Model Evaluation**
- **Validation Accuracy**: 87.03%
- **Overfitting**: -3.13% (acceptable, well-controlled)
- **Interpretability**: Highly transparent decision rules make it valuable for coaches and analysts

---

## 📊 Team Results & Findings

### Model Performance Comparison

| Model | Validation Accuracy | Overfitting | Key Strength |
|-------|---------------------|-------------|--------------|
| Neural Network (Jalen) | 92.66% | -0.11% | Highest accuracy, complex patterns |
| Logistic Regression (Keila) | 92.00% | -0.01% | Best interpretability, near-zero overfitting |
| Random Forest (Darshil) | 87.61% | -4.95% | Robust ensemble method |
| **Decision Tree (Me)** | **87.03%** | **-3.13%** | **Highly interpretable, mirrors coaching logic** |

### Key Team Findings

1. **🛡️ Defense Wins Games**
   - `def_total_off_points` was the #1 predictor across **all four models**
   - Accounted for 27-51% of predictive power depending on model
   - **Insight**: Limiting opponent scoring is the highest-value investment

2. **🎯 Red Zone Execution > Total Yardage**
   - Passing and rushing touchdowns significantly outranked total yards
   - **Insight**: Finishing drives matters more than accumulating yards

3. **📊 Single-Game Data Dramatically Outperforms Averages**
   - V2 models: 87-93% accuracy
   - V1 models: 65-80% accuracy
   - **Insight**: Game-level dynamics capture more signal than historical trends

4. **🔄 Turnover Differential is Critical**
   - Engineered feature directly impacts win probability
   - **Insight**: Force turnovers and protect the ball

5. **⚖️ Offensive Balance Matters**
   - `off_pass_pct` appeared as significant across models
   - **Insight**: One-dimensional offenses are easier to defend

---

## 📁 Project Structure

```
nfl-game-outcome-analysis/
│
├── README.md                              # This file
│
├── notebooks/                             # My Decision Tree notebooks
│   ├── DecisionTree_V1_2.8_0406.ipynb     # V1 specification testing
│   ├── DecisionTree_V2_2.8_0406.ipynb     # V2 80/20 split
│   └── DecisionTree_V2_3.7_0406.ipynb     # V2 70/30 split
│
├── sas_code/                              # Team SAS implementations
│   ├── NFL_Logistic_Regression.sas        # Keila's logistic regression
│   └── Weekly_team_com_NN.sas             # Jalen's neural network
│
├── presentation/                          # Team presentation materials
│   └── NFL_Analysis_Slides.pptx
│
└── report/                                # Complete team report
    └── Final_Project_Report.pdf
```

---

## 📊 Dataset

**Source**: [NFL Stats (2012-2024) via Kaggle](https://www.kaggle.com/datasets/philiphyde1/nfl-stats-1999-2022)

### Dataset Quality
- **Original**: 7,088 team-game records
- **Cleaned**: 6,972 records (removed 116 rows with missing point values)
- **Class Balance**: 51.66% Loss / 48.33% Win (near-perfect balance)

### Features
- **175 total variables**
  - Offensive metrics: passing, rushing, total yards, touchdowns, efficiency
  - Defensive metrics: points allowed, yards allowed, defensive efficiency
  - Engineered features: `turnover_differential`
- **Target Variable**: `game_result` (1 = Win, 0 = Loss)

---

## 🛠️ Technologies Used

### My Implementation (Decision Tree)
- **Python 3.8+**
- **Libraries**: 
  - `scikit-learn` - Decision Tree Classifier
  - `pandas` - Data manipulation
  - `numpy` - Numerical computing
  - `matplotlib` / `seaborn` - Visualization
- **Jupyter Notebook** - Interactive development and documentation

### Team Tools
- **SAS 9.4+** - PROC LOGISTIC, HPNEURAL (Logistic Regression, Neural Network)
- **Python** - Random Forest implementation

---

## 🚀 How to Run My Decision Tree Analysis

### Prerequisites
```bash
python >= 3.8
pip install scikit-learn pandas numpy matplotlib seaborn jupyter
```

### Running the Notebooks

1. **Clone or download this repository**

2. **Navigate to the notebooks folder**
```bash
cd notebooks/
```

3. **Launch Jupyter Notebook**
```bash
jupyter notebook
```

4. **Open and run notebooks in order**:
   - `DecisionTree_V1_2.8_0406.ipynb` - See V1 baseline performance
   - `DecisionTree_V2_2.8_0406.ipynb` - My best model (87.03% accuracy)
   - `DecisionTree_V2_3.7_0406.ipynb` - Alternative split testing

---

## 📈 My Decision Tree Results

### Performance Metrics
- **Validation Accuracy**: 87.03%
- **Training Accuracy**: 90.16%
- **Overfitting**: -3.13% (well-controlled)

### Feature Importance (Top 5)
1. `def_total_off_points` - **51.39%** (dominant)
2. `off_pass_td_pct` - 13.95%
3. `off_rush_touchdown` - 13.70%
4. `off_total_off_yards` - 8.32%
5. `off_pass_touchdown` - 7.03%

### Key Takeaway from My Analysis
Defense alone accounts for over **half** of my Decision Tree's predictive power. This finding was consistent across all four team models, validating the "defense wins championships" principle with quantitative evidence.

---

## 💡 Managerial Insights

Based on our team's comprehensive analysis:

### For NFL Teams
1. **Invest heavily in defensive talent** - Points allowed is the #1 predictor
2. **Prioritize red zone offense** - Touchdowns matter more than yards
3. **Emphasize turnover margin** - Protect the ball and force takeaways
4. **Maintain offensive balance** - Don't become one-dimensional

### For Analytics Teams
1. **Use game-level data** - Single-game stats dramatically outperform seasonal averages
2. **Engineer features thoughtfully** - `turnover_differential` proved highly predictive
3. **Compare multiple models** - Different models revealed complementary insights
4. **Prioritize interpretability** - Decision Trees and Logistic Regression provide actionable rules

---

## 🔮 Future Work

Potential extensions identified by the team:

1. **Remove dominant feature**: Test performance excluding `def_total_off_points`
2. **Era analysis**: Compare different NFL eras (1990s run-heavy vs modern pass-heavy)
3. **Player-level granularity**: Incorporate individual player statistics
4. **Real-time prediction**: Develop live in-game win probability models
5. **Weather impact**: Add environmental factors

---

## 🎓 Academic Context

- **Course**: MIS5560 - Data Science
- **Institution**: Oakland University, School of Business Administration
- **Instructor**: Dr. Hongyu Gao
- **Semester**: Winter 2026
- **Team Size**: 4 members
- **Project Type**: Collaborative machine learning analysis

---

## 📝 Citation

If you reference this project, please cite:

```bibtex
@misc{hsu2026nfl,
  author = {Hsu, Fu Wei and Team},
  title = {NFL Game Outcome Analysis: Identifying Key Performance Metrics Through Classification Modeling},
  year = {2026},
  course = {MIS5560 Data Science},
  institution = {Oakland University}
}
```

---

## 📧 Contact

**Fu Wei Hsu** (Decision Tree Implementation)

- **Email**: fuwei.hsu1988@gmail.com
- **LinkedIn**: [Fu Wei Hsu](https://www.linkedin.com/in/vivianfuweihsu)
- **GitHub**: [@Vivian-be-nerd](https://github.com/Vivian-be-nerd)
- **Portfolio**: [Data Analytics Portfolio](https://github.com/Vivian-be-nerd/FuWei-Portfolio)

---

## 🙏 Acknowledgments

- **Team Members**: Jalen (Neural Network), Keila (Logistic Regression), Darshil (Random Forest)
- **Dr. Hongyu Gao** - Course instructor and project advisor
- **Oakland University** - School of Business Administration
- **Kaggle** - NFL dataset provider

---

[← Back to Machine Learning Projects](../ML_README.md) | [← Back to Portfolio](../../README.md)
