from dpeaDPi.DPiComputer import *
from time import sleep

#
# Create a DPiComputer object
#
dpiComputer = DPiComputer()

#
# Initialize the board to its default values
#
dpiComputer.initialize()

#
# Using hobby "Servo motors" can be an easy way to make things move small
# distances.  Up to 2 servo motors can be connected to the DPiComputer, plugging
# into connectors labeled "SERVO 0" and SERVO 1".  You give these motors a
# value between 0 and 180, with 0 rotating the motor fully counter-clockwise and
# 180 going fully CW. Setting to 90 will center the motor.
#

#
# Rotate the motor plugged into to "SERVO 0", From 0deg to 180deg
#
print("Servo example:")
print("  Rotate Servo 0 CW")
i = 0
servo_number = 0
for i in range(180):
    dpiComputer.writeServo(servo_number, i)
    sleep(.05)

#
# Rotate the motor plugged into to "SERVO 0", From 180deg to 0deg
#
print("  Rotate Servo 0 CCW")
i = 0
servo_number = 0
for i in range(180,0,-1):
    dpiComputer.writeServo(servo_number, i)
    sleep(.05)

#
# Rotate the motor plugged into to "SERVO 1", From 0deg to 180deg
#
print("  Rotate Servo 1 CW")
i = 0
servo_number = 1
for i in range(180):
    dpiComputer.writeServo(servo_number, i)
    sleep(.05)


# Rotate the motor plugged into to "SERVO 0", From 180deg to 0deg
#
print("  Rotate Servo 1 CCW")
i = 0
servo_number = 1
for i in range(180,0,-1):
    dpiComputer.writeServo(servo_number, i)
    sleep(.05)
