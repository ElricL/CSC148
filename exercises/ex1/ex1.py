"""CSC148 Exercise 1: Basic Object-Oriented Programming

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto

=== Module description ===
This module contains starter code for Exercise 1.
It contains two classes that work together:
- SuperDuperManager, which manages all the cars in the system
- Car, a class which represents a single car in the system

Your task is to design and implement the Car class, and then modify the
SuperDuperManager methods so that they make proper use of the Car class.

You may not modify the public interface of any of the SuperDuperManager methods.
We have marked the parts of the code you should change with TODOs, which you
should remove once you've completed them.

Notes:
  1. We'll talk more about private attributes on Friday's class.
     For now, treat them the same as any other instance attribute.
  2. You'll notice we use a trailing underscore for the parameter name
     "id_" in a few places. It is used to avoid conflicts with Python
     keywords. Here we want to have a parameter named "id", but that is
     already the name of a built-in function. So we call it "id_" instead.
"""
from typing import Dict, Optional, Tuple


class SuperDuperManager:
    """A class that keeps track of all cars in the Super Duper system.
    """
    # === Private Attributes ===
    # _cars:
    #   A map of unique string identifiers to the corresponding Car.
    #   For example, _cars['car1'] would be a Car object corresponding to
    #   the id 'car1'.
    _cars: Dict[str, 'Car']

    def __init__(self) -> None:
        """Initialize a new SuperDuperManager.

        There are no cars in the system when first created.
        """
        self._cars = {}

    def add_car(self, id_: str, fuel: int) -> None:
        """Add a new car to the system.

        The new car is identified by the string <id_>, and has initial amount
        of fuel <fuel>.

        Do nothing if there is already a car with the given id.

        Precondition: fuel >= 0.
        """
        # Check to make sure the identifier isn't already used.
        if id_ not in self._cars:
            self._cars[id_] = Car(fuel)

    def move_car(self, id_: str, new_x: int, new_y: int) -> None:
        """Move the car with the given id.

        The car called <id_> should be moved to position (<new_x>, <new_y>).
        Do nothing if there is no car with the given id,
        or if the corresponding car does not have enough fuel.
        """
        if id_ in self._cars:
            self._cars[id_].move(new_x, new_y)

    def get_car_position(self, id_: str) -> Optional[Tuple[int, int]]:
        """Return the position of the car with the given id.

        Return a tuple of the (x, y) position of the car with id <id_>.
        Return None if there is no car with the given id.
        """
        if id_ in self._cars:
            return self._cars[id_].x, self._cars[id_].y

    def get_car_fuel(self, id_: str) -> Optional[int]:
        """Return the amount of fuel of the car with the given id.

        Return None if there is no car with the given id.
        """
        if id_ in self._cars:
            return self._cars[id_].fuel

    def dispatch(self, x: int, y: int) -> None:
        """Move a car to the given location.

        Choose a car to move based on the following criteria:
        (1) Only consider cars that *can* move to the location.
            (Ignore ones that don't have enough fuel.)
        (2) After (1), choose the car that would move the *least* distance to
            get to the location.
        (3) If there is a tie in (2), pick the car whose id comes first
            alphabetically. Use < and/or > to compare the strings.
        (4) If no cars can move to the given location, do nothing.
        """
        possible_cars = self._possible_cars(x, y)
        if len(possible_cars) > 0:
            min_distance = min(possible_cars)
            if len(possible_cars[min_distance]) > 1:
                min_id = ''
                for i in range(len(possible_cars[min_distance])):
                    if possible_cars[min_distance][i] < possible_cars[min_distance][i-1]:
                        min_id = possible_cars[min_distance][i]
            else:
                min_id = possible_cars[min_distance][0]
            self._cars[min_id].move(x, y)

    def _possible_cars(self, x: int, y: int) -> Dict[int, str]:
        '''Return a dictionary of cars that has enough fuel to go
        to new coordinate

        Each car would be categorized by amount of distance it would take
        to go to new coordinate from their current location
        '''
        possible_cars = {}
        for id_ in self._cars:
            car = self._cars[id_]
            distance = car.distance(x, y)
            if distance <= car.fuel:
                if distance not in possible_cars:
                    possible_cars[distance] = [id_]
                else:
                    possible_cars[distance].append(id_)
        return possible_cars


class Car:
    """A car in the Super system.

    === Public attributes ===
    x: the x-coordinate of this car's position
    y: the y-coordinate of this car's position
    fuel: the amount of fuel remaining this car has remaining

    === Representation invariants ===
    fuel >= 0
    """
    x: int
    y: int
    fuel: int

    def __init__(self, fuel: int) -> None:
        """Initialize a new Car with given amount of fuel

        The Car starts at position (0, 0)
        """
        self.fuel = fuel
        self.x = 0
        self.y = 0

    def move(self, new_x: int, new_y: int) -> None:
        """Move car to new coordinates if enough fuel

        Decrease fuel if car moves
        """
        units = self.distance(new_x, new_y)
        if units <= self.fuel and self.fuel:
            self.fuel -= units
            self.x = new_x
            self.y = new_y

    def distance(self, new_x: int, new_y: int) -> int:
        """Return the distance from car current position and new position
        """
        return abs(new_x - self.x) + abs(new_y - self.y)


if __name__ == '__main__':
    # Run python_ta to ensure this module passes all checks for
    # code inconsistencies and forbidden Python features.
    # Useful for debugging!
    import python_ta
    python_ta.check_all()
