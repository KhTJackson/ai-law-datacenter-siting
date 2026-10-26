"""Shared paths, feature lists & preprocessing for notebooks 05-11.

Every modeling notebook imports from here so feature sets, outlier caps
and cross-validation splits are defined once.
"""

from pathlib import Path

import numpy as np
import pandas as pd
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.model_selection import StratifiedGroupKFold

ROOT = Path(__file__).resolve().parents[1]          # repo root, wherever Jupyter was started
OUT = ROOT / "data" / "cerf_siting" / "output"       # same folder notebooks 01-02 write to
STAGE2 = OUT / "stage2_clean_join"
STAGE3 = OUT / "stage3_model_table"
STAGE4 = OUT / "stage4_supervised"
STAGE5 = OUT / "stage5_unsupervised"
STAGE6 = OUT / "stage6_pnnl"
OUTPUTS = OUT / "model_outputs"
FIGURES = OUT / "figures"

for _d in (STAGE3, STAGE4, STAGE5, STAGE6, OUTPUTS, FIGURES):
    _d.mkdir(parents=True, exist_ok=True)

# ---- infrastructure features (CERF-DC county statistics) ---------------------------------
# Supervised set (report Appendix A). Water cooling is left out because it equals
# 1 - mechanical cooling; the market-location raster is never used (zero everywhere, leaks the label).

INFRA_GROUPS = {
    "Electricity cost": ["commercial_electricity_rates_dollar_per_kwh_mean",
                         "industrial_electricity_rates_dollar_per_kwh_mean"],
    "Grid access and suitability": ["distance_to_substation_mean", "distance_to_substation_min",
                                    "composite_siting_suitability_mean", "composite_siting_suitability_max"],
    "Land and taxes": ["land_value_dollar_per_sqft_mean", "real_property_tax_rate_mean",
                       "personal_property_tax_rate_mean", "sales_tax_rate_mean"],
    "Cooling": ["mechanical_cooling_fraction_mean"]}

INFRA = [f for g in INFRA_GROUPS.values() for f in g]

# Clustering set used in notebook 03 (11 features, standardized).
CLUSTER_FEATURES = [
    "commercial_electricity_rates_dollar_per_kwh_mean", "industrial_electricity_rates_dollar_per_kwh_mean",
    "composite_siting_suitability_mean", "distance_to_substation_mean", "distance_to_substation_min",
    "land_value_dollar_per_sqft_mean", "mechanical_cooling_fraction_mean", "personal_property_tax_rate_mean",
    "real_property_tax_rate_mean", "sales_tax_rate_mean", "water_cooling_fraction_mean"]

ELECTRICITY = INFRA_GROUPS["Electricity cost"]
LOG_FEATURES = ["land_value_dollar_per_sqft_mean", "distance_to_substation_mean", "distance_to_substation_min"]

# ---- geography control and policy features (built in notebook 05) ---------------------------
DIVISIONS = ["New England", "Middle Atlantic", "East North Central", "West North Central", "South Atlantic",
             "East South Central", "West South Central", "Mountain", "Pacific"]

GEO = [f"div_{d.lower().replace(' ', '_')}" for d in DIVISIONS]

POLICY_GROUPS = {
    "Attention and follow-through": ["pol_bills_log", "pol_enacted_log", "pol_pass_rate"],
    "Timing": ["pol_first_year"],
    "Content": ["pol_share_regulatory", "pol_share_public", "pol_share_rights"],
    "Infrastructure bills": ["pol_infra_bills", "pol_infra_enacted"]}

POLICY = [f for g in POLICY_GROUPS.values() for f in g]

FEATURE_SETS = {
    "Infrastructure": INFRA,
    "+ Geography": INFRA + GEO,
    "+ AI policy": INFRA + GEO + POLICY}

TARGET, GROUP = "has_data_center", "state_abbr"


class Prep(BaseEstimator, TransformerMixin):
    """Cap the electricity rates at the 99th percentile of the training fold, then log1p the skewed columns.

    Same handling as the clustering notebook (03): the electricity rasters hold impossible values
    (up to $215/kWh). The cap is learned inside each training fold, so no test county shapes it.
    `cap=None` leaves the raw values in place for the sensitivity analysis.
    """

    def __init__(self, columns, cap=0.99, cap_columns=tuple(ELECTRICITY), log_columns=tuple(LOG_FEATURES)):
        self.columns, self.cap, self.cap_columns, self.log_columns = columns, cap, cap_columns, log_columns

    def fit(self, X, y=None):
        X = pd.DataFrame(X, columns=self.columns)
        self.capped_ = [c for c in self.cap_columns if c in X]
        self.hi_ = X[self.capped_].quantile(self.cap) if (self.cap and self.capped_) else None
        return self

    def transform(self, X):
        X = pd.DataFrame(X, columns=self.columns).astype(float).copy()
        if self.hi_ is not None:
            X[self.capped_] = X[self.capped_].clip(upper=self.hi_, axis=1)
        for c in self.log_columns:
            if c in X:
                X[c] = np.log1p(X[c])
        return X.values


