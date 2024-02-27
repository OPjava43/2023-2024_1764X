# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       james                                                        #
# 	Created:      Wed Aug 24 2022                                              #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

def autonomous():
    count = 0
    brain.screen.clear_screen()
    while True:
        brain.screen.print_at("Auton.... %6d" %(count), x=10, y=40)
        count = count + 1
        wait(20, MSEC)

def usercontrol():
    count = 0
    brain.screen.clear_screen()
    while True:
        brain.screen.print_at("driver... %6d" %(count), x=10, y=40)
        count = count + 1
        wait(20, MSEC)

comp = Competition(usercontrol, autonomous)