# -*- coding: utf-8 -*-

"""
This script creates artifical data sets used for testing purposes.
"""
# imports from standard library
import sys
from typing import Callable, List, Tuple
from pathlib import Path

# third-party imports
import pandas as pd
import pvlib as pv
import numpy as np
import matplotlib.pyplot as plt

# local imports
from solarobs.location import Location

##### FUNCTIONS #####

## Use these functions, if you want to run tests with test datasets as pandas dataframes.
## Otherwise use the ArtificalDataFileCreator to write those datasets to csv files.

# Note:
# They should be as simple as possible.
# Artifical data sets should not be longer than needed, in general 1 day.


def create_missing_data(
    location: Location,
    start: str,
    end: str,
    freq: str,
    gaps: List[Tuple[str, str, str]],
) -> pd.DataFrame:
    """
    Create a dataset with missing values in between.
    """
    # we use constant radiation values as a reference and set values within
    # the gaps defined to nan
    data = pd.DataFrame(
        index=pd.date_range(start=start, end=end, freq=freq),
        columns=["ghi", "dni", "dhi"],
    )
    data.loc[:, :] = 42

    # set gaps to nan (=missing values)
    for gap in gaps:
        param, start_gap, end_gap = gap

        data.loc[start_gap:end_gap, param] = np.nan

    return data


##### DATA CREATOR CLASS #####

## Use this class to create artifical datasets that you want to save as csv.
## Otherwise directly call the functions above to get a pandas dataframe to directly work with.
class ArtificalDataFileCreator:
    def __init__(self, base_path):
        self.base_path = base_path

    def create_data(
        self, data_name: str, location: Location, data_function: Callable, kwargs: dict
    ):
        output_path = self.get_output_path(data_name)

        with open(output_path, "w") as fout:
            dataframe = data_function(location, **kwargs)

            dataframe.to_csv(fout, sep=",", na_rep="NaN", index_label="datetime")

    def get_output_path(self, data_name):
        return self.base_path / Path(f"{data_name}.csv")


##### RUN #####

if __name__ == "__main__":
    # init adc and set base bath where csv files are saved to
    adc = ArtificalDataFileCreator("data/artificial_data/")

    hamburg = Location(lat=53.519267, lon=10.1023435, elev=1)

    adc.create_data(
        data_name="missing_data",
        location=hamburg,
        data_function=create_missing_data,
        kwargs={
            "start": "2000-04-02 00:00",
            "end": "2000-04-02 23:59",
            "freq": "1min",
            "gaps": [
                ("ghi", "2000-04-02 00:00", "2000-04-02 00:00"),
                ("ghi", "2000-04-02 02:42", "2000-04-02 03:13"),
                ("dni", "2000-04-02 02:52", "2000-04-02 03:42"),
                ("dni", "2000-04-02 12:00", "2000-04-02 12:00"),
                ("dhi", "2000-04-02 20:31", "2000-04-02 20:33"),
            ],
        },
    )