"""Assignment 1 - Bike-share objects

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Station and Ride classes, which store the data for the
objects in this simulation.

There is also an abstract Drawable class that is the superclass for both
Station and Ride. It enables the simulation to visualize these objects in
a graphical window.
"""
from datetime import datetime
from typing import Tuple


# Sprite files
STATION_SPRITE = 'stationsprite.png'
RIDE_SPRITE = 'bikesprite.png'


class Drawable:
    """A base class for objects that the graphical renderer can be drawn.

    === Public Attributes ===
    sprite:
        The filename of the image to be drawn for this object.
    """
    sprite: str

    def __init__(self, sprite_file: str) -> None:
        """Initialize this drawable object with the given sprite file.
        """
        self.sprite = sprite_file

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (lat, long) position of this object at the given time.
        """
        raise NotImplementedError


class Station(Drawable):
    """A Bixi station.

    === Public Attributes ===
    capacity:
        the total number of bikes the station can store
    location:
        the location of the station in lat/long coordinates
    name: str
        name of the station
    num_bikes: int
        current number of bikes at the station
    bikes_start: int
        number of bike rides that start at the station
    bikes_end: int
        number of bike rides that end at the station
    low_avail: float
        amount of seconds the station is in state of "low availability"
    low_unocc: float
        amount of seconds the station is in state of "low unoccupied"


    === Representation Invariants ===
    - 0 <= num_bikes <= capacity
    """
    name: str
    location: Tuple[float, float]
    capacity: int
    num_bikes: int
    bikes_start: int
    low_avail: float
    low_unocc: float

    def __init__(self, pos: Tuple[float, float], cap: int,
                 num_bikes: int, name: str) -> None:
        """Initialize a new station.

        Precondition: 0 <= num_bikes <= cap
        """
        Drawable.__init__(self, STATION_SPRITE)
        self.location = pos
        self.capacity = cap
        self.num_bikes = num_bikes
        self.name = name
        self.rides_start = 0
        self.rides_end = 0
        self.low_avail = 0.0
        self.low_unocc = 0.0

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (lat, long) position of this station for the given time.

        Note that the station's location does *not* change over time.
        The <time> parameter is included only because we should not change
        the header of an overridden method.
        """
        return self.location

    def is_full(self):
        """Return True iff the station has reached it's capacity
        """
        return self.num_bikes == self.capacity

    def is_low_availability(self):
        """Return True iff the Station has atmost five bikes available
        """
        return self.num_bikes <= 5

    def is_low_unoccupied(self):
        """Return True iff the station has atmost five unoccupied
        """
        return (self.capacity - self.num_bikes) <= 5


class Ride(Drawable):
    """A ride using a Bixi bike.

    === Attributes ===
    start:
        the station where this ride starts
    end:
        the station where this ride ends
    start_time:
        the time this ride starts
    end_time:
        the time this ride ends

    === Representation Invariants ===
    - start_time < end_time
    """
    start: Station
    end: Station
    start_time: datetime
    end_time: datetime

    def __init__(self, start: Station, end: Station,
                 times: Tuple[datetime, datetime]) -> None:
        """Initialize a ride object with the given start and end information.
        """
        Drawable.__init__(self, RIDE_SPRITE)
        self.start, self.end = start, end
        self.start_time, self.end_time = times[0], times[1]

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the position of this ride for the given time.

        A ride travels in a straight line between its start and end stations
        at a constant speed.
        """
        long1, lat1 = self.start.get_position(time)
        long2, lat2 = self.end.get_position(time)

        diff_time = (self.end_time - self.start_time).total_seconds()
        long_velocity = (long2 - long1) / diff_time
        lat_velocity = (lat2 - lat1) / diff_time

        cur_time = (time - self.start_time).total_seconds()
        cur_long = long1 + (long_velocity * cur_time)
        cur_lat = lat1 + (lat_velocity * cur_time)
        return cur_long, cur_lat


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'datetime'
        ],
        'max-attributes': 15
    })
