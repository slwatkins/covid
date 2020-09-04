import numpy as np
import pandas as pd
from scipy import signal
import os

__all__ = [
    'get_data',
    'get_bay_data',
]

FILE_PATH = os.path.dirname(os.path.realpath(__file__))
BAYAREA_COUNTIES = [
    'Alameda',
    'Contra Costa',
    'Marin',
    'Napa',
    'San Francisco',
    'San Mateo',
    'Santa Clara',
    'Solano',
    'Sonoma',
]

def _read_jhu_csv(path, datatype, us_or_global):
    """
    Function for reading an individual JHU data file and returning
    a Pandas DataFrame with desired format.

    """

    jhu_csv = pd.read_csv(path)

    if us_or_global == "us":

        jhu_us_remove_columns = ['UID', 'iso2', 'iso3', 'code3', 'Combined_Key']
        if 'Population' in jhu_csv.keys():
            jhu_us_remove_columns.append('Population')
        jhu_csv.drop(columns=jhu_us_remove_columns, inplace=True)

        jhu_us_rename_columns = {
            "FIPS": "fips",
            "Admin2": "county",
            "Province_State": "state",
            "Country_Region": "country",
            "Lat": "lat",
            "Long_": "long",
        }

        jhu_csv.rename(columns=jhu_us_rename_columns, inplace=True)

        timestamp = {d: pd.to_datetime(
            d,
            errors='ignore',
        ) for d in jhu_csv.keys() if d not in jhu_us_rename_columns.values()}

        jhu_csv.rename(columns=timestamp, inplace=True)

        jhu_us_keep_columns = ['fips', 'county', 'state', 'country', 'lat', 'long']

        if datatype == 'confirmed':
            jhu_csv = pd.melt(
                jhu_csv, id_vars=jhu_us_keep_columns, var_name='date', value_name='cases',
            )
        elif datatype == 'deaths':
            jhu_csv = pd.melt(
                jhu_csv, id_vars=jhu_us_keep_columns, var_name='date', value_name='deaths',
            )

    elif us_or_global == 'global':
        jhu_global_rename_columns = {
            "Province/State": "state",
            "Country/Region": "country",
            "Lat": "lat",
            "Long": "long",
        }

        jhu_csv.rename(columns=jhu_global_rename_columns, inplace=True)

        timestamp = {
            d: pd.to_datetime(
                d, errors='ignore',
            ) for d in jhu_csv.keys() if d not in jhu_global_rename_columns.values()
        }

        jhu_csv.rename(columns=timestamp, inplace=True)
        jhu_global_keep_columns = ['state', 'country', 'lat', 'long']
        if datatype == 'confirmed':
            jhu_csv = pd.melt(
                jhu_csv, id_vars=jhu_global_keep_columns, var_name='date', value_name='cases',
            )
        elif datatype == 'deaths':
            jhu_csv = pd.melt(
                jhu_csv, id_vars=jhu_global_keep_columns, var_name='date', value_name='deaths',
            )
        elif datatype == 'recovered':
            jhu_csv = pd.melt(
                jhu_csv, id_vars=jhu_global_keep_columns, var_name='date', value_name='recovered',
            )

    return jhu_csv

def _merge_jhu_data(us_or_global):
    """
    Function for merging the JHU data to combine different source
    files.

    """

    if us_or_global == "us":
        jhu_paths = [
            f"{FILE_PATH}/data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv",
            f"{FILE_PATH}/data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv",
        ]

        jhu_datainfo = [p.lower().split('.')[-2].split('_')[-2:] for p in jhu_paths]

        jhu_data = pd.merge(
            *[_read_jhu_csv(
                p,
                *datainfo,
            ) for p, datainfo in zip(
                jhu_paths,
                jhu_datainfo,
            )],
        )
    elif us_or_global == 'global':
        jhu_paths = [
            f"{FILE_PATH}/data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
            f"{FILE_PATH}/data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
            f"{FILE_PATH}/data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
        ]

        jhu_datainfo = [p.lower().split('.')[-2].split('_')[-2:] for p in jhu_paths]

        for ii in range(len(jhu_paths)):
            if ii == 0:
                jhu_data = _read_jhu_csv(jhu_paths[ii], *jhu_datainfo[ii])
            elif ii > 0:
                jhu_data = pd.merge(
                    jhu_data,
                    _read_jhu_csv(jhu_paths[ii], *jhu_datainfo[ii]),
                )
    
    return jhu_data

