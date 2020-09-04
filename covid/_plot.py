import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import signal

from ._io import BAYAREA_COUNTIES, get_data, get_bay_data


__all__ = [
    'plot_bay_cases',
]


def _plot_cumulative_bay_cases(cases, deaths, lastnumdays, data_source):
    """
    Hidden function for plotting the cumulative cases and/or deaths for
    the total Bay Area.

    """

    bay_df = get_bay_data(data_source=data_source)

    if lastnumdays is not None:
        bay_cut = bay_df.index > pd.Timestamp(datetime.date.today() - datetime.timedelta(days=lastnumdays))
        bay_df = bay_df[bay_cut]

    if cases and deaths:
        ax = bay_df.plot(y='cases', marker='.', color='r')
        ax = bay_df.plot(y='deaths', marker='.', ax=ax, color='k')
    elif cases and not deaths:
        ax = bay_df.plot(y='cases', marker='.', color='r')
    else:
        ax = bay_df.plot(y='deaths', marker='.', color='k')

    labels = ["Cases", "Deaths"]
    for line, label in zip(ax.lines, labels):
        line.set_label(label)

    ax.legend(loc='upper left')
    ax.set_yscale('log')
    ax.set_ylim(0.8)
    ax.tick_params(which='both', direction='in', top=True, right=True)
    ax.grid(linestyle='dotted', color='k')
    if cases and deaths:
        ax.set_ylabel('Cumulative Cases/Deaths')
    elif cases and not deaths:
        ax.set_ylabel('Cumulative Cases')
    else:
        ax.set_ylabel('Cumulative Deaths')
    ax.set_xlabel('Date')
    ax.set_title("Total SF Bay Area")
    fig = plt.gcf()
    fig.tight_layout()

    return fig, ax

def _plot_new_bay_cases(cases, deaths, lastnumdays, data_source):
    """
    Hidden function for plotting the new daily cases and/or deaths for
    the total Bay Area.

    """

    bay_df = get_bay_data(data_source=data_source)

    if lastnumdays is not None:
        bay_cut = bay_df.index > pd.Timestamp(datetime.date.today() - datetime.timedelta(days=lastnumdays))
        bay_df = bay_df[bay_cut]

    if cases and deaths:
        ax = bay_df.plot(y='new_cases', marker='', color='r', alpha=0.3)
        ax = bay_df.plot(y='new_cases_filt', marker='', ax=ax, color='r')
        ax = bay_df.plot(y='new_deaths', marker='', ax=ax, color='k', alpha=0.3)
        ax = bay_df.plot(y='new_deaths_filt', marker='', ax=ax, color='k')
        labels = [None, "Cases", None,  "Deaths"]
    elif cases and not deaths:
        ax = bay_df.plot(y='new_cases', marker='', color='r', alpha=0.3)
        ax = bay_df.plot(y='new_cases_filt', marker='', ax=ax, color='r')
        labels = [None, "Cases"]
    else:
        ax = bay_df.plot(y='new_deaths', marker='', color='k', alpha=0.3)
        ax = bay_df.plot(y='new_deaths_filt', marker='', ax=ax, color='k')
        labels = [None,  "Deaths"]

    for line, label in zip(ax.lines, labels):
        line.set_label(label)

    ax.legend(loc='upper left')
    ax.set_yscale('log')
    ax.set_ylim(0.8)
    ax.tick_params(which='both', direction='in', top=True, right=True)
    ax.grid(linestyle='dotted', color='k')
    if cases and deaths:
        ax.set_ylabel('New Cases/Deaths Per Day')
    elif cases and not deaths:
        ax.set_ylabel('New Cases Per Day')
    else:
        ax.set_ylabel('New Deaths Per Day')
    ax.set_xlabel('Date')
    ax.set_title("Total SF Bay Area")
    fig = plt.gcf()
    fig.tight_layout()

    return fig, ax

