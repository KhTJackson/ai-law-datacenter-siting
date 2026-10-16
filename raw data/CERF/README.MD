# Package Data for CERF-Data Centers, Version v1

**Citation:**

> Mongird, K. (2025). Package Data for CERF-Data Centers (Version v1) [Data set]. MSD-LIVE Data Repository. https://doi.org/10.57931/3006807

**Overview**

This dataset contains sample input 100m raster files for running the CERF-DC python package (see https://github.com/IMMM-SFA/cerf_data_centers) at the state level across the CONUS. Due to data availability constraints, some of the items included are proxies or assumptions for siting factors used in the model. These are individually noted in the item descriptions and can be exchanged with more detailed information upon availability. 

**Data Descriptions**

The following raster files are included in the data download:

* state_siting_region.tif — State areas identified by state FIPS code
* composite_siting_suitability.tif — Value of 1 indicates suitable siting location, 0 otherwise. The following areas are excluded from siting:
    * Areas within 300m of a federal airport runway
    * Waterbodies
    * Areas with slope >16%
    * Areas susceptible to sinkholes
    * High coastal or inland flood risk areas
    * Local, state, and federal parks, leisure areas, and cemeteries
    * Areas >2 km away from electric substations
    * Areas >5 km away from a municipal water supplier service area
    * Areas >2 km away from high-speed fiber provider service territory
    * Protected Areas Database of the United States (PAD-US) areas
    * Railroads, major roadways, and minor roadways
    * Military areas and training grounds
    * Developed lands
    * Areas >0.8 km (0.5 miles) from developed lands
* land_value_dollar_per_sqft.tif — USD per square foot (sqft) derived from USDA $/acre land cost
* personal_property_tax_rate.tif — Personal property tax rate by state. Uses an assumed 0.0125 personal property tax rate for states with personal property tax, 0 for states without personal property tax.
* real_property_tax_rate.tif — Real personal property tax rate. Based on data available at the county level on residential real estate property tax rates.
* sales_tax_rate.tif — Sales tax rate by state.
* mechanical_cooling_fraction.tif — Fraction of year (values between 0 and 1, inclusive) that the data center would be cooled through mechanical processes based on local water stress and humidity levels.
* water_cooling_fraction.tif — Fraction of year (values between 0 and 1, inclusive) that the data center would be cooled through evaporative (water cooled) processes based on local water stress and humidity levels.
* distance_to_substation.tif — Distance to nearest substation in hundreds of meters (i.e., value of 1 equals a distance of 100m). Offshore areas have a value of 0.
* industrial_electricity_rates_dollar_per_kwh.tif — USD/kWh industrial electricity rates. Represents the average industrial rate across all utilities that operate within a given county. Values are derived from the US Utility Rate Database.
* commercial_electricity_rates_dollar_per_kwh.tif — USD/kWh commercial electricity rates. Represents the average commercial rate across all utilities that operate within a given county. Values are derived from the US Utility Rate Database.
* data_center_market_locations.tif — Grid cells with positive values represent the centroid of existing data center market clusters. The value of non-zero grid cells represents the number of data centers in the market cluster. All other grid cells have a value of 0.

**Geospatial Metadata**

CRS: Albers Equal Area Conic (ESRI:102003)

Extent: -2415585.0000000023283064,-1441981.2605773280374706 : 2384414.9999999976716936,1708018.7394226719625294

Dimensions: X: 48000 Y: 31500 Bands: 1

Origin: -2415585.0000000023283064,1708018.7394226719625294

Pixel Size: 100,-100

**Acknowledgment**

IM3 is a multi-institutional effort led by Pacific Northwest National Laboratory and supported by the U.S. Department of Energy's Office of Science as part of research in MultiSector Dynamics, Earth and Environmental Systems Modeling Program.

**License**

This data is made available under a CCBY4.0 License

**Disclaimer**

This material was prepared as an account of work sponsored by an agency of the United States Government. Neither the United States Government nor the United States Department of Energy, nor the Contractor, nor any or their employees, nor any jurisdiction or organization that has cooperated in the development of these materials, makes any warranty, express or implied, or assumes any legal liability or responsibility for the accuracy, completeness, or usefulness or any information, apparatus, product, software, or process disclosed, or represents that its use would not infringe privately owned rights. Reference herein to any specific commercial product, process, or service by trade name, trademark, manufacturer, or otherwise does not necessarily constitute or imply its endorsement, recommendation, or favoring by the United States Government or any agency thereof, or Battelle Memorial Institute. The views and opinions of authors expressed herein do not necessarily state or reflect those of the United States Government or any agency thereof.

PACIFIC NORTHWEST NATIONAL LABORATORYoperated byBATTELLEfor theUNITED STATES DEPARTMENT OF ENERGYunder Contract DE-AC05-76RL01830