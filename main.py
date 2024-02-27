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
spinner = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
b_r = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
m_r = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
f_r = Motor(Ports.PORT7, GearSetting.RATIO_18_1, False)
lifter_motor_r = Motor(Ports.PORT3, GearSetting.RATIO_36_1, False)
lifter_motor_l = Motor(Ports.PORT13, GearSetting.RATIO_36_1, True)
lifter = MotorGroup(lifter_motor_r, lifter_motor_l)
r_wall = DigitalOut(brain.three_wire_port.a)
l_wall = DigitalOut(brain.three_wire_port.h)
bumperswitch = Bumper(brain.three_wire_port.b)
bumperswitchtwo = Bumper(brain.three_wire_port.g)
allseeingeye = Inertial(Ports.PORT6)
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

auton = 0

selected = False

spin_mode = "Off"

height = 0

spin_direction = 1
spin_simb = "^"


match = False
spinner.set_stopping(COAST)
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///menu///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def menu():
    controller_1.screen.clear_line(1)
    controller_1.screen.set_cursor(1,1)
    controller_1.screen.print(autons[auton] + "  " + spin_mode)

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///BIG LIFT BIG///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def reversal():
    global spin_direction
    global spin_simb
    spin_direction = spin_direction * -1
    if spin_simb == "^":
        spin_simb = "V"
    else:
        spin_simb = "^"
    spinner.stop()
    

def hightenator():
    global height
    global spin_mode
    global spin_direction
    global spin_simb


    if height == 0:
        spinner.set_velocity((spin_direction * 50), PERCENT)
        spinner.spin(FORWARD)
        spin_mode = "Push Over" + spin_simb
        # lift down untill bumper, spin wheel
        while not (bumperswitch.pressed or bumperswitchtwo.pressed):
            lifter.spin(REVERSE)
        lifter.reset_position()
        lifter.set_stopping(COAST)
        lifter.stop()
    
    if height == 1:
        spinner.set_velocity(spin_direction * 50, PERCENT)
        spinner.spin(FORWARD)
        lifter.set_stopping(HOLD)
        spin_mode = "Intake" + spin_simb
        # lift to x degrees, spin wheel, when pressed go to x pos r1
        lifter.spin_to_position(150, wait = False)
        
    
    if height == 2:
        lifter.set_stopping(HOLD)
        spinner.stop()
        lifter.spin_to_position(320, wait = False)
        spin_mode = "None"


    if height == 3:
        lifter.set_stopping(HOLD)
        # find real mesurement
        spinner.set_velocity(spin_direction * 85, PERCENT)
        spinner.spin(FORWARD)
        spin_mode = "Shooting" + spin_simb
        lifter.spin_to_position(500, DEGREES, 100, PERCENT, wait = False)

def weirdthing(height):
    global spin_direction
    if height == 0 or height == 1:
        spin_direction = -1
    if height == 2 or height == 3:
        spin_direction = 1

def lift_up():
    global height
    global spin_simb

    if height < 3:
        height += 1
        spin_simb = "^"
    weirdthing(height)

def lift_down():

    global height
    global spin_simb

    if height > 0:
        height -= 1
        spin_simb = "^"
    weirdthing(height)

def gleb_gleb():
    global height
    height = 0

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///Wall/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def rwall():
    if controller_1.buttonR2.pressing():
        r_wall.set(True)
    else:
        r_wall.set(False)

def lwall():
    if controller_1.buttonR1.pressing():
        l_wall.set(True)
    else:
        l_wall.set(False)

def open():
    r_wall.set(False)
    l_wall.set(False)

def close():
    r_wall.set(True)
    l_wall.set(True)

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///skills func/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def Move(inches, wait_at_end = True, speed = 100):
    #equation to change inches moved into degrees the wheels turned
    degrees = inches * ((60/36)*(3.25*3.141592653589))*2
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


def side(sideof, degrees, wait_at_end = True, speed = 100):
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
    # old 0.0188
    num_turns = degrees*0.0256363636
    if sideof == "left":    
        f_l.spin_for(FORWARD, num_turns, TURNS, False)
        m_l.spin_for(FORWARD, num_turns, TURNS, False)
        b_l.spin_for(FORWARD, num_turns, TURNS, wait_at_end)


    #turns right
    if sideof == "right":
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
    
    move = controller_1.axis3.position()
    turn = controller_1.axis1.position()

    if abs(move) <= 5:
        move = 0

    if abs(turn) <= 5:
        turn = 0

    RightVel = (move - turn)
    LeftVel = (move + turn)

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

def Skills():
    lifter.set_stopping(HOLD)
    lifter.spin_to_position(500, DEGREES, 100, PERCENT, wait = False)
    spinner.spin(FORWARD)
    Move(30)
    side("right", 45)
    open()
    wait(30, SECONDS)
    spinner.stop()
    side("left", 90)
    Move(10)
    lifter.set_stopping(COAST)
    while not bumperswitch or bumperswitchtwo: 
        lifter.spin(REVERSE)
    lifter.stop()
    close()
    side("left", 600, False, -70)
    side("right", 500, True, -50)

    Move(-60)
    side("left", 90)
    Move(50)

    side("left", 20, speed=-70)

    Move(-30)
    Move(5)
    Move(-5)
    side("right", 20, speed=-70)
    Move(-30)
    side("left", 180, speed=70)
    open()
    Move(40)
    Move(-5)
    Move(5)

    close()
    Move(-30)
    side("right", 30)
    open()
    Move(40)
    Move(-5)
    Move(5)

    Move(-40)
    Move(15)
    side("right", 90)
    Move(20)
    side("left", 100)
    Move(30)
    Move(-5)
    Move(5)
    Move(-5)

def Offense():
    Move(-30, wait_at_end = True, speed = 70)
    side("right", 65, wait_at_end = True, speed = 40)
    Move(-5, wait_at_end = True, speed = 70)

def Defense():
    pass

def High_Offense():
    
    open()
    side("left", 60)
    Move(30)
    Move(-30)
    side("left", 90, False, -100)
    side("right", 90, True, 100)
    side("right", 80, False, -70)
    side("left", 40)
    Move(40) 

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
    global match
    match = True
    lifter.reset_position()
    while True:
        menu()
        if autons[auton] == "Offense":
            Offense()
            break

        if autons[auton] == "Defense":
            Defense()
            break

        if autons[auton] == "High_Offense":
            High_Offense()
            break

        if autons[auton] == "High_Defense":
            High_Defense()
            break

        if autons[auton] == "Skills":
            Skills()
            break

        if autons[auton] == "Test":
            Test()
            break
    
def lift_test():
    lifter.set_stopping(HOLD)
    if controller_1.buttonL1.pressing():
        lifter.spin(FORWARD)
    elif controller_1.buttonL2.pressing():
        lifter.spin(REVERSE)
    else:
        lifter.stop()

menu()

def usercontrol():
    global height
    while not selected:
        menu()
    lifter.reset_position()
    if match:
        height = 3
        
    while True:
        rwall()
        lwall()
        menu()
        #lift_test()
        hightenator()
        drivetrain()

#High_Offense()
        
controller_1.buttonUp.pressed(menu_up)
controller_1.buttonDown.pressed(menu_down)
controller_1.buttonA.pressed(select)

comp = Competition(usercontrol, autonomous)

controller_1.buttonL1.pressed(lift_up)
controller_1.buttonL2.pressed(lift_down)
controller_1.buttonLeft.pressed(gleb_gleb)
controller_1.buttonB.pressed(reversal)