def _get_jhu_data():
    """
    Function for reading all JHU data and returning a Pandas DataFrame.

    """

    jhu_data = pd.concat(
        (_merge_jhu_data('us'), _merge_jhu_data('global')), ignore_index=True, sort=False,
    )

    return jhu_data

def _get_nytimes_data():
    """
    Function for reading the NYTimes data and returning a Pandas
    DataFrame.

    """

    nytimes_data = pd.read_csv(f"{FILE_PATH}/data/nytimes/us-counties.csv")
    nytimes_data['date'] = pd.to_datetime(nytimes_data['date'])

    return nytimes_data

def get_data(data_source='jhu'):
    """
    Function for parsing and returning a dataset on COVID-19.

    Parameters
    ----------
    data_source : str, optional
        The source to use for the COVID-19 data. Can be either "jhu" for the
        John Hopkins University dataset or "nytimes" for the NY Times dataset.
        See Notes for more information on these datasets.

    Returns
    -------
    df_data : Pandas.DataFrame
        A DataFrame containing all the relevant information from the specified
        `data_source` on COVID-19.

    Notes
    -----
    The John Hopkins University dataset can be found here:
        - https://github.com/CSSEGISandData/COVID-19

    The NY Times dataset can be found here:
        - https://github.com/nytimes/covid-19-data

    """

    if data_source == "jhu":
        return _get_jhu_data()
    elif data_source == "nytimes":
        return _get_nytimes_data()

    raise ValueError("data_source should be either 'jhu' or 'nytimes'.")


def get_bay_data(data_source='jhu'):
    """
    Function for parsing and returning a dataset on COVID-19 for the
    entire San Francisco Bay Area. See Notes for the included counties.

    Parameters
    ----------
    data_source : str, optional
        The source to use for the COVID-19 data. Can be either "jhu"
        for the John Hopkins University dataset or "nytimes" for the NY
        Times dataset. See Notes for more information on these
        datasets.

    Returns
    -------
    bay_df : Pandas.DataFrame
        A DataFrame containing all the relevant information from the
        specified `data_source` on COVID-19 for the total Bay Area.

    Notes
    -----
    The Bay Area counties included are:
        Alameda, Contra Costa, Marin, Napa, San Francisco, San Mateo,
        Santa Clara, Solano, and Sonoma.

    The John Hopkins University dataset can be found here:
        - https://github.com/CSSEGISandData/COVID-19

    The NY Times dataset can be found here:
        - https://github.com/nytimes/covid-19-data

    """

    df = get_data(data_source=data_source)

    bayarea_cut = np.logical_or.reduce([df.county == bac for bac in BAYAREA_COUNTIES])
    bay_df = df[bayarea_cut].groupby('date').sum()
    bay_df.drop(['fips'], axis='columns', inplace=True)
    if data_source=='jhu':
        bay_df.drop(['lat', 'long'], axis='columns', inplace=True)

    bay_df['new_cases'] = np.concatenate(([0], np.diff(bay_df.cases)))
    bay_df['new_deaths'] = np.concatenate(([0], np.diff(bay_df.deaths)))
    bay_df['new_cases_filt'] = signal.savgol_filter(bay_df.new_cases, 15, 3)
    bay_df['new_deaths_filt'] = signal.savgol_filter(bay_df.new_deaths, 15, 3)

    return bay_df
