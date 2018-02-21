"""
Copyright (c) 2018. All rights reserved.

Author: Madhu.Guddana@gmail.com

Package to provide library for various operation of Automated Parking System.

"""

from tabulate import tabulate
from lib.utils import validate_input, INTEGER
from source.vehicle import Vehicle


class ParkingSystem(object):
  """
  Class that provides libraries for various interfaces like park, leave,
  status and query.
  """

  def __init__(self, capacity):
    """Intialization of the object to start the system.

    Args:
      capacity(int): Capacity of the building to allow parking of n number of
                     vehicles.
    """
    self.__capacity = capacity
    self.__slots = [None] * (capacity+1)

  @property
  def capacity(self):
    """
    This provide read access to capacity of the system.

    Returns:
      int: capacity of the system.

    """
    return self.__capacity

  def __search_slot(self):
    """
    This uses linear search to check for free slots.
    Linear search is best suited here, as we need to check for available
    slot that is closer to the gate.

    Returns:
      int: Free slot number that is nearer to the gate, if available. Else
      returns -1 indicating no free Slots available

    """
    for index, slot in enumerate(self.__slots):
      if index == 0:
        continue
      if slot is None:
        return index
    print ("Sorry, parking lot is full")
    return -1

  def park(self, vehicle):
    """A method to provide free parking lot in the building.

    Args:
      vehicle (Vehicle): Instance of class Vehicle, which is at the gate and
      need to be parked.

    Returns:
      None

    """

    assert isinstance(vehicle, Vehicle), "Need Vehicle object, found :%s" % \
                                         type(vehicle)
    available_slot = self.__search_slot()
    if available_slot == -1:
      return
    print ("Allocated   slot   number: %d" % available_slot)
    self.__slots[available_slot] = vehicle

  def leave(self, slot):
    """A method to update data base when a vehicle leaves.

    Args:
      slot (int): Slot number in which vehicle was parked.

    Returns:
      None
    """

    assert validate_input(slot, INTEGER, required_range=(1, self.__capacity)),\
      "Out of range slot mentioned"
    vehicle = self.__slots[slot]

    if not vehicle:
      print ("%s was free, invalid request" % slot)
      return

    self.__slots[slot] = None
    print ("Vehicle: %s left the building, slot:%s is free now" % (vehicle,
                                                                   slot))

  def query(self, number="", color=""):
    """
    An interface to query the system for vehicle that is parked inside the
    building, based on its color and number.

    Args:
      number (str): Registration number of the Vehicle
        defaults: ""
      color (int): Code for color, defined in enumeration Color
        defaults: ""

    Returns:
      list: List of vehcile resulted in the query.

    """
    if color != "":
      assert color.isalpha(), "Invalid color input, must be alphaphets only"
    if not (number or color):
      print ("Neither Color nor Number is provided")
      return {}

    if number and color:
      print ("Both number and color is provided, only Number will be taken "
             "for consideration")

    attribute = "number" if number else "color"
    value = number if number else color
    value = value.upper()
    resulted_slot = {slot: vehicle for slot, vehicle in enumerate(
      self.__slots) if vehicle and getattr(vehicle, attribute) == value}

    return resulted_slot

  def status(self):
    """This display the status of parking system, that includes information
    of the vehicles parked in slots and Available slots.

    Returns:
      None

    """
    data = []

    for slot, vehicle in enumerate(self.__slots):
      if slot == 0:
        continue
      if vehicle:
        data.append((slot, vehicle.number, vehicle.color))
      else:
        data.append((slot, "", ""))
    print tabulate(data, headers=["Slot No", "Registration No", "Color"],
                   tablefmt='grid')


