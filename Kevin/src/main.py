# ---------------------------------------------------------------------------- #
#                                                                              #
#   Module:       main.py                                                      #
#   Author:       student                                                      #
#   Created:      1/4/2024, 3:53:42 PM                                         #
#   Description:  V5 project                                                   #
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
da_walls = Pneumatics(brain.three_wire_port.a)
bumperswitch = Bumper(brain.three_wire_port.h)
bumperswitchtwo = Bumper(brain.three_wire_port.b)
brain.screen.print("Hello V5")
pnumatic_switcher = False

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

height = 3

forwarder = 0
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




def hightenator():
    global height
    global spin_mod
    global forwarder
    if height == 0:
        spinner.set_velocity(-50, PERCENT)
        spinner.spin(FORWARD)
        spin_mod = "Push Over"
        # lift down untill bumper, spin wheel
        lifter.reset_position()
        lifter.spin(REVERSE)
        if bumperswitch.pressed or bumperswitchtwo.pressed:
            # set inter
            lifter.set_stopping(COAST)
            lifter.stop()
    
    if height == 1:
        spinner.set_velocity(50, PERCENT)
        spinner.spin(FORWARD)
        lifter.set_stopping(HOLD)
        spin_mod = "Intake"
        # lift to x degrees, spin wheel, when pressed go to x pos r1
        lifter.spin_to_position(150)
        lifter.stop()
    
    if height == 2:
        lifter.set_stopping(HOLD)
        spinner.set_velocity(50, PERCENT)
        spinner.spin(FORWARD)
        lifter.spin_to_position(230)
        lifter.stop()
    """
    if height == 1:
        lifter.set_stopping(HOLD)
        lifter.spin_to_position(80, DEGREES, 100, PERCENT, False)

    """
    if height == 3:
        lifter.set_stopping(HOLD)
        # find real mesurement
        lifter.spin_to_position(500, DEGREES, 100, PERCENT, False)
        brain.screen.print(forwarder)
        if forwarder % 2 == 0:
            spinner.set_velocity(-100, PERCENT)
            spinner.spin(FORWARD)
            spin_mod = "Shooting"
        else:
            spinner.set_velocity(100, PERCENT)
            spinner.spin(FORWARD)
            spin_mod = "Shooting_rev"
        # lift to x degrees, spin wheel 100 percent, change directions with r1



def lift_up():
    global height
    if height < 3:
        height += 1
    if height > 3:
        height -= 1

def lift_down():
    global height
    if height > 0:
        height -= 1
    if height < 0:
        height += 1


def forwarding():
    global forwarder
    forwarder += 1

def walls_open():

    da_walls.open()

def walls_close():
    
    da_walls.close()


def gleb_gleb():

    global height

    height = 0

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
    if direction == "left":    
        f_l.spin_for(FORWARD, num_turns, TURNS, False)
        m_l.spin_for(FORWARD, num_turns, TURNS, False)
        b_l.spin_for(FORWARD, num_turns, TURNS, wait_at_end)


    #turns right
    if direction == "right":
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
    speed = 1
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
    RightVel = RightVel*speed

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
    Move(35, wait_at_end = True, speed = 70)
    rotate("left", -70, wait_at_end = True, speed = 50)
    wait(100, SECONDS)

def Defense():
    pass

def High_Offense():
    pass

def High_Defense():
    pass

def Skills():
    Move(35, wait_at_end = True, speed = 50)
    rotate("left", -70, wait_at_end = True, speed = 50)
    lifter.spin_to_position(230)
    spinner.spin(FORWARD)
    Move(10, wait_at_end = True, speed = 50)
    da_walls.open()
    wait(30, SECONDS)
    da_walls.close()

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
    # skills auto, quote out if coding for matches
    Move(35, wait_at_end = True, speed = 70)
    rotate("left", -70, wait_at_end = False, speed = 50)
    lifter.spin_to_position(500)
    Move(10, wait_at_end = False, speed = 100)
    da_walls.open()
    spinner.set_velocity(-100, PERCENT)
    spinner.spin_for(FORWARD, 60, SECONDS)
    lifter.set_stopping(COAST)
    lifter.spin_to_position(100, wait = False)
    da_walls.close()
    rotate("right", -120, wait_at_end = True)
    Move(60, wait_at_end = True, speed = 100)
    rotate("right", -120, wait_at_end = True)
    Move(40, wait_at_end = True, speed = 100)
    Move(-10, wait_at_end = True, speed = 100)
    Move(10, wait_at_end = True, speed = 100)
    Move(-10, wait_at_end = True, speed = 100)
    lifter.spin_to_position(150, wait = False)
    da_walls.open()
    spinner.stop()
    Move(100, wait_at_end = True, speed = 100)
    da_walls.close()
    Move(-30, wait_at_end = True, speed = 100)
    brain.screen.clear_screen()

    wait(10000, SECONDS)
    


    while True:
        menu()
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



menu()

controller_1.buttonUp.pressed(up)
controller_1.buttonDown.pressed(down)
controller_1.buttonA.pressed(select)


def usercontrol():
    
    Move(35, wait_at_end = True, speed = 70)
    rotate("left", -60, wait_at_end = False, speed = 50)
    lifter.spin_to_position(500)
    Move(6, wait_at_end = True, speed = 100)
    da_walls.open()
    spinner.set_velocity(-100, PERCENT)
    spinner.spin_for(FORWARD, 25, SECONDS)
    
    while True:
        hightenator()
        menu()
        drivetrain()

comp = Competition(usercontrol, autonomous)

controller_1.buttonR1.pressed(forwarding)
controller_1.buttonL1.pressed(lift_up)
controller_1.buttonL2.pressed(lift_down)
controller_1.buttonR2.pressed(walls_open)
controller_1.buttonA.pressed(walls_close)
controller_1.buttonLeft.pressed(gleb_gleb)

#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis
