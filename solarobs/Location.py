
class Location:
    def __init__(self, lat: float, lon: float, elev: float) -> None:
        self.lat = lat
        self.lon = lon
        # elevation in meters
        self.elev = elev

    def __repr__(self):
        return f"<{self.__class__.__name__} object {self.__dict__}>"

if __name__ == "__main__":
    loc = Location(55., 10., 10.)

    print(loc)