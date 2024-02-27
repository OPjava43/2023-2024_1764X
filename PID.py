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
b_l = Motor(Ports.PORT3, GearSetting.RATIO_18_1, True)
m_l = Motor(Ports.PORT18, GearSetting.RATIO_18_1, True)
f_l = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
spinner = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
b_r = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False)
m_r = Motor(Ports.PORT8, GearSetting.RATIO_18_1, False)
f_r = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False)
lifter_motor_r = Motor(Ports.PORT3, GearSetting.RATIO_36_1, False)
lifter_motor_l = Motor(Ports.PORT13, GearSetting.RATIO_36_1, True)
lifter = MotorGroup(lifter_motor_r, lifter_motor_l)
r_wall = DigitalOut(brain.three_wire_port.a)
l_wall = DigitalOut(brain.three_wire_port.h)
bumperswitch = Bumper(brain.three_wire_port.b)
bumperswitchtwo = Bumper(brain.three_wire_port.g)
brain.screen.print("Hello V5")
allseeingeye = Inertial(Ports.PORT6)
allseeingeye.calibrate()






def rotate(targetValue):
    # add KC - a constant, DO A WRAP AROUND, find which one is better
    Kp = 0
    Ki = 0
    Kd = 0
    l_direction = FORWARD
    r_direction = REVERSE
    
    if targetValue < 0:
        l_direction = REVERSE
        r_direction = FORWARD

    integral = 0
    motorVoltage = 100
    sensorReading = allseeingeye.heading(DEGREES)
    error = (targetValue) - (sensorReading)
    previous_error = 0

    while abs(error) > 0.5:
        sensorReading = allseeingeye.heading(DEGREES)
        
        error = (targetValue) - (sensorReading)
        integral = integral + error
        if error > -1 and error < 1:
            integral = 0

        if Kp*integral > 70:
            integral = 70/Kp
        if Kp*integral < -70:
            integral = -70/Kp
        
        derivative = error - previous_error

        previous_error = error

        motorVoltage = (Kp * error) + (integral * Ki) + (derivative * Kd)

        if (motorVoltage >= 127):
            motorVoltage = 127
        f_r.spin(r_direction, motorVoltage, VOLT)
        m_r.spin(r_direction, motorVoltage, VOLT)
        b_r.spin(r_direction, motorVoltage, VOLT)

        f_l.spin(l_direction, motorVoltage, VOLT)
        m_l.spin(l_direction, motorVoltage, VOLT)
        b_l.spin(l_direction, motorVoltage, VOLT)

        wait(10, MSEC)
        print(error)
        
    f_r.stop()
    m_r.stop()
    b_r.stop()
    f_l.stop()
    m_l.stop()
    b_l.stop()

brain.screen.print("gob")
rotate(-90)
brain.screen.print("rob")
wait(5, SECONDS)
brain.screen.print("flob")
rotate(90)
brain.screen.print("nob")