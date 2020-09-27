# -*- coding: utf-8 -*-

"""
This script handles the location object and features some useful methods.
"""
# imports from standard library


# third-party imports
import pandas as pd
import pvlib as pv


class Location:
    def __init__(self, lat: float, lon: float, elev: float) -> None:
        self.lat = lat
        self.lon = lon
        # elevation in meters
        self.elev = elev

    def __repr__(self):
        return f"<{self.__class__.__name__} object {self.__dict__}>"

    def get_clear_sky(self, start: str, end: str, freq: str) -> pd.DataFrame:
        """
        Returns clear sky data for this location between start and end date.
        start, end and freq and directly passed to the pd.date_range function,
        which is why the syntax and possible values are identical.
        """

        # create DatetimeIndex
        dt_index = pd.date_range(start=start, end=end, freq=freq)

        # sun position
        solar_position = pvlib.solarposition.get_solarposition(
            dt_index, self.lat, self.lon
        )

        # relative air mass
        air_mass_rel = pvlib.atmosphere.get_relative_airmass(
            solar_position["apparent_zenith"]
        )

        # estimate pressure
        pressure = pvlib.atmosphere.alt2pres(self.elev)

        # absolute air mass
        air_mass_abs = pvlib.atmosphere.get_absolute_airmass(air_mass_rel, pressure)

        # get linke turbidity for this location and times
        linke_turbidity = pvlib.clearsky.lookup_linke_turbidity(
            dt_index, self.lat, self.lon
        )

        # get extraterrestrial radiation (radiation above the atmosphere)
        dni_extra = pvlib.irradiance.get_extra_radiation(dt_index)

        # get clear sky values using ineichen estimation by pvlib
        data = clearsky.ineichen(
            solar_position["apparent_zenith"],
            air_mass_abs,
            linke_turbidity,
            self.elev,
            dni_extra,
        )

        # rename columns as clear sky values should always be indicated as such,
        # if we do not explicitely create artifical data sets
        data.rename(
            columns={
                "dni": "dni_clear",
                "ghi": "ghi_clear",
                "dhi": "dhi_clear",
            },
            inplace=True,
        )

        return data


if __name__ == "__main__":
    loc = Location(55.0, 10.0, 10.0)

    print(loc)