# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       main.py                                                      #
# 	Author:       student                                                      #
# 	Created:      1/4/2024, 3:53:42 PM                                         #
# 	Description:  V5 project                                                   #
#                                                                              #
# ---------------------------------------------------------------------------- #

# Library imports
from vex import *

# Brain should be defined by default
brain=Brain()

controller_1 = Controller(PRIMARY)
# B = back M = middle F = Front
#L = Left R =Right
b_l = Motor(Ports.PORT19, GearSetting.RATIO_18_1, True)
m_l = Motor(Ports.PORT18, GearSetting.RATIO_18_1, True)
f_l = Motor(Ports.PORT17, GearSetting.RATIO_18_1, True)
spinner = Motor(Ports.PORT12, GearSetting.RATIO_6_1, True)
b_r = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
m_r = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
f_r = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
lifter = Motor(Ports.PORT2, GearSetting.RATIO_36_1, False)
l_wall = DigitalOut(brain.three_wire_port.a)
r_wall = DigitalOut(brain.three_wire_port.b)
bumperswitch = Bumper(brain.three_wire_port.h)

brain.screen.print("Hello V5")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//VARIABLES/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
autons = [
    "0",
    "Offense",
    "Defense",
    "High_Offense",
    "High_Defense",
    "Skills",
    "Test"
]
auton = 1

spinning = False

selected = False

spin_mod = "Off"

height = 0

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///menu///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def menu():
    controller_1.screen.clear_line(1)
    controller_1.screen.set_cursor(1,1)
    controller_1.screen.print(autons[auton] + "  " + spin_mod)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///other func/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



def spin():
    global spinning
    global spin_mod
    if spinning:
        spinning = False
        spinner.stop()
        spin_mod = "Off"
    else:
        spinning = True
        spinner.spin(FORWARD)



def hightenator():
    global height
    global spin_mod
    
    if height == 0:
        spinner.set_velocity(-50, PERCENT)
        spinner.spin(FORWARD)
        spin_mod = "Push Over"
        # lift down untill bumper, spin wheel
        lifter.spin(REVERSE)
        if bumperswitch.pressed:
            # set inter
            lifter.position(0)
            lifter.set_stopping(COAST)
            lifter.stop()

    if height == 1:
        spinner.set_velocity(50, PERCENT)
        spinner.spin(FORWARD)
        lifter.set_stopping(HOLD)
        spin_mod = "Intake"
        # lift to x degrees, spin wheel, when pressed go to x pos r1
        if controller_1.buttonR1.pressing:
            if lifter.position(DEGREES) < 275:
                lifter.spin(FORWARD)
            else:
                lifter.stop()
        else:
            lifter.spin_to_position(250)

    if height == 2:
        lifter.set_stopping(HOLD)
        forwarder = 0
        # find real mesurement
        lifter.spin_to_position(500)
        if controller_1.buttonR1.pressed:
            forwarder += 1
        if forwarder % 2 == 0:
            spinner.set_velocity(100, PERCENT)
            spin_mod = "Shooting"
        else:
            spinner.set_velocity(-100, PERCENT)
            spin_mod = "Shooting_rev"
        # lift to x degrees, spin wheel 100 percent, change directions with r1



def lift_up():
    global height
    if height < 2:
        height += 1

def lift_down():
    global height
    if height > 0:
        height -= 1

    
    




#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///skills func/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def Move(inches, wait_at_end = True, speed = 100):
    #equation to change inches moved into degrees the wheels turned
    degrees = inches * ((60/36)*(3.25*3.141592653589))*2;
    #sets the speed
    f_l.set_velocity(speed, PERCENT)
    m_l.set_velocity(speed, PERCENT)
    b_l.set_velocity(speed, PERCENT)
    f_r.set_velocity(speed, PERCENT)
    m_r.set_velocity(speed, PERCENT)
    b_r.set_velocity(speed, PERCENT)

    f_l.spin_for(FORWARD, degrees, DEGREES, False)
    m_l.spin_for(FORWARD, degrees, DEGREES, False)
    b_l.spin_for(FORWARD, degrees, DEGREES, False)
    f_r.spin_for(FORWARD, degrees, DEGREES, False)
    m_r.spin_for(FORWARD, degrees, DEGREES, False)
    b_r.spin_for(FORWARD, degrees, DEGREES, wait_at_end)


