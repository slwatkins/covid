#!/usr/bin/env python3

import matplotlib.pyplot as plt
import covid

fig, ax = covid.plot_bay_cases(
    cumulative=True,
    cases=True,
    deaths=True,
    groupcounties=True,
    lastnumdays=None,
    data_source='jhu',
)
ax.set_title(
    "Bay Area COVID-19 Stats, Source: JHU"
)
fig.savefig(".github/current_bay_area_total_cases.png", dpi=200, bbox_inches='tight')

fig, ax = covid.plot_bay_cases(
    cumulative=False,
    cases=True,
    deaths=True,
    groupcounties=True,
    lastnumdays=None,
    data_source='jhu',
)
ax.set_title(
    "Bay Area COVID-19 Stats, Source: JHU"
)
fig.savefig(".github/current_bay_area_new_cases.png", dpi=200, bbox_inches='tight')


fig, ax = covid.plot_bay_cases(
    cumulative=True,
    cases=True,
    deaths=True,
    groupcounties=False,
    lastnumdays=None,
    data_source='jhu',
)
fig.savefig(".github/current_county_total_cases.png", dpi=200, bbox_inches='tight')

fig, ax = covid.plot_bay_cases(
    cumulative=False,
    cases=True,
    deaths=False,
    groupcounties=False,
    lastnumdays=None,
    data_source='jhu',
)

fig.savefig(".github/current_county_new_cases.png", dpi=200, bbox_inches='tight')

fig, ax = covid.plot_bay_cases(
    cumulative=False,
    cases=True,
    deaths=False,
    groupcounties=False,
    lastnumdays=31,
    data_source='jhu',
)

fig.savefig(".github/current_county_new_cases_month.png", dpi=200, bbox_inches='tight')
