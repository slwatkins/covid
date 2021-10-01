#!/usr/bin/env python3

import datetime
import yaml

date = {'date': f"{datetime.date.today().strftime(format='%Y-%m-%d')}"}

with open('date_last_updated.yml', 'w') as f:
    yaml.dump(date, f, default_flow_style=False)
