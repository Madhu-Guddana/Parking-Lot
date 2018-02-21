"""
Copyright (c) 2018. All rights reserved.

Author: Madhu.Guddana@gmail.com
"""
#pylint: disable = broad-except
import functools

# Constants
INTEGER = 2
ARRAY = 5


def validate_input(input_variable, expected_type, **kwargs):
  """
  This is an utility to check if the parameter provided as per expected value.

  Args:
    input_variable (var): Any variable, which need to be tested against type
      and value.
    expected_type (int): Constant defined in this package
    kwargs (dict):.
      For ARRAY, array_length = <value>
      For INTEGER, required_positive = True, to check for positive integer.
                   required_range = (low, high), where low and high are
                   inclusive, to check integer range.
      Note: required_positive will be given priority over required_range.

  Returns:
    bool: True if type and value is as per expected, False otherwise.

  """

  def is_integer_range(variable, required_range=None, required_positive=False):
    """An internal method that will check if variable is interger within
    expected range

    Args:
      variable(var): Variable to be checked against.
      required_range(tuple, optional): tuple with 2 values, inclusively
        defining upper and lower limit.
        default: None, will not be check for range.
      required_positive(bool, optional): If set to true, will be check for
        positive integer, and required_range will be ignored.
        default: False
    Returns:
      bool: True if variable is as per expected, False otehrwise.
    """
    try:
      variable = int(variable)
    except ValueError:
      return False
    if required_positive:
      return variable > 0
    if required_range:
      return required_range[0] <= variable <= required_range[1]

  def is_array_with_expected_length(variable, array_length):
    """
    Check for variable to be array with expected length.
    Args:
      variable (var): Variable to be of type array
      array_length (int): Expected length of array

    Returns:
      bool: True if variable is as per expected, False otehrwise.
    """
    return isinstance(variable, list) and len(variable) == array_length

  dictionary = {
    INTEGER: is_integer_range,
    ARRAY: is_array_with_expected_length
  }
  return dictionary[expected_type](input_variable, **kwargs)


def supress_exception(func):
  """
  This is a decorator, that will suprress any exception, with a message.
  This need to be used only in user interfaced script.

  Args:
    func (obj): Object of function, which need to supressed exception upon
    execution.

  Returns:
    (obj): Modified func object.

  """

  @functools.wraps(func)
  def inner_fucn(*args, **kwargs):
    """An inner function in decorator"""
    try:
      return func(*args, **kwargs)
    except Exception as exp_obj:
      print exp_obj.message
      print ("Operation failed, kindly refer help to understand usage of the " \
            "system")
  return inner_fucn

def graceful_terminate(*args):
  """
  This function exit from the system gracefully upon EOF in case of file
  input.

  """
  print (args)
  print ("Thank you for using Automated Parking System")
  return True

def usage_note():
  """This provides usage note of the system"""
  usage = ("""
        Documented commands (type help <topic>):
        ========================================
        create_parking_lot  quit                                        status
        help                registration_numbers_for_cars_with_colour
        leave               slot_number_for_registration_number
        park                slot_numbers_for_cars_with_colour     """)
  print (usage)