def rotate(direction, degrees, wait_at_end = True, speed = 100):
    # wait_at_end determines if the bot waits before running code after it
    # eg: if wait is false, it will run drive code and fourbar code at the same time

    f_l.set_velocity(speed, PERCENT)
    m_l.set_velocity(speed, PERCENT)
    b_l.set_velocity(speed, PERCENT)
    f_r.set_velocity(speed, PERCENT)
    m_r.set_velocity(speed, PERCENT)
    b_r.set_velocity(speed, PERCENT)

    #left
    # num_turns is a constant for the rotation of the bot 11 * 2 * pi / (3.25 * pip) / 360
    num_turns = degrees*0.0188;
    if direction == "right":    
        f_l.spin_for(FORWARD, num_turns, TURNS, False)
        m_l.spin_for(FORWARD, num_turns, TURNS, False)
        b_l.spin_for(FORWARD, num_turns, TURNS, wait_at_end)


    #turns right
    if direction == "left":
        f_r.spin_for(FORWARD, num_turns, TURNS, False)
        m_r.spin_for(FORWARD, num_turns, TURNS, False)
        b_r.spin_for(FORWARD, num_turns, TURNS, wait_at_end)

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//DriveTrain/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def drivetrain():
    #Drivetrain Kevin Mode
    # calculates the right velocity for with the left to right forward to back
    # controller set up
    # examples:
      #if the position is 3 both should have a posiitve speed
      # if the 3 is positivie but the 1 is negative we should be turning left
      # basically whichever direction we want to go in, the velocity of that side is turned down
    RightVel = (controller_1.axis3.position() - controller_1.axis1.position())
    LeftVel = (controller_1.axis3.position() + controller_1.axis1.position())
    speed = .75
    #prevents the motor from trying to go to fast
    if RightVel > 100:
        RightVel = 100
    
    if LeftVel > 100:
        LeftVel = 100
    
    if RightVel < -100:
        RightVel = -100
    
    if LeftVel < -100:
        LeftVel = -100

    LeftVel= LeftVel*speed
    

    #sets the velocity and goes forward
    f_l.set_velocity(LeftVel, PERCENT)
    m_l.set_velocity(LeftVel, PERCENT)
    b_l.set_velocity(LeftVel, PERCENT)
    f_r.set_velocity(RightVel, PERCENT)
    m_r.set_velocity(RightVel, PERCENT)
    b_r.set_velocity(RightVel, PERCENT)
    f_l.spin(FORWARD)
    m_l.spin(FORWARD)
    b_l.spin(FORWARD)
    f_r.spin(FORWARD)
    m_r.spin(FORWARD)
    b_r.spin(FORWARD)



#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//Autons/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////



def Offense():
    pass

def Defense():
    pass

def High_Offense():
    pass

def High_Defense():
    pass

def Skills():
    pass

def Test():
    pass

def up() :
    global auton
    global selected
    if not selected:
        auton += 1
        if auton > len(autons):
            auton = 1

def down():
    global auton
    global selected
    if not selected:
        auton -= 1
        if auton < 1:
            auton = len(autons)

def select():
    global selected
    controller_1.rumble("-.-.")
    selected = True

def autonomous():
    spinner.set_stopping(COAST)
    brain.screen.clear_screen()
    while True:
        menu()
        hightenator()
        if autons[auton] == "Offense":
            Offense()

        if autons[auton] == "Defense":
            Defense()

        if autons[auton] == "High_Offense":
            High_Offense()

        if autons[auton] == "High_Defense":
            High_Defense()

        if autons[auton] == "Skills":
            Skills()

        if autons[auton] == "Test":
            Test()

def usercontrol():
    spinner.set_stopping(COAST)
    brain.screen.clear_screen()
    while True:
        hightenator()
        menu()
        drivetrain()


menu()

controller_1.buttonUp.pressed(up)
controller_1.buttonDown.pressed(down)
controller_1.buttonR2.pressed(spin)
controller_1.buttonA.pressed(select)
controller_1.buttonL1.pressed(lift_up)
controller_1.buttonL2.pressed(lift_down)
comp = Competition(usercontrol, autonomous)