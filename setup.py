import os
import glob
import shutil
from setuptools import find_packages, Command

from numpy.distutils.core import Extension, setup



covid_data_paths_jhu = [
    "covid/data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_US.csv",
    "covid/data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_US.csv",
    "covid/data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv",
    "covid/data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv",
    "covid/data/jhu/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv",
]

covid_data_paths_nytimes = [
    "covid/data/nytimes/us-counties.csv",
]

class CleanCommand(Command):
    """Custom clean command to tidy up the project root."""
    CLEAN_FILES = './build ./dist ./*.pyc ./*.tgz ./*.egg-info'.split(' ')

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        here = os.path.dirname(os.path.abspath(__file__))

        for path_spec in self.CLEAN_FILES:
            # Make paths absolute and relative to this path
            abs_paths = glob.glob(os.path.normpath(os.path.join(here, path_spec)))
            for path in [str(p) for p in abs_paths]:
                if not path.startswith(here):
                    # Die if path in CLEAN_FILES is absolute + outside this directory
                    raise ValueError("%s is not a path inside %s" % (path, here))
                print('removing %s' % os.path.relpath(path))
                shutil.rmtree(path)

setup(
    name="covid", 
    version="0.1.0", 
    description="COVID-19 Plotting Package", 
    author="Samuel Watkins", 
    author_email="samwatkins@berkeley.edu", 
    url="https://github.com/slwatkins/covid", 
    packages=find_packages(), 
    zip_safe=False,
    cmdclass={
        'clean': CleanCommand,
    },
    data_files=[
        ('covid/data/jhu/csse_covid_19_data/csse_covid_19_time_series/', covid_data_paths_jhu),
        ('covid/data/nytimes/', covid_data_paths_nytimes),
    ],
)
