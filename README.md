# AI Regulation and Data Center Siting

Do state AI laws affect where data centers get built? 

This project combines county-level siting factors (electricity prices, land values, taxes, cooling needs, distance to substations) with existing and projected data center locations and every state AI bill tracked by NCSL from 2019 to 2025. We use supervised models to test whether a state’s AI policy helps predict which counties have data centers, beyond infrastructure and geography. Clustering groups counties into siting archetypes, and we compare our predictions with PNNL’s projected sites. 

[Results Dashboard](https://chalseokorom.github.io/ai-law-datacenter-siting/).

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