def _plot_cumulative_county_cases(cases, deaths, lastnumdays, data_source):
    """
    Hidden function for plotting the cumulative cases and/or deaths for
    the each county in the Bay Area.

    """

    df = get_data(data_source=data_source)

    fig, ax = plt.subplots(3, 3, sharey=True, sharex=True)

    for ii, county in enumerate(BAYAREA_COUNTIES):
        plotcut = df.county == county
        if lastnumdays is not None:
            plotcut = plotcut & (df.date > pd.Timestamp(datetime.date.today() - datetime.timedelta(days=lastnumdays)))

        if cases:
            ax[ii//3, np.mod(ii, 3)].plot(df[plotcut].date, df[plotcut].cases, color='r')

        if deaths:
            ax[ii//3, np.mod(ii, 3)].plot(df[plotcut].date, df[plotcut].deaths, color='k')

        ax[ii//3, np.mod(ii, 3)].set_title(county, fontsize=8, pad=2)
        ax[ii//3, np.mod(ii, 3)].tick_params(which='both', direction='in', top=True, right=True)
        ax[ii//3, np.mod(ii, 3)].grid(linestyle='dotted', color='k')
        ax[ii//3, np.mod(ii, 3)].tick_params(labelsize=8)

    ax[0, 0].set_yscale('log')
    ax[0, 0].set_ylim(0.8)
    if cases and deaths:
        ax[1, 0].set_ylabel('Cumulative Cases/Deaths')
    elif cases and not deaths:
        ax[1, 0].set_ylabel('Cumulative Cases')
    else:
        ax[1, 0].set_ylabel('Cumulative Deaths')
    fig.autofmt_xdate(rotation=90, ha='center')

    return fig, ax

def _plot_new_county_cases(cases, deaths, lastnumdays, data_source):
    """
    Hidden function for plotting the daily new cases and/or deaths for
    the each county in the Bay Area.

    """

    df = get_data(data_source=data_source)

    fig, ax = plt.subplots(3, 3, sharey=True, sharex=True)

    for ii, county in enumerate(BAYAREA_COUNTIES):
        filtercut = (df.county == county)
        cases_per_day = np.concatenate(([0], np.diff(df[filtercut].cases)))
        filtered_cases = signal.savgol_filter(cases_per_day, 15, 3)
        deaths_per_day = np.concatenate(([0], np.diff(df[filtercut].deaths)))
        filtered_deaths = signal.savgol_filter(deaths_per_day, 15, 3)

        if lastnumdays is not None:
            plotcut = df[filtercut].date > pd.Timestamp(datetime.date.today() - datetime.timedelta(days=lastnumdays))
        else:
            plotcut = np.ones(np.sum(filtercut), dtype=bool)

        if cases:
            ax[ii//3, np.mod(ii, 3)].plot(df[filtercut][plotcut].date, cases_per_day[plotcut], color='r', alpha=0.3)
            ax[ii//3, np.mod(ii, 3)].plot(df[filtercut][plotcut].date, filtered_cases[plotcut], color='r')
        if deaths:
            ax[ii//3, np.mod(ii, 3)].plot(df[filtercut][plotcut].date, deaths_per_day[plotcut], color='k', alpha=0.3)
            ax[ii//3, np.mod(ii, 3)].plot(df[filtercut][plotcut].date, filtered_deaths[plotcut], color='k')

        ax[ii//3, np.mod(ii, 3)].set_title(county, fontsize=8, pad=2)
        ax[ii//3, np.mod(ii, 3)].tick_params(which='both', direction='in', top=True, right=True)
        ax[ii//3, np.mod(ii, 3)].grid(linestyle='dotted', color='k')
        ax[ii//3, np.mod(ii, 3)].tick_params(labelsize=8)

    ax[0, 0].set_ylim(0)
    if cases and deaths:
        ax[1, 0].set_ylabel('New Cases/Deaths Per Day')
    elif cases and not deaths:
        ax[1, 0].set_ylabel('New Cases Per Day')
    else:
        ax[1, 0].set_ylabel('New Deaths Per Day')
    fig.autofmt_xdate(rotation=90, ha='center')

    return fig, ax

def plot_bay_cases(cumulative=True, cases=True, deaths=False, groupcounties=True, lastnumdays=None, data_source='jhu'):
    """
    Function for plotting various pertinent plots for COVID-19
    cases/deaths in the San Francisco Bay Area.

    Parameters
    ----------
    cumulative : bool, optional
        Boolean value for plotting the cumulative cases/deaths (True)
        or the daily new cases/deaths (False). Default is True.
    cases : bool, optional
        Boolean value for whether or not to plot the confirmed cases
        data. Default is True.
    deaths : bool, optional
        Boolean value for whether or not to plot the confirmed deaths
        data. Default is False.
    groupcounties : bool, optional
        Boolean value for grouping all Bay Area counties into one plot
        (True) or plotting each county individually in a grid of
        subplots (False). Default is True.
    lastnumdays : int, NoneType, optional
        Option to plot only the specified last number of days. If set
        to None, then the full date range is plotted.
    data_source : str, optional
        The source to use for the COVID-19 data. Can be either "jhu"
        for the John Hopkins University dataset or "nytimes" for the NY
        Times dataset.

    Returns
    -------
    fig : matplotlib.Figure
        The figure object for the created plot.
    ax : matplotlib.Axes, list of matplotlib.Axes
        The Axes object (or a list of Axes objects) for the created
        plot.

    """

    if cumulative and groupcounties:
        fig, ax = _plot_cumulative_bay_cases(cases, deaths, lastnumdays, data_source)
    elif not cumulative and groupcounties:
        fig, ax = _plot_new_bay_cases(cases, deaths, lastnumdays, data_source)
    elif cumulative and not groupcounties:
        fig, ax = _plot_cumulative_county_cases(cases, deaths, lastnumdays, data_source)
    elif not cumulative and not groupcounties:
        fig, ax = _plot_new_county_cases(cases, deaths, lastnumdays, data_source)

    return fig, ax
