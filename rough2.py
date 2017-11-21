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
#   Created: 10/20/17 - Dr. Vaughan - 
#   Servomotor code Created: 10/06/17
#       - Dr. Vaughan
#       
#Try Except Code created: 10/26/17 Dr. Vaughan
"""Created: 10/30/17 - Kelli K
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
        motors = motor.DCMotors(i2c)
        BIGDCMOTOR1=0 # DC motor M1
        try:
            motors.speed(BIGDCMOTOR1, 4095)  # Go ~1/2 speed in one direction
            print("Run BIGDCMOTOR")
            time.sleep(5)                       # Continue at this speed for 1s
            # To stop, issue a speed of 0
            motors.speed(BIGDCMOTOR1, 0)
            time.sleep_ms(10) # pause briefly to let the motor stop
            print("Stopping BIGDCMOTOR")
            BLUE_LED = pyb.LED(4)
            #
            print("Turning on LED")
            BLUE_LED.on()           # Turn on at full brightness
            time.sleep_ms(100)           # Sleep 0.1 seconds
        except:
            motors.speed(BIGDCMOTOR1, 0)
            print("Things are not so smooth anymore.")
        finally:
            motors.speed(BIGDCMOTOR1, 0)
            print("Motor Stopped")
        i2c = machine.I2C(scl=machine.Pin('Y9'), sda=machine.Pin('Y10'))
        #And, then initialize the DC motor control object
        motors = motor.DCMotors(i2c)
        linear_adc = pyb.ADC(pyb.Pin("X22"))
        print("prepare for Linear Actuator to start")
        # Now, we can initialize the DC motor object. The number should match the
        # motor number = (number on the motor driver board - 1)
        # For example, M1 on the board is motor 0, M2 on the board is motor 1, etc
        MOTOR_NUMBER = 3 # DC motor M4
        try:
            # To control the actuator, give it a speed between -4095 and 4095
            motors.speed(MOTOR_NUMBER, 2048)    # Go ~1/2 speed in one direction
            time.sleep(4)                       # Continue at this speed for 1s
            print("RUN LIN ACT")
            # ALWAYS STOP THE actuator BEFORE SWITCHING DIRECTIONS!!!!
            # To stop, issue a speed of 0
            motors.speed(MOTOR_NUMBER, 0)
            time.sleep_ms(100) # pause briefly to let the motor stop - 1s here
        except:
            motors.speed(MOTOR_NUMBER, 0)
            print("oh no")
        finally:
            motors.speed(MOTOR_NUMBER, 0)
            print("All stop")
        try:
            motors.speed(BIGDCMOTOR1, -4095)  # Go ~1/2 speed in one direction
            print("Run BIGDCMOTOR")
            time.sleep(2)                       # Continue at this speed for 1s
            # To stop, issue a speed of 0
            motors.speed(BIGDCMOTOR1, 0)
            time.sleep_ms(100) # pause briefly to let the motor stop
            print("Stopping BIGDCMOTOR")
        except:
            motors.speed(BIGDCMOTOR1, 0)
            print("Things are not so smooth anymore.")
        finally:
            motors.speed(BIGDCMOTOR1, 0)
            print("Motor Stopped")
        try:
            print("Turning off ORANGE LED")
            motors.speed(BIGDCMOTOR1, 4095)  # Go ~1/2 speed in one direction
            print("Run BIGDCMOTOR")
            time.sleep(7)                       # Continue at this speed for 1s
            motors.speed(BIGDCMOTOR1, 0)
            time.sleep_ms(100) # pause briefly to let the motor stop
            print("Stopping BIGDCMOTOR")
        except:
            motors.speed(BIGDCMOTOR1, 0)
            print("Things are not so smooth anymore.")
        finally:
            motors.speed(BIGDCMOTOR1, 0)
        try:
            # To control the actuator, give it a speed between -4095 and 4095
            motors.speed(MOTOR_NUMBER, -2048)    # Go ~1/2 speed in one direction
            time.sleep(4)                       # Continue at this speed for 1s
            print("RUN LIN ACT")
            # ALWAYS STOP THE actuator BEFORE SWITCHING DIRECTIONS!!!!
            # To stop, issue a speed of 0
            motors.speed(MOTOR_NUMBER, 0)
            time.sleep_ms(100) # pause briefly to let the motor stop - 1s here
        except:
            motors.speed(MOTOR_NUMBER, 0)
            print("oh no")
        finally:
            motors.speed(MOTOR_NUMBER, 0)
            print("All stop")
        try:
            motors.speed(BIGDCMOTOR1, -4095)  # Go full speed in one direction
            print("Run BIGDCMOTOR")
            time.sleep(5)                       # Continue at this speed for 1s
            motors.speed(BIGDCMOTOR1, 0)
            time.sleep_ms(100) # pause briefly to let the motor stop
            print("Stopping BIGDCMOTOR")
        except:
            motors.speed(BIGDCMOTOR1, 0)
            print("Things are not so smooth anymore.")
        finally:
            motors.speed(BIGDCMOTOR1, 0)
        try:
            # To control the actuator, give it a speed between -4095 and 4095
            motors.speed(MOTOR_NUMBER, 2048)    # Go ~1/2 speed in one direction
            time.sleep(1)                       # Continue at this speed for 1s
            print("RUN LIN ACT")
            # ALWAYS STOP THE actuator BEFORE SWITCHING DIRECTIONS!!!!
            # To stop, issue a speed of 0
            motors.speed(MOTOR_NUMBER, 0)
            time.sleep_ms(100) # pause briefly to let the motor stop - 1s here
        except:
            motors.speed(MOTOR_NUMBER, 0)
            print("oh no")
        finally:
            motors.speed(MOTOR_NUMBER, 0)
            print("All stop")
        try:
            motors.speed(BIGDCMOTOR1, -4095)  # Go ~1/2 speed in one direction
            print("Run BIGDCMOTOR")
            time.sleep(2)                       # Continue at this speed for 1s
            motors.speed(BIGDCMOTOR1, 0)
            time.sleep_ms(100) # pause briefly to let the motor stop
            print("Stopping BIGDCMOTOR")
        except:
            motors.speed(BIGDCMOTOR1, 0)
            print("Things are not so smooth anymore.")
        finally:
            motors.speed(BIGDCMOTOR1, 0)
        try:
            # To control the actuator, give it a speed between -4095 and 4095
            motors.speed(MOTOR_NUMBER, -2048)    # Go ~1/2 speed in one direction
            time.sleep(1)                       # Continue at this speed for 1s
            print("RUN LIN ACT")
            # ALWAYS STOP THE actuator BEFORE SWITCHING DIRECTIONS!!!!
            # To stop, issue a speed of 0
            motors.speed(MOTOR_NUMBER, 0)
            time.sleep_ms(100) # pause briefly to let the motor stop - 1s here
        except:
            motors.speed(MOTOR_NUMBER, 0)
            print("oh no")
            time.sleep(30)
    else:
        print("Start button is not pressed. I'll wait, then check again.\n")
        time.sleep_ms(10)          # Sleep 30 seconds ...10 ms (0.01s)