def make_models(cols, spw, cap=0.99):
    """The four model families of notebook 06 with their grids: {family: (pipeline, grid)}."""
    from imblearn.ensemble import BalancedRandomForestClassifier
    from sklearn.linear_model import LogisticRegression
    from sklearn.neighbors import KNeighborsClassifier
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    from xgboost import XGBClassifier

    prep = lambda: Prep(cols, cap=cap)
    return {
        "Logistic regression": (Pipeline([("prep", prep()), ("sc", StandardScaler()),
                                          ("m", LogisticRegression(class_weight="balanced", max_iter=5000))]),
                                {"m__C": [0.01, 0.1, 1, 10]}),
        "k-nearest neighbors": (Pipeline([("prep", prep()), ("sc", StandardScaler()), ("m", KNeighborsClassifier())]),
                                {"m__n_neighbors": [10, 25, 50, 100], "m__weights": ["uniform", "distance"]}),
        "Balanced random forest": (Pipeline([("prep", prep()), ("m", BalancedRandomForestClassifier(
                                       n_estimators=300, sampling_strategy="all", replacement=True, bootstrap=False,
                                       random_state=0, n_jobs=1))]),
                                   {"m__max_depth": [6, 12, None], "m__min_samples_leaf": [1, 5]}),
        "XGBoost": (Pipeline([("prep", prep()), ("m", XGBClassifier(
                        tree_method="hist", subsample=0.8, colsample_bytree=0.8, scale_pos_weight=spw,
                        eval_metric="logloss", random_state=0, n_jobs=1))]),
                    {"m__max_depth": [2, 3, 5], "m__learning_rate": [0.03, 0.1], "m__n_estimators": [200, 500]})}


def fixed_model(family, cols, spw, params, cap=0.99):
    """One family with fixed hyperparameters (the modal choice from notebook 06)."""
    pipe = make_models(cols, spw, cap)[family][0]
    return pipe.set_params(**{f"m__{k}": v for k, v in params.items()})


def outer_splits(y, groups, seeds=(0, 1, 2), n_splits=5):
    """State-grouped, class-stratified folds: (seed, fold, train_idx, test_idx)."""
    for s in seeds:
        cv = StratifiedGroupKFold(n_splits=n_splits, shuffle=True, random_state=s)
        for k, (tr, te) in enumerate(cv.split(np.zeros(len(y)), y, groups)):
            yield s, k, tr, te


def load_model_table():
    return pd.read_csv(STAGE3 / "model_table.csv", dtype={"county_fips": str, "state_fips": str})


# ---- plain-language labels for figures and dashboard -------------------------------------
LABELS = {
    "commercial_electricity_rates_dollar_per_kwh_mean": "Commercial power price",
    "industrial_electricity_rates_dollar_per_kwh_mean": "Industrial power price",
    "distance_to_substation_mean": "Mean distance to a substation",
    "distance_to_substation_min": "Shortest distance to a substation",
    "composite_siting_suitability_mean": "Share of land suitable for siting",
    "composite_siting_suitability_max": "Any suitable land",
    "land_value_dollar_per_sqft_mean": "Land value",
    "real_property_tax_rate_mean": "Real property tax rate",
    "personal_property_tax_rate_mean": "Personal property tax rate",
    "sales_tax_rate_mean": "Sales tax rate",
    "mechanical_cooling_fraction_mean": "Mechanical cooling share",
    "water_cooling_fraction_mean": "Water cooling share",
    "pol_bills_log": "AI bills introduced (log)",
    "pol_enacted_log": "AI bills enacted (log)",
    "pol_pass_rate": "AI bill pass rate",
    "pol_first_year": "Year of first AI bill",
    "pol_share_regulatory": "Share of bills regulating private AI",
    "pol_share_public": "Share of bills on government AI use",
    "pol_share_rights": "Share of bills on rights and safety",
    "pol_infra_bills": "Energy, tax or data center AI bills (log)",
    "pol_infra_enacted": "Enacted an energy, tax or data center AI bill",
    **{g: "Division: " + d for g, d in zip(GEO, DIVISIONS)}}

FEATURE_GROUP = {**{f: g for g, fs in INFRA_GROUPS.items() for f in fs}, **{f: "Geography" for f in GEO},
                 **{f: "AI policy" for f in POLICY}}
