"""
Copyright (c) 2018. All rights reserved.

Author: Madhu.Guddana@gmail.com

Package to provide Interface to Automated Parking System of a multi-storey
parking lot that can hold up to 'n' cars at any given point in time.
Each slot is given a number starting at 1 increasing with increasing distance
from the entry point in steps of one.
This package creates an automated ticketing system that allows the customers
to use the parking lot without human intervention.

"""
#pylint: disable = no-self-use

import functools
from cmd import Cmd

from tabulate import tabulate

from lib.utils import supress_exception, validate_input, ARRAY, INTEGER
from source.parking_system import ParkingSystem
from source.vehicle import Vehicle


def check_for_initialization(expected_to_initialize):
  """
  This method is meant to use as decorator, to check if system is
  initalized with the command create_parking_lot, before using various
  utility.
  """
  def outer_func(func):
    """Outer function of the decorator"""
    @functools.wraps(func)
    def inner_func(*args, **kwargs):
      """This method will check for attribute _Prompt__parking_object"""
      self = args[0]
      error_message = {
        True: "System is not initialized yet, kindly use the command" \
              "`create_parking_lot <capacity>` to initiate the system",
        False: "System can't be initiated again, this can be done only" \
               " once in the beggining"
      }
      is_initialized = hasattr(self, "_Prompt__parking_object")
      unexpected_opertion = bool(is_initialized != expected_to_initialize)

      if unexpected_opertion:
        print error_message[expected_to_initialize]
        return
      return func(*args, **kwargs)
    return inner_func
  return outer_func


