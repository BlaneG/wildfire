# Canadian wildfire statistics

Wildfire is the dominant stand replacing disturbance in many forest ecosystems. This repository develops wildfire probability estimates by ecoregion using 33 years of historical wildfire statistics from 1986-2019.

![cdf-sample](figures/cdf-ecoregions.png)

Wildfire probability estimates show the likelihood of experiencing a wildfire on a given land area in years from the present and the cumulative probability that a land area will be disturbed by wildfire in the future.


## Approach
Wildfire statistics are available as polygons describing area of land disturbed by wildfire for each wildfire event. Annual land area disturbed by wildfire is computer and summed to generate a weighted uniform probability density function. The uniform probability density function is then fit to a sum of exponentials.

![approach](figures/overview.png)

As a validation check, we can see that the cumulative area disturbed by wildfire in ecoregion 65 was 20% over 33 years while it is estimated to be 17% in the cumulative disturbance probability plot.

![cdf-validation](figures/cdf-validation.png)

## Limitations
Wildfire is caused by fuel load, climate (moisture, temperature) and ignition sources (lightning, human sources). Temporal wildfire PDFs generated from historical statistics are biased estimates of the liklihood of wildfire for any particular land area when these PDFs are developed without controlling for these other variables that are causal determinants of wildfire. Developing wildfire PDFs by ecoregion helps to control for (historical) climate. Within each ecozone, these wildfire PDFs are likely to overestimate wildfire frequency for forests with recent disturbances (wildfire, harvesting) that have a reduced fuel load, and also to underestimate wildfire frequency for forest stands that have higher fuel loads like increased deadwood from mountain pine beetle.

Using geometries that are too narrowly defined may lead to biased estimates of wildfire risk if historical wildfire statistics in these small areas are not representative of actual wildfire risk.  Similarly, defining geometries too broadly can lead to locally biased estimates of wildfire risk by overestimating wildfire risk in some areas and understimating wildfire risk in other areas.

## Future work
For applying the wildfire PDFs to estimate loss of biomass from forests, the approach would benefit from normalizing to total forested area within a polygon rather than total land area as currently implemented.


## Installation
1. install python using anaconda
2. fork the repository
3. open the Anaconda prompt and run `conda env create -f environment.yml`
4. run `python scr\extract_data.py` to download the raw data
