# -*- coding: utf-8 -*-

"""
Tests quality check routines.
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

# import test functions, which create artifical datasets
import solarobs.test_data as tf

# import qc functions
import solarobs.quality_checks.functions as qcf


class TestQC:
    def test_missing_data(self):

        hamburg = Location(lat=53.519267, lon=10.1023435, elev=1)

        data = tf.create_missing_data(
            location=hamburg,
            start="2000-04-02 00:00",
            end="2000-04-02 23:59",
            freq="1min",
            gaps=[
                ("ghi", "2000-04-02 00:00", "2000-04-02 00:00"),
                ("ghi", "2000-04-02 02:42", "2000-04-02 03:13"),
                ("dni", "2000-04-02 02:52", "2000-04-02 03:42"),
                ("dni", "2000-04-02 12:00", "2000-04-02 12:00"),
                ("dni", "2000-04-02 20:31", "2000-04-02 20:33"),
            ],
        )

        flagged_data = qcf.flag_missing_data(data)

        assert flagged_data.loc["2000-04-02 00:00", "ghi_flag_missing"]
        assert not np.isnan(flagged_data.loc["2000-04-02 00:01", "ghi_flag_missing"])

        assert flagged_data.loc["2000-04-02 02:53", "dni_flag_missing"]
        assert not flagged_data.loc["2000-04-02 03:14", "ghi_flag_missing"]

        assert all(
            flagged_data.loc[
                "2000-04-02 20:31":"2000-04-02 20:33", "dni_flag_missing"
            ].values
        )

        assert flagged_data["ghi_flag_missing"].sum() == 33
        assert flagged_data["dni_flag_missing"].sum() == 55
        assert flagged_data["dhi_flag_missing"].sum() == 0
