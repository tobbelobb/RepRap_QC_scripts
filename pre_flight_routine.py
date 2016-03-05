#!/usr/bin/env python

# This script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Printrun.  If not, see <http://www.gnu.org/licenses/>.

# Interactive RepRap quality control script for D3D Workshop
# (C) Torbjørn Ludvigsen, 2016

# The plan:
#  * Make every step accessible to user at all times by presenting
#    them in an ipython interactive document.
#  * For all steps, present
#    - A video titled "This is supposed to happen"
#    - A button titled "Send command!"
#    - A button titled "It worked!"
#  * All quality control steps are manual, no automatic parsing of
#    firmware output takes place.
#  * When all itworked-buttons have been pushed, congratulate
#    the user with a nice looking picture.
#
## PREPARATIONS
#  Step 0:  Read this warning:
#           "Quality Control sometimes involves surprising printer behaviour.
#           Localize the power plug and be ready to pull it in case uncontrolled
#           movements or heating occurs."
#  Step 1:  Connect to printer
## DRY MOVEMENT CONTROL
#  Step 2:  Move X-axis 10 mm to the right
#  Step 3:  Move Y-axis 10 mm forwards
#  Step 4:  Move Z-axis 1 mm upwards
#  Step 5:  Test triggering, ensure untriggered enstops are really untriggered
#  Step 6:  Press and hold X-enstop, ensure firmware reacts to triggering
#  Step 7:  Press and hold Y-enstop, ensure firmware reacts to triggering
#  Step 8:  Press and hold Z-enstop, ensure firmware reacts to triggering
#  Step 9:  Home X-axis
#  Step 10: Home Y-axis
#  Step 11: Home Z-axis
## HEATED PRINTER CONTROL
#  Step 12: Read printer temperatures. Ensure within reasonable range (often between 15 and 30) degrees Celcius.
#  Step 13: Set print head temperature to 40 degrees Celcius
#  Step 14: Set print head temperature to 200 degrees Celcius
#  Step 15: Set print bed temperature to 50 degrees Celcius
#  Step 16: Home Z-axis again (auto bed level is temperature dependent)
#  Step 17: Extrude 5 mm of filament repeatedly until molten plastic emerges
#  Step 18: Print calibration cube

port = '/dev/ttyUSB0'  # Default serial port to connect to printer
baud = 115200          # Default baud for printer communication

try:
    from printdummy import printcore
except ImportError:
    from printcore import printcore

import time
#import getopt
import sys
#import os

def w(s):
    sys.stdout.write(s)
    sys.stdout.flush()


# This should be an array with one bool per quality control step,
# indicating if the step is successfully finished or not.
# Keeping track of this lets us handle dependencies while
# allowing concurrency.
Steps_completed = [False, False, False, False, False, False,
                   False, False, False, False, False, False,
                   False, False, False, False, False, False]

def step_completed(step_number)
  print_checkbox(step_number)
  Steps_completed[step_number] = True


# Steps could clearly be captured in separate functions.

## Step 0: Present warning
w("Quality Control sometimes involves surprising printer behaviour.")
w("Localize the power plug and be ready to pull it in case uncontrolled movements or heating occurs.")
# Present "Okay" button with callback argument 0
step_completed(0)
## End of Step 0
## Step 1: Connect to printer
p = None
try:
    if not os.path.exists(port):
        prompt_for_new_port(port);
    # Present drop down menus for port and baud here
    # On try-button1 click event do:
    w("Connecting to printer..")
    try:
        p = printcore(port, baud)
    except: # Detecting the type of error here would be _really_ nice.
        print 'Unable to connect. Try again with alternative ports and bauds or contact instructor.'
        raise
    while not p.online:
        time.sleep(1)
        w('.')
    print " Success! Connected!"
    step_completed(1)
    ## End of Step 1

    ## Step 2: Move X-axis 10 mm to the right at controlled speed
    # On try-button2 click event do:
      p.send_now('G1 X10 F500')
      # Present "Yes, print head moved 10 mm to the right"-button with callback step_completed(2)
    ## End of Step 2

    ## Step 3: Move Y-axis 10 mm to the right at controlled speed
    # On try-button2 click event do:
      p.send_now('G1 Y10 F500')
      # Present "Yes, print bed moved 10 mm away from end-stop"-button with callback step_completed(3)
    ## End of Step 3

    ## Step 4:  Move Z-axis 10 mm upwards
      p.send_now('G1 Z1 F100')
      # Present "Yes, print head moved 10 mm upwards"-button with callback step_completed(4)
    ## End of Step 4

    ## Step 5:  Test triggering, ensure untriggered enstops are really untriggered
      p.send_now('M119')
      # TODO: How to dump printer log directly to iPython?
      #while(not got log line)
      #  try to fetch log line
      w(p.log(p.logl)) #print log line?
    ## End of Step 5

    ## Step 6:  Press and hold X-enstop, ensure firmware reacts to triggering
    ## End of Step 6

except KeyboardInterrupt:
    pass

finally:
    if p: p.disconnect()