class Prompt(Cmd):
  """
  Class that provides interfaces for various operation in parking system like
  park, leave, status and query.
  """
  intro = """
          Welcome to Automate Parking System.
          -----------------------------------
          > Use create_parking_lot <capacity> to start system
          > Use help to list commands
          > Type help <command> to know more about the command"""

  def do_quit(self, args):
    """Function: quit

    This function exit from the system gracefully.

    Usage:  quit

    Examples: quit

    Notes:
      1. This accepts no other arguments.

    Args:
      str: None

    """
    print (args)
    print ("Thank you for using Automated Parking System")
    return True

  @supress_exception
  @check_for_initialization(expected_to_initialize=True)
  def do_park(self, args):
    """
    Function: park

    This function provides free slot to park the vehicle.

    Usage:  park <vehicle_registration_number> <color>

    Examples: park   KA-01-HH-1234   White

    Notes:
      1. Registration number and Color should be entered in case sensitive.

    Args:
      str: Color of the car.
    """
    args = args.split()
    user_note = "Required inut <register_no> and <color>, type *help park* " \
                "for more details"
    assert validate_input(args, ARRAY, array_length=2), user_note

    number = args[0]
    user_note = "ALERT, Duplicate numbered Vehicle Found"
    assert not self.__parking_object.query(number=number), user_note
    color = args[1]
    user_note = "Value for color must be only alphaphets"
    assert color.isalpha(), user_note

    vehicle = Vehicle(*args)
    self.__parking_object.park(vehicle)

  @check_for_initialization(expected_to_initialize=True)
  def do_status(self, args):
    """
    Function: status

    This function provides status of the parking facility of the building.

    Usage:  status

    Examples: status

    Notes:
      1. This accepts no parametes.

    Args:
      None
    """

    if args:
      print ("status doesn't accept value, hence ignoring extra paramter:%s" %\
          args)
    self.__parking_object.status()

  def emptyline(self):
    """Overridng the pratent method Cmd.emptyline
    Called when an empty line is entered in response to the prompt.

    If this method is not overridden, it repeats the last nonempty command
    entered.
    """
    pass

  @supress_exception
  @check_for_initialization(expected_to_initialize=True)
  def do_slot_numbers_for_cars_with_colour(self, args):
    """Function: slot_numbers_for_cars_with_colour

    This function provides list of cars in the given color along with the
    parked location, if present in the parking slot of the building.

    Usage:  slot_numbers_for_cars_with_colour <color>

    Examples: slot_numbers_for_cars_with_colour   White

    Notes:
      1. Color should be entered in case sensitive.

    Args:
      str: Color of the car.
    """
    user_note = "Provide valid value for <color> to search, check help <cmd> " \
                "for more information"
    assert validate_input(args.split(), ARRAY, array_length=1), user_note
    color = args.split()[0]

    assert color.isalpha(), "Invalid Color input"
    slots = self.__parking_object.query(color=color)

    if not slots:
      print ("No Vehicle Found for the query")
      return

    print ("Vehicle Found in slots: %s" % slots.keys())

  @supress_exception
  @check_for_initialization(expected_to_initialize=True)
  def do_slot_number_for_registration_number(self, args):
    """
    Function: slot_number_for_registration_number

    This function gets you the location of the car with given registration
    number, if parked in the building's parkings slot.

    Usage:  slot_number_for_registration_number <registration_number>

    Examples: slot_number_for_registration_number   KA-01-HH-3141

    Notes:
      1. Registration Number should be entered in case sensitive.

    Args:
      str: Registration Number of the car.
    """
    user_note = "Provide valid registration number to search"
    assert validate_input(args.split(), ARRAY, array_length=1), user_note
    number = args.split()[0]
    slots = self.__parking_object.query(number=number)
    if not slots:
      print ("No Vehicle Found for the query")
      return

    print ("Vehicle Found in slots: %s" % slots.keys())

  @supress_exception
  @check_for_initialization(expected_to_initialize=True)
  def do_registration_numbers_for_cars_with_colour(self, args):
    """
    Function: registration_numbers_for_cars_with_colour

    This function gets you the registration numbers of all cars having the
    specified color.

    Usage:  registration_numbers_for_cars_with_colour <color>

    Examples: registration_numbers_for_cars_with_colour Black

    Notes:
      1. Color should be entered in case sensitive.

    Args:
      str: Color of the car.
    """

    user_note = "Provide proper value of color for search"
    assert validate_input(args.split(), ARRAY, array_length=1), user_note

    color = args.split()[0]
    assert color.isalpha(), user_note

    slots = self.__parking_object.query(color=color)

    if not slots:
      print ("No Vehicle Found for the query")
      return

    data = [(slot, vehicle.number, vehicle.color) for slot, vehicle in
            slots.items()]
    print tabulate(data, headers=["Slot No", "Registration No", "Color"],
                   tablefmt='grid')

  @supress_exception
  @check_for_initialization(expected_to_initialize=True)
  def do_leave(self, args):
    """
    Function: leave

    This function helps vehicle to exit the building.

    Usage:  leave <parking_slot_number>

    Examples: leave 4

    Notes:
      1. parking_slot_number must be non-negative integer.

    Args:
      int: Parking slot number, where vehicle was parked.

    """
    user_note = "Invalid input, provide valid slot number"
    assert validate_input(args.split(), ARRAY, array_length=1), user_note
    slot = args.split()[0]
    assert validate_input(
      slot, INTEGER, required_range=(1, self.__parking_object.capacity)), \
      user_note
    slot = int(slot)
    self.__parking_object.leave(slot)

  @supress_exception
  @check_for_initialization(expected_to_initialize=False)
  def do_create_parking_lot(self, capacity):
    """
    Function: create_parking_lot

    This must be the first command to execute, and can be called only once.
    This initiates the system with Capacity of the buliding to facilitate
    multiple car to park.

    Usage:  create_parking_lot <capacity>

    Examples: create_parking_lot 6

    Notes:
      1. capacity must be non-negative integer.

    Args:
      int: capacity to park multiple vehicle in the building.

    """
    assert validate_input(capacity, INTEGER, required_positive=True)

    self.__parking_object = ParkingSystem(capacity=int(capacity))
    print ("Created a parking lot with {capacity} slots".format(
      capacity=capacity))
