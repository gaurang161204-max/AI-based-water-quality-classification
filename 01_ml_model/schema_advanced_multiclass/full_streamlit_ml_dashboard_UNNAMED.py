"""
AI-Based Water Quality Classification Dashboard
------------------------------------------------
Run:
    pip install streamlit pandas numpy scikit-learn plotly
    streamlit run water_quality_dashboard.py

Features
  * Demo data (synthetic, guideline-based) OR upload your own CSV
  * Train Random Forest / Gradient Boosting / Logistic Regression
  * Metrics, confusion matrix, ROC curves, permutation feature importance
  * Single-sample prediction with sliders + guideline compliance check
  * Batch prediction from CSV with downloadable results
"""

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.ensemble import GradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, StandardScaler, label_binarize

st.set_page_config(page_title="Water Quality AI Dashboard", page_icon="💧", layout="wide")

# ----------------------------------------------------------------------------
# Approximate drinking-water guideline limits (WHO / BIS style): (min, max)
# Used for the demo data and for the compliance check. Adjust to your standard.
# ----------------------------------------------------------------------------
LIMITS = {
    "pH": (6.5, 8.5),
    "Hardness": (None, 300),          # mg/L
    "TDS": (None, 500),               # mg/L
    "Chloramines": (None, 4),         # mg/L
    "Sulfate": (None, 250),           # mg/L
    "Conductivity": (None, 400),      # µS/cm
    "Organic_Carbon": (None, 4),      # mg/L
    "Trihalomethanes": (None, 80),    # µg/L
    "Turbidity": (None, 5),           # NTU
}

CLASS_COLORS = {"Safe": "#2ca02c", "Marginal": "#f5a623", "Unsafe": "#d62728"}


def color_for(cls, i=0):
    return CLASS_COLORS.get(str(cls), px.colors.qualitative.Set2[i % 8])


def show(fig):
    """Render plotly chart, compatible with old and new Streamlit versions."""
    try:
        st.plotly_chart(fig, width="stretch")
    except TypeError:
        st.plotly_chart(fig, use_container_width=True)


# ----------------------------------------------------------------------------
# Data
# ----------------------------------------------------------------------------
@st.cache_data
def make_synthetic(n=2500, seed=42):
    rng = np.random.default_rng(seed)
    df = pd.DataFrame(
        {
            "pH": rng.normal(7.3, 0.7, n).clip(4, 10.5),
            "Hardness": rng.normal(200, 60, n).clip(40, 450),
            "TDS": rng.normal(380, 180, n).clip(40, 1800),
            "Chloramines": rng.normal(3.0, 1.2, n).clip(0.1, 8),
            "Sulfate": rng.normal(200, 70, n).clip(30, 500),
            "Conductivity": rng.normal(380, 100, n).clip(80, 800),
            "Organic_Carbon": rng.normal(3.2, 1.4, n).clip(0.3, 10),
            "Trihalomethanes": rng.normal(60, 22, n).clip(3, 150),
            "Turbidity": rng.normal(3.0, 1.3, n).clip(0.1, 9),
        }
    )
    # Severity score = total normalised exceedance of guideline limits + noise
    score = np.zeros(n)
    for col, (lo, hi) in LIMITS.items():
        if hi is not None:
            score += np.clip((df[col] - hi) / hi, 0, None)
        if lo is not None:
            score += np.clip((lo - df[col]) / lo, 0, None)
    score += rng.normal(0, 0.05, n)
    q1, q2 = np.quantile(score, [0.45, 0.75])
    df["Quality"] = np.where(score < q1, "Safe", np.where(score < q2, "Marginal", "Unsafe"))
    # Introduce a few missing values, like real sensor data
    for col in ["pH", "Sulfate", "Trihalomethanes"]:
        df.loc[rng.choice(n, int(0.03 * n), replace=False), col] = np.nan
    return df


def load_data():
    st.sidebar.header("📂 Data")