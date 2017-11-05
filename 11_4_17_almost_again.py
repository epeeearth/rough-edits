#--------------------------------------------------
# rough2.py
#
# Some description of functionality
#
# Links to relevant documentation:
#   https://github.com/DocVaughan/MCHE201---Intro-to-Eng-Design
#    DC Motor Code adapted from:
#     http://docs.micropython.org/en/latest/pyboard/pyboard/tutorial/servo.html
#DC MOtor code requires the .mpy files from the repository to be on the pyboard.
#     https://github.com/adafruit/micropython-adafruit-pca9685
#    For more information see:
#https://learn.adafruit.com/micropython-hardware-pca9685-dc-
#motor-and-stepper-driver
#     The circuit on the shield is identical to the Feather board shown in that
#     tutorial.
#   DC MOtor Code:
#   Created: 10/20/17 - Joshua Vaughan -
#   Servomotor code Created: 10/06/17
#       - Joshua Vaughan
#       - 
#       - http://www.ucs.louisiana.edu/~jev9637
#Try Except Code created: 10/26/17Joshua Vaughan
"""Created: 10/30/17 - Kelli K"""
# Modified:
#   * 10/31/17 - Kelli K (email if not same person as above)
#     - fixed spacing issues in some places
#     - added while loop
#     - added blue LED
#     - took out  linear Actuator
#     - worked on getting start button to worke
#
#   * 11/01/17 - Kelli K (email if not same person as above)
#     - defined Motors
#     - changed time of motors running
#
#   * 11/04/17 - Kelli K(email if not same person as above)
#     - added code for servo motors
#     - added sleep mode for 30 seconds in while loop
#     - added additional comments to give credit for souce code
#     -
#
# TODO:
#   * 11/04/17 - Major bug to fix, find whitespace error and LIN ACT RUN
#   # mm/dd/yy - Desired new feature
#   #10/30/17 - Get DC Motors and Linear Actuator to Run
#   #10/30/17 - Get Start Button to Run
#
# -----------------------------------------------------------------------------
import pyb# import the pyboard module
import time# import the time module
import machine# We'll use the machine i2c implementation.
import motor# We also need to import the DC motor code from the library
# Assign the input pin to variable input_pin
# We set it up as an input with a pulldown resistor
input_pin = pyb.Pin('X4', pyb.Pin.IN, pull=pyb.Pin.PULL_DOWN)
i2c = machine.I2C(scl=machine.Pin('Y9'), sda=machine.Pin('Y10'))
# And, then initialize the DC motor control object
# Initialize communication with the motor driver
motors = motor.DCMotors(i2c)
linear_adc = pyb.ADC(pyb.Pin("X22"))
def handle_start_signal(line):
    # We need the global modifier here to enable changing
    # the value of a global variable (start_trial in this case)
    global start_trial
    # Turn on the green LED to indicate the trial is starting, but only
    # if this is our first time starting the trial
    if start_trial == False:
        GREEN_LED.on()
    start_trial = True
# This flag variable will be checked in the main part of the script, and
# changed by an interrupt handler function attached to the track banana plugs
start_trial = False

# Assign the start pin to variable start_pin
# We set it up as an input with a pulldown resistor and add an interrupt to
# handle when it is pressed. This interrupt looks for rising edges, meaning
# when the state changes from low to high
start_pin = pyb.ExtInt(pyb.Pin('X4'),
                       pyb.ExtInt.IRQ_RISING,
                       pyb.Pin.PULL_DOWN,
                       handle_start_signal)

# Let's also set up the green LED to turn on when we sense the start button
GREEN_LED = pyb.LED(2)
# This will loop forever, checking the button every 10ms
while (True):
    input_state = input_pin.value()   # read the state of the input
    if (input_pin.value()):
        print("The start button is pressed. I'll run the main code now.\n")
        # Now, we can initialize the DC motor object. The number should match
    	# the motor number = (number on the motor driver board - 1)
    	# For example, M1 on the board is motor 0, M2 on the board is motor 1
        #motors = motor.DCMotors(i2c)
        #BIGDCMOTOR1=2 # DC motor M3
        try:
            #motors.speed(BIGDCMOTOR1, -4095)  # Go ~1/2 speed in one direction
            print("Run BIGDCMOTOR")
            time.sleep(1)                       # Continue at this speed for 1s
            # To stop, issue a speed of 0
            #motors.speed(BIGDCMOTOR1, 0)
            time.sleep_ms(10) # pause briefly to let the motor stop
            print("Stopping BIGDCMOTOR")
            BLUE_LED = pyb.LED(4)
            #
            print("Turning on LED")
            BLUE_LED.on()           # Turn on at full brightness
            time.sleep_ms(100)           # Sleep 1 second
        except:
            #motors.speed(BIGDCMOTOR1, 0)
            print("Things are not so smooth anymore.")
        finally:
            #motors.speed(BIGDCMOTOR1, 0)
            print("Motor Stopped")
        # Define the servo object. The numbering scheme differs between the
        # pyboard and the pyboard LITE.
        #
        # For the pyboard:
        #  Servo 1 is connected to X1, Servo 2 to X2, Servo 3 to X3,
        # and Servo 2 to X4
        # For the pyboard LITE:
        #  Servo 1 is connected to X3, Servo 2 to X4, Servo 3 to X1, and
        # Servo 2 to X2
        # Here, we'll use the first position on the pyboard
        servo1 = pyb.Servo(1)
        #
        # Now, we can control the angle of the servo
        # The range of possible angles is -90 < angle < 90, but many servos
        # can't move over that entire range. A safer range is -60 < angle < 60
        # or even -45 < angle < 45
        servo1.angle(45)
        #
        # Sleep 1s to let it move to that angle
        time.sleep(1)
        #
        current_angle = servo1.angle()
        print("The current servo angle {:+5.2f} degrees.".format(current_angle))
        # Move to 0 degrees
        servo1.angle(0)
        servo1.angle(0, 2000)
        # Sleep 1s to let it move to that angle
        time.sleep(1)
        #
        # Move to -45degrees
        servo1.angle(-45)
        servo1.angle(-45, 2000)
        #
        # Sleep 1s to let it move to that angle
        time.sleep(1)
        current_angle = servo1.angle()
        print("current servo angle is {:+5.2f} degrees.".format(current_angle))
        # Finally, we can also specify how long it should take the servo to
        # move to the commanded angle by adding a second argument to the
        #  .angle() call. The
        #argument should be the time to move in milliseconds (1000 = 1s)
        current_angle = servo1.angle()
        print(" final angle of {:+5.2f} degrees.".format(current_angle))
        try:
            ORANGE_LED = pyb.LED(3)
            BLUE_LED = pyb.LED(4)
            print("Turning on ORANGE LED, and turning off BLUE LED")
            BLUE_LED.off()          # Turn off Red LED
            RED_LED.on()           # Turn on at full brightness
            time.sleep_ms(100)           # Sleep 100 milliseconds
        except:
        	#motors.speed(BIGDCMOTOR1, 0)
        	print("Things are not so smooth anymore.")
        finally:
            #motors.speed(BIGDCMOTOR1, 0)
            time.sleep_ms(10)
        #SMALLDCMOTOR2 = 3 # DC motor M4
        try:
        	# To control the motor, give it a speed between -4095 and 4095
            #motors.speed(SMALLDCMOTOR2, 4095) # Go ~1/2 speed in one direction
            print("Run Small DC Motor")
            #time.sleep(10)                    # Continue at this speed for 1s
            # To stop, issue a speed of 0
            #motors.speed(SMALLDCMOTOR2, 0)
            time.sleep_ms(10) # pause briefly to let the motor stop
            print("Stopping Small DC Motor")
        except:
        	#motors.speed(SMALLDCMOTOR2, 0)
        	print("Things are not so smooth anymore.")
        finally:
        	#motors.brake(SMALLDCMOTOR2)
            print("Stopping Small DC Motor")
        MOTOR_NUMBER = 0 # M1
        try:
            time.sleep(5)
            ORANGE_LED.off()           # Turn on at full brightness
            print("Turn ORANGE LED OFF")
            motors.speed(MOTOR_NUMBER, 2048)    # Go ~1/2 speed in one direction
            time.sleep(10)                       # Continue at this speed for 1s
            motors.speed(MOTOR_NUMBER, 0)
            time.sleep(1) # pause briefly to let the motor stop - 1s here
            print("LIN ACT RUN")
        except: # If any error occurs, then stop the motors
            motors.speed(MOTOR_NUMBER, 0)
            print("LIN ACT stopped")
        finally: # If any error occurs, then stop the motors
            motors.speed(MOTOR_NUMBER, 0)
            print("All Stop")
            time.sleep(30) #sleep 30 seconds
    else:
        print("Start button is not pressed. I'll wait, then check again.\n")
        time.sleep_ms(10)          # Sleep 30 seconds ...10 ms (0.01s)
