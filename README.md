# AI Regulation and Data Center Siting

Do state AI laws affect where data centers get built? 

This project combines county-level siting factors (electricity prices, land values, taxes, cooling needs, distance to substations) with existing and projected data center locations and every state AI bill tracked by NCSL from 2019 to 2025. We use supervised models to test whether a state’s AI policy helps predict which counties have data centers, beyond infrastructure and geography. Clustering groups counties into siting archetypes, and we compare our predictions with PNNL’s projected sites. 

[Launch Results Dashboard](https://chalseokorom.github.io/ai-law-datacenter-siting/).
[Report docx](https://docs.google.com/document/d/1fcJ7O-R34FJn4XA4aGvSHTTaM5ukwFxQ/edit?usp=sharing&ouid=112816011740944920138&rtpof=true&sd=true)

## Folders

- `scripts/`: the main notebooks, run in number order
- `data/cerf_siting/`: CERF siting rasters and all pipeline outputs (`output/`)
- `data/im3/`: IM3 data center atlas and growth projections
- `data/ncsl_ai/`: NCSL AI legislation: scraped pages, notebooks, bill tables
- `data/census/`: Census files, downloaded automatically by step 05

## How to run

The data-prep steps are slow, and their outputs are already saved in the repo, so you can start at step 05.

1. Clone the repo.
2. *Optional: rebuild the data from scratch.* This takes a long time. 
    - Run `git lfs pull` to download the CERF rasters
    - Run notebooks 01 and 02.
3. Run the notebooks in `scripts/` in order, 05 through 11.

Notebooks 05–11 need `scripts/pipeline_config.py`.

`03_*` and `04_*` in `scripts/` are older drafts and aren't part of the pipeline.

## Data sources
- [CERF-DC siting rasters](https://doi.org/10.57931/3006807) (MSD-LIVE)
- [IM3 Data Center Atlas and projections](https://im3.pnnl.gov/datacenter-atlas) (PNNL)
- [NCSL AI legislation database](https://www.ncsl.org/technology-and-communication/artificial-intelligence-2025-legislation), 2019–2025
- U.S. Census Bureau: [county population estimates](https://www2.census.gov/programs-surveys/popest/datasets/2020-2024/counties/totals/co-est2024-alldata.csv) and [county boundaries](https://www2.census.gov/geo/tiger/GENZ2024/shp/cb_2024_us_county_500k.zip)


### My Contributions

**Role: Data Engineering and Machine Learning**

Contributed to a collaborative University of Michigan Master of Applied Data Science project examining U.S. data center siting using geospatial data, infrastructure characteristics, and state AI policy.

Key contributions included:

- **Data Engineering:** Extracted and transformed CERF geospatial raster datasets into county-level tabular features.
- **Data Integration:** Cleaned and integrated multiple datasets using county FIPS identifiers.
- **Supervised Learning:** Developed and evaluated classification approaches to predict counties hosting data centers.
- **Unsupervised Learning:** Implemented K-means and Gaussian Mixture Model clustering, including PCA visualization and cluster evaluation.
- **Project Collaboration:** Contributed modeling notebooks, preprocessing workflows, and analytical documentation.

*This project was completed collaboratively. The full repository and Git history recognize contributions from the project team.*

**Original team repository:** https://github.com/chalseokorom/ai-law-datacenter-siting
