# Bay Area COVID-19 Dashboard
A repo for plotting and analyzing COVID-19 cases/deaths, with a focus on the San Francisco Bay Area. The data in this `README` are from the [John Hopkins University dataset](https://github.com/CSSEGISandData/COVID-19).

To install this package, clone this repo, from the top-level directory of the repo, type the following line into your command line

`pip install .`

The plots below are easily reproducible using the `covid.plot_bay_cases` method. There are also useful functions for reading in the COVID-19 data from both the JHU and [NY Times](https://github.com/nytimes/covid-19-data) datasets: `covid.get_data` loads the entire COVID-19 dataset from the specified source into a `Pandas.DataFrame`, and `covid.bay_data` loads the pertinent information for only the 9 Bay Area counties.

The Bay Area counties included are: Alameda, Contra Costa, Marin, Napa, San Francisco, San Mateo, Santa Clara, Solano, and Sonoma.

## Current Bay Area Numbers

Below, we show the total, cumulative cases (and deaths) over time for the combined 9 Bay Area counties.

![Bay Area Cumulative](.travis/current_bay_area_total_cases.png)

Below, we show the daily new cases (and deaths) over time for the combined 9 Bay Area counties.

![Bay Area Daily](.travis/current_bay_area_new_cases.png)

## County-by-County Numbers

Below, we show the total, cumulative cases (and deaths) over time for each of the 9 Bay Area counties.

![County Cumulative](.travis/current_county_total_cases.png)

Below, we show the daily new cases cases over time for each of the 9 Bay Area counties.

![County Daily](.travis/current_county_new_cases.png)

Below, we show the daily new cases cases over the last month for each of the 9 Bay Area counties.

![County Daily, Recent](.travis/current_county_new_cases_month.png)
