# -*- coding: utf-8 -*-

"""
Tests quality check routines.
"""
import re
from typing import Optional

# third-party imports
import pandas as pd
import pvlib as pv
import numpy as np


def flag_missing_data(data: pd.DataFrame, vars: Optional[list] = None) -> pd.DataFrame:
    """
    Flag name/s which will be added as (a) column(s): "{var_name}_flag_missing"

    Flag columns will have a value of True, if the test was positive.

    If vars are not provided, it will check for missing values for all columns, which do not
    included the word "flag" within their names.

    If the flag column(s) already existed, the values will be overwritten.

    This is a simple check, if there are "np.nan" values. It is expected that values representing
    missing values are already transformed to "np.nan". If you read your file with pandas.read_csv
    this is quite likely. If you have non-standard nan-value-representations in your file as "-999"
    or "missing" you need to take a look at the "na_values" parameter you can pass to pandas.read_csv
    when reading the file.
    """

    # define columns we need to run the check on
    pattern_flag = re.compile(".*flag.*")

    if vars is None:
        columns = [col for col in data.columns if not pattern_flag.match(col)]
    else:
        columns = [col for col in vars if not pattern_flag.match(col)]

    # define new flag columns
    flag_columns = [f"{col}_flag_missing" for col in columns]

    # set default value of False (= test was negative)
    data.loc[:, flag_columns] = False

    # run qc check
    for col, flag in zip(columns, flag_columns):
        data.loc[data[col].isnull(), flag] = True

    return data