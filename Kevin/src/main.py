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
r_wall = Pneumatics(brain.three_wire_port.a)
l_wall = Pneumatics(brain.three_wire_port.b)
bumperswitch = Bumper(brain.three_wire_port.h)
bumperswitchtwo = Bumper(brain.three_wire_port.d)
brain.screen.print("Hello V5")

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//VARIABLES/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
autons = [
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

spin_mode = "Off"

height = 3

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///menu///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def menu():
    controller_1.screen.clear_line(1)
    controller_1.screen.set_cursor(1,1)
    controller_1.screen.print(autons[auton] + "  " + spin_mode)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///other func/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////




def hightenator():
    global height
    global spin_mode
    if height == 0:
        spinner.set_velocity(-50, PERCENT)
        spinner.spin(FORWARD)
        spin_mode = "Push Over"
        # lift down untill bumper, spin wheel
        lifter.reset_position()
        while not (bumperswitch.pressed or bumperswitchtwo.pressed):
            lifter.spin(REVERSE)
        # set inter
        lifter.set_stopping(COAST)
        lifter.stop()
    
    if height == 1:
        spinner.set_velocity(50, PERCENT)
        spinner.spin(FORWARD)
        lifter.set_stopping(HOLD)
        spin_mode = "Intake"
        # lift to x degrees, spin wheel, when pressed go to x pos r1
        lifter.spin_to_position(150)
        lifter.stop()
    
    if height == 2:
        lifter.set_stopping(HOLD)
        spinner.set_velocity(50, PERCENT)
        spinner.spin(FORWARD)
        lifter.spin_to_position(230)
        lifter.stop()

    if height == 3:
        lifter.set_stopping(HOLD)
        # find real mesurement
        spinner.set_velocity(100, PERCENT)
        spinner.spin(FORWARD)
        spin_mod = "Shooting"
        lifter.spin_to_position(500, DEGREES, 100, PERCENT, False)


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

def lwall():
    if r_wall == True:
        r_wall.close()
    if r_wall == False:
        r_wall.open()

def rwall():
    if l_wall == True:
        l_wall.close()
    if l_wall == False:
        l_wall.open()

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
    RightVel = RightVel%100
    
    LeftVel = LeftVel%100

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

def open():
    r_wall.open()
    l_wall.open()

def close():
    r_wall.close()
    l_wall.close()

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#//Autons/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def Skills():
    Move(35, wait_at_end = True, speed = 70)
    rotate("left", -70, wait_at_end = False, speed = 50)
    lifter.spin_to_position(500)
    Move(10, wait_at_end = False, speed = 100)
    open()
    spinner.set_velocity(-100, PERCENT)
    spinner.spin_for(FORWARD, 60, SECONDS)
    lifter.set_stopping(COAST)
    lifter.spin_to_position(100, wait = False)
    close()
    rotate("right", -120, wait_at_end = True)
    Move(60, wait_at_end = True, speed = 100)
    rotate("right", -120, wait_at_end = True)
    Move(40, wait_at_end = True, speed = 100)
    Move(-10, wait_at_end = True, speed = 100)
    Move(10, wait_at_end = True, speed = 100)
    Move(-10, wait_at_end = True, speed = 100)
    lifter.spin_to_position(150, wait = False)
    open()
    spinner.stop()
    Move(100, wait_at_end = True, speed = 100)
    close()
    Move(-30, wait_at_end = True, speed = 100)
    brain.screen.clear_screen()

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

def Test():
    pass


def menu_up() :
    global auton
    global selected
    if not selected:
        auton += 1
        if auton > len(autons)-1:
            auton = 0

def menu_down():
    global auton
    global selected
    if not selected:
        auton -= 1
        if auton < 0:
            auton = len(autons)-1

def select():
    global selected
    controller_1.rumble("-.-.")
    selected = True



def autonomous():
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

controller_1.buttonUp.pressed(menu_up)
controller_1.buttonDown.pressed(menu_down)
controller_1.buttonA.pressed(select)


def usercontrol():
    while not selected:
        menu()

    if autons[auton] == "Skills":
        Move(35, wait_at_end = True, speed = 70)
        rotate("left", -60, wait_at_end = False, speed = 50)
        lifter.spin_to_position(500)
        Move(6, wait_at_end = True, speed = 100)
        open()
        spinner.set_velocity(-100, PERCENT)
        spinner.spin_for(FORWARD, 25, SECONDS)
    
    while True:
        menu()
        hightenator()
        drivetrain()

comp = Competition(usercontrol, autonomous)

controller_1.buttonL1.pressed(lift_up)
controller_1.buttonL2.pressed(lift_down)
controller_1.buttonR1.pressed(lwall)
controller_1.buttonR2.pressed(rwall)
controller_1.buttonLeft.pressed(gleb_gleb)

#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis#penis
