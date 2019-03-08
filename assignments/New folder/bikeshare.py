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
        """Return the (long, lat) position of this object at the given time.
        """
        raise NotImplementedError


class Station(Drawable):
    """A Bixi station.

    === Public Attributes ===
    capacity:
        the total number of bikes the station can store
    location:
        the location of the station in long/lat coordinates
        **UPDATED**: make sure the first coordinate is the longitude,
        and the second coordinate is the latitude.
    name: str
        name of the station
    num_bikes: int
        current number of bikes at the station
    start_rides: int
        number of bikes that start at a station during the simulation
    end_rides: int
        number of bikes that end at a station when the simulation ends
    low_availability_time: int
        the total time a station spent in low availability during the simulation
    low_unoccupied_time: int
        the total time a station spent in low unoccupancy during the simulation
    unoccupied_spots: int
        the number of space available at a station for incoming rides
    === Representation Invariants ===
    - 0 <= num_bikes <= capacity
    """
    name: str
    location: Tuple[float, float]
    capacity: int
    num_bikes: int
    start_rides: int
    end_rides: int
    low_availability_time: int
    low_unoccupied_time: int
    unoccupied_spots: int

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
        self.start_rides = 0
        self.end_rides = 0
        self.low_availability_time = 0
        self.low_unoccupied_time = 0
        self.unoccupied_spots = self.capacity - self.num_bikes

    def get_position(self, time: datetime) -> Tuple[float, float]:
        """Return the (long, lat) position of this station for the given time.

        Note that the station's location does *not* change over time.
        The <time> parameter is included only because we should not change
        the header of an overridden method.
        """
        return self.location

    def low_availability(self) -> bool:
        """Return whether or not a station has low availability"""
        if self.num_bikes <= 5:
            return True
        return False

    def low_unoccupancy(self) -> bool:
        """Return whether or not a station has low unoccupacny"""
        if self.unoccupied_spots <= 5:
            return True
        return False


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
        """Return the (long, lat) position of this ride for the given time.

        A ride travels in a straight line between its start and end stations
        at a constant speed.
        """
        total_time = self.end_time - self.start_time
        time_in_progress = time - self.start_time

        long_distance = self.end.location[0] - self.start.location[0]
        lat_distance = self.end.location[1] - self.start.location[1]
        long_speed = long_distance / total_time.total_seconds()
        lat_speed = lat_distance / total_time.total_seconds()

        long_position = self.start.location[0] + long_speed * time_in_progress.\
            total_seconds()
        lat_position = self.start.location[1] + lat_speed * time_in_progress.\
            total_seconds()

        return long_position, lat_position


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-import-modules': [
            'doctest', 'python_ta', 'typing',
            'datetime'
        ],
        'max-attributes': 15
    })
