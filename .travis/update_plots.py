#!/usr/bin/env python3

import datetime
import matplotlib.pyplot as plt
import covid

jhu_data = covid.get_data()
ax = jhu_data[jhu_data.county=='Alameda'].plot('date', 'cases', marker='.', color='r')
ax = jhu_data[jhu_data.county=='Alameda'].plot('date', 'deaths', marker='.', ax=ax, color='k')

labels = ["Cases", "Deaths"]
for line, label in zip(ax.lines, labels):
    line.set_label(label)

ax.legend(loc='upper left')
ax.set_yscale('log')
ax.set_ylim(0.8)
ax.tick_params(which='both', direction='in', top=True, right=True)
ax.grid(linestyle='dotted', color='k')
ax.set_ylabel('Number of Confirmed Cases/Deaths')
ax.set_xlabel('Date')
ax.set_title(
    "Alameda County COVID-19 Stats\n"
    f"Source: JHU, Last Updated: {datetime.date.today().strftime(format='%Y-%m-%d')}"
)
fig = plt.gcf()
fig.savefig(".travis/current_alameda_cases.png", dpi=200)
