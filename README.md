# Modeling pipeline (steps 04–10)

Steps 01–03 build `processed/stage2_clean_join/master_county_clean.csv`. Steps 04–10 turn it into the
model table, the models, the report figures and dashboard files. Each step is an executed notebook (`.ipynb`) of the same name beside it. Shared paths, feature
lists, preprocessing and cross validation splits live in `pipeline_config.py`.

| Step | What it does | Writes | Time |
|---|---|---|---|
| `04_policy_features` | NCSL bills → nine state AI-policy features, adds Census division & population, builds county model table | `processed/stage3_model_table/` | seconds |
| `05_supervised` | Four model families × three feature sets, nested cross validation grouped by state (5 folds × 3 seeds), calibrated out of fold probabilities, paired policy test | `processed/stage4_supervised/` | ~9 min |
| `06_feature_insight` | SHAP, group ablation, state shuffle permutation test (100 shuffles), sensitivity checks, hyperparameter grid, failure analysis | `processed/stage4_supervised/` | ~4 min |
| `07_pnnl_benchmark` | Comparison with the PNNL IM3 projected sites (moderate growth, 50% market gravity) | `processed/stage6_pnnl/` | seconds |
| `08_unsupervised` | K-means archetypes (K = 3), Gaussian mixture sweep, assignment uncertainty, policy augmented clustering | `processed/stage5_unsupervised/` | seconds |
| `09_report_figures` | Report figures (Altair → PNG) | `processed/figures/` | under a minute |
| `10_dashboard_export` | Files for dashboard repo | `processed/model_outputs/` | seconds |

- Step 04 downloads two public Census files into `raw data/census/` on its first run (git-ignored).
- `fold_models.pkl` is git-ignored, so run step 05 before step 06.
- Tested with Python 3.13, pandas 3.0, numpy 2.5, scikit-learn 1.9, imbalanced-learn 0.14, xgboost 3.4,
  shap 0.54, scipy 1.18, geopandas 1.2, altair 6.3, vl-convert-python 1.9, jupytext 1.19.

## Dashboard

