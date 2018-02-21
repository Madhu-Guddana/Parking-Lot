--------------------------------------------
Copyright (c) 2018. All rights reserved.

Author: Madhu.Guddana@gmail.com
--------------------------------------------



Project: Automated Parking System v1.2
**************************************

Installation:
------------
  Do the following steps to install this project on a Linux/Mac machines.

  $ source sourceme.sh
      This will setup the python path and system path to run the
      parking_lot binary.

Build:
-----
  Run the following script to run the unittests and the pylint sanity
  checks.

  $ build
      This will run the unit tests and pylint on the System.

  Note: indentation need to be set to 2 in pylint configuration of the system.

Usage:
-----
  parking_lot --> For interactive mode
  parking_lot <input_file> --> For non interactive mode

Disclaimer:
----------
  3)  Color of the car is assumed to be all alphabets.
  4)  Register Number accepts all characters.
  5)  User is assumed to parked the vehicle in the allocated slot.
  6)  System need to be initiated using command
      create_parking_lot <parking_capacity> before any other operation
  7)  System can't be re-initiated, as it might lose existing data.
  8)  Upgrading capacity is not supported in this version.
  9)  Extra message are used than specified in the requirement document.
      So if parsing script is used to check system stability, it
      might have few divergent behaviour.



Compatibility:
-------------
   System is tested in following environment:
   1) Darwin Kernel Version 16.5.0, Python 2.7.10


Patch Specific Features:
-----------------------
   1) If 2 cars has same number plate, then it is illegal, So park operation
      fails with an alert, user is expected to report this to local police
      station.
   2) Slot in the building starts from 1 to n (previously it was 0 to n-1).
   3) Pylint config file is used to avoid sanity check failure due to
      different pylint configuration.
   4) Better display of build results.

