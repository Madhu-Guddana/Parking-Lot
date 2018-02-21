"""
Copyright (c) 2018. All rights reserved.

Author: Madhu.Guddana@gmail.com

This package provides various classes that will be used to represent
information regarding vehicle.
"""

class Vehicle(object):
  """Class which upon instantiate represents Vehicle.
  """

  def __init__(self, number, color):
    """The initializer of the vehicle object.

    Args:
      number (str): Registration number of the vehicle.
      color (Color.int): Color constant defined in Color.
    """
    assert color.isalpha(), "Invalid color input, must be alphaphets only"
    self.__number = number.upper()
    self.__color = color.upper()

  def __str__(self):
    """ String representation of the vehicle, that provides information like
    registration number and color of the vehicle object.

    Returns:
      None

    """
    return "Registration number = {number} and color = {color}".format(
      number=self.__number, color=self.__color)

  @property
  def color(self):
    """Property the provide read access to private member __color"""
    return self.__color

  @property
  def number(self):
    """Property the provide read access to private member __number"""
    return self.__number


