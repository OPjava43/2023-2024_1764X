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
b_l = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)
m_l = Motor(Ports.PORT19, GearSetting.RATIO_18_1, False)
f_l = Motor(Ports.PORT20, GearSetting.RATIO_18_1, False)
spinner = Motor(Ports.PORT5, GearSetting.RATIO_6_1, False)
b_r = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
m_r = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
f_r = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
l_wall = DigitalOut(brain.three_wire_port.a)
r_wall = DigitalOut(brain.three_wire_port.b)

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

#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#///other func/////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
#////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
def spin():

    global spinning
    if spinning:
        spinning = False
        spinner.stop()
    else:
        spinning = True
        spinner.set_velocity(100, PERCENT)
        spinner.spin(FORWARD)



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
    RightVel = (controller_1.axis3.position() - controller_1.axis1.position());
    LeftVel = (controller_1.axis3.position() + controller_1.axis1.position());
    #prevents the motor from trying to go to fast
    if RightVel > 100:
        RightVel = 100
    
    if LeftVel > 100:
        LeftVel = 100
    
    if RightVel < -100:
        RightVel = -100
    
    if LeftVel < -100:
        LeftVel = -100
    

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


        
def menu():
    controller_1.screen.clear_line(1)
    controller_1.screen.set_cursor(1,1)
    controller_1.screen.print(autons[auton])

def up() :
    global auton
    global selected
    if not selected:
        auton += 1
        if auton > len(autons):
            auton = 1
        menu()

def down():
    global auton
    global selected
    if not selected:
        auton -= 1
        if auton < 1:
            auton = len(autons)
        menu()

def select():
    global selected
    controller_1.rumble("-.-.")
    selected = True

def autonomous():
    spinner.set_stopping(COAST)
    brain.screen.clear_screen()
    while True:
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
    count = 0
    brain.screen.clear_screen()
    while True:
        brain.screen.print_at("driver... %6d" %(count), x=10, y=40)
        count = count + 1
        wait(20, MSEC)


menu()

controller_1.buttonUp.pressed(up)
controller_1.buttonDown.pressed(down)
controller_1.buttonR2.pressed(spin)
controller_1.buttonA.pressed(select)
comp = Competition(usercontrol, autonomous)