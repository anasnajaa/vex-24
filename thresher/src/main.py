#-----------------------------------------------------------------------------*/
#                                                                             */
#     Module:       Thresher Main Code                                        */
#     Authors:      Thamer                                                    */
#     Forked From:  https://github.com/jpearman/v5-drivecode                  */
#     Created:      Sun Jan 12 2025                                           */
#     Description:  Default code for Basking VeXU Robot - Python              */
#     API Ref:      https://api.vex.com/v5/home/python/index.html             */
#                                                                             */
#-----------------------------------------------------------------------------*/

# Library imports
from vex import *

# Brain should be defined by default
brain = Brain()

# We define motors we want to use here 
# we use the motor variable to display statistics later
motor_11 = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False) # left
motor_12 = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False) # left
motor_13 = Motor(Ports.PORT13, GearSetting.RATIO_6_1, True) # left - top
motor_14 = Motor(Ports.PORT14, GearSetting.RATIO_6_1, True) # left - top

motor_20 = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True) # right
motor_19 = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True) # right
motor_18 = Motor(Ports.PORT18, GearSetting.RATIO_6_1, False) # right - top
motor_17 = Motor(Ports.PORT17, GearSetting.RATIO_6_1, False) # right - top


motor_01 = Motor(Ports.PORT1, GearSetting.RATIO_6_1, False)
motor_10 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True) 

motor_8 = Motor(Ports.PORT8, GearSetting.RATIO_36_1, True) 
motor_7 = Motor(Ports.PORT7, GearSetting.RATIO_36_1, False) 


motor_05 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
motor_06 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)


# wait for all motors and sensors to fully initialize
wait(30, MSEC)

# The controller
controller_1 = Controller(ControllerType.PRIMARY)


# Assign generic motor to more useful names
right_drive_1 = motor_20
right_drive_2 = motor_19
right_drive_3 = motor_18
right_drive_4 = motor_17

left_drive_1 =  motor_11
left_drive_2 = motor_12
left_drive_3 = motor_13
left_drive_4 = motor_14

lift_left = motor_8
lift_right = motor_7

intake_roller = motor_01
chain_and_hook = motor_10

intake_roller.set_velocity(500, RPM)
chain_and_hook.set_velocity(200, RPM)

# Max motor speed (percent) for motors controlled by buttons
MAX_RPM = 24 # percent 
MAX_SPEED_INTAKE = 200
MAX_SPEED_ROLLER = 70
mogo_clamp_on = True
climb_hook_on = True
mouth_open = False
intake_on = False

#-----------------------------------------------------------------------------*/
#   @brief  Drive task                                                        */
#-----------------------------------------------------------------------------*/
#
# All motors are controlled from this function which is run as a separate thread
# Axis doc
# https://api.vex.com/v5/home/python/Controller/Controller.Axis.html
# axis1 - Left and right of the right joystick.
# axis2 - Up and down of the right joystick.
# axis3 - Up and down of the left joystick.
# axis4 - Left and right of the left joystick.

def climb_hook_button_pressed():
    global climb_hook_on
    climb_hook_on = not climb_hook_on
    three_wire_mogo_clamp = DigitalOut(brain.three_wire_port.h)
    three_wire_mogo_clamp.set(climb_hook_on)
    return 


def mogo_clamp_button_pressed():
    global mogo_clamp_on
    mogo_clamp_on = not mogo_clamp_on
    three_wire_mogo_clamp = DigitalOut(brain.three_wire_port.g)
    three_wire_mogo_clamp.set(mogo_clamp_on)
    return 

def mouth_button_pressed():
    global mouth_open
    mouth_open = not mouth_open
    three_wire_mouth = DigitalOut(brain.three_wire_port.g)
    three_wire_mouth.set(mouth_open)


def intake_toggle_button_pressed():
    global intake_on
    intake_on = not intake_on    
    return 


# special buttons events
# controller_1.buttonY.pressed(mouth_button_pressed)
controller_1.buttonDown.pressed(mogo_clamp_button_pressed)
controller_1.buttonUp.pressed(climb_hook_button_pressed)
controller_1.buttonY.pressed(intake_toggle_button_pressed)

def drive_task():
    drive_left = 0
    drive_right = 0

    # loop forever
    while True:
        # buttons
        chain_and_hook_m_12 = (controller_1.buttonR1.pressing() - controller_1.buttonL1.pressing()) * MAX_SPEED_INTAKE
        intake_roller_m_19 = (controller_1.buttonR1.pressing() - controller_1.buttonL1.pressing()) * MAX_SPEED_ROLLER

        drive_lift = (controller_1.buttonR2.pressing() - controller_1.buttonL2.pressing()) * MAX_RPM

        drive_left =  (controller_1.axis3.position() - controller_1.axis1.position()) * MAX_RPM
        drive_right = (controller_1.axis3.position() + controller_1.axis1.position()) * MAX_RPM

        # threshold the variable channels so the drive does not
        # move if the joystick axis does not return exactly to 0
        deadband = 15
        if abs(drive_left) < deadband:
            drive_left = 0
        if abs(drive_right) < deadband:
            drive_right = 0

        # The drivetrain
        left_drive_1.spin(FORWARD, drive_left * .5, PERCENT)
        right_drive_1.spin(FORWARD, drive_right * .5, PERCENT)

        left_drive_2.spin(FORWARD, drive_left * .5, PERCENT)
        right_drive_2.spin(FORWARD, drive_right * .5, PERCENT)

        left_drive_3.spin(FORWARD, drive_left * .5, PERCENT)
        right_drive_3.spin(FORWARD, drive_right * .5, PERCENT)

        left_drive_4.spin(FORWARD, drive_left * .5, PERCENT)
        right_drive_4.spin(FORWARD, drive_right * .5, PERCENT)

        # intake roller + chain and hook
        # if intake is toggled on spin forever
        # if intake_on == True:
        #     chain_and_hook.spin(FORWARD, -100, PERCENT)
        #     intake_roller.spin(FORWARD, -100, PERCENT)
        # else:
        #     if controller_1.buttonL2.pressing() or controller_1.buttonR2.pressing():
        #         chain_and_hook2 = (controller_1.buttonR2.pressing() - controller_1.buttonL2.pressing()) * MAX_SPEED_INTAKE
        #         chain_and_hook.spin(FORWARD, chain_and_hook2, PERCENT)
        #     else:
        #         chain_and_hook.spin(FORWARD, chain_and_hook_m_12, PERCENT)
        #         intake_roller.spin(FORWARD, intake_roller_m_19, PERCENT)

        chain_and_hook.spin(FORWARD, chain_and_hook_m_12, PERCENT)
        intake_roller.spin(FORWARD, intake_roller_m_19, PERCENT)

        if controller_1.buttonR2.pressing() or controller_1.buttonL2.pressing():
            lift_left.spin(FORWARD, drive_lift, PERCENT)
            lift_right.spin(FORWARD, drive_lift, PERCENT)
        else:
            lift_left.stop(BRAKE)
            lift_right.stop(BRAKE)

        # No need to run too fast
        # sleep(15)


#------------------------------------------------------------------------------*/
#   @brief      Display data for one motor                                     */
#------------------------------------------------------------------------------*/

# define some more colors
grey = Color(0x202020)
dgrey = Color(0x2F4F4F)
lblue = Color(0x303060)
lred = Color(0x603030)

def displayMotorData(m, index):
    ypos = 0
    xpos = index * 48

    # The actual velocity of the motor in rpm
    v2 = m.velocity(RPM)

    # The position of the motor internal encoder in revolutions
    pos = m.position(TURNS)

    # Motor current in Amps
    c1 = m.current()

    # Motor temperature
    t1 = m.temperature()

    brain.screen.set_font(FontType.MONO15)

    # background color based on
    # device and whether it's left, right or other motor
    if not m.installed():
        brain.screen.set_fill_color(grey)
    elif m == left_drive_1 or m == left_drive_2:
        brain.screen.set_fill_color(lblue)
    elif m == right_drive_1 or m == right_drive_2:
        brain.screen.set_fill_color(lred)
    else:
        brain.screen.set_fill_color(dgrey)

    # Draw outline for motor info
    brain.screen.set_pen_color(Color.WHITE)
    w = 49 if index < 9 else 48
    brain.screen.draw_rectangle(xpos, ypos, w, 79)

    # no motor, then return early
    if not m.installed():
        brain.screen.print_at("NC", x=xpos+15, y=ypos+30)
        return

    # we have no way to get command value in Python VM 1.0.0b20
    # so have to deviate from C++ version, just show port number
    brain.screen.print_at("%02d" % (index+1), x=xpos+13, y=ypos+13)

    # Show actual speed
    brain.screen.set_pen_color(Color.YELLOW)
    brain.screen.print_at("%4d" % v2, x=xpos+13, y=ypos+30)

    # Show position
    brain.screen.print_at("%5.1f" % pos, x=xpos+5, y=ypos+45)

    # Show current
    brain.screen.print_at("%4.1fA" % c1, x=xpos+5, y=ypos+60)

    # Show temperature
    brain.screen.print_at("%4.0fC" % t1, x=xpos+5, y=ypos+75)

    brain.screen.set_pen_color(Color.WHITE)
    brain.screen.draw_line(xpos, ypos+14, xpos+48, ypos+14)

#-----------------------------------------------------------------------------*/
#   @brief  Display task - show some useful motor data                        */
#-----------------------------------------------------------------------------*/

def display_task():
    brain.screen.set_font(FontType.PROP20)
    brain.screen.set_pen_color(Color.RED)
    brain.screen.print_at("TEST DRIVE CODE", x=90, y=160)

    motors = [motor_01,
              motor_12,
              motor_13,
              motor_20,
              motor_13,
              motor_06,
              motor_11,
              motor_12,
              motor_19,
              motor_18]

    while True:
        index = 0
        for m in motors:
            displayMotorData(m, index)
            index = index+1

        # display using back buffer, stops flickering
        brain.screen.render()

        sleep(10)

# Run the display code
display = Thread(display_task)


def setVelocity(percentage):
    right_drive_1.set_velocity(percentage, PERCENT)
    right_drive_2.set_velocity(percentage, PERCENT)
    right_drive_3.set_velocity(percentage, PERCENT)
    left_drive_1.set_velocity(percentage, PERCENT)
    left_drive_2.set_velocity(percentage, PERCENT)
    left_drive_3.set_velocity(percentage, PERCENT)


def rightGearsMove(direction, percentage):
    right_drive_1.spin(direction, percentage, PERCENT)
    right_drive_2.spin(direction, percentage, PERCENT)
    right_drive_3.spin(direction, percentage, PERCENT)

def leftGearsMove(direction, percentage):
    left_drive_1.spin(direction, percentage, PERCENT)
    left_drive_2.spin(direction, percentage, PERCENT)
    left_drive_3.spin(direction, percentage, PERCENT)

def allIntakes(direction, percentage):
    intake_roller.spin(direction, percentage, PERCENT)
    chain_and_hook.spin(direction, percentage, PERCENT)

def autonomous_task():
    brain.screen.print("Auton Started")
    three_wire_mogo_clamp_auton = DigitalOut(brain.three_wire_port.h)

    # open piston
    three_wire_mogo_clamp_auton.set(True)
    brain.screen.set_cursor(3, 1)
    brain.screen.print("Back Piston: Opened")

    rightGearsMove(REVERSE, 35)
    leftGearsMove(REVERSE, 35)
    wait(1.4, SECONDS)  # Move backward for 1.8 seconds

    # Gradual stop of motors after moving backward
    rightGearsMove(REVERSE, 0)
    leftGearsMove(REVERSE, 0)
    wait(0.2, SECONDS)  # Wait for 0.5 seconds


 
    rightGearsMove(FORWARD, 35)
    leftGearsMove(REVERSE, 35)
    wait(0.4, SECONDS)  # Move backward for 1.8 seconds

    # Gradual stop of motors after moving backward
    rightGearsMove(FORWARD, 0)
    leftGearsMove(REVERSE, 0)
    wait(0.2, SECONDS)


    rightGearsMove(REVERSE, 35)
    leftGearsMove(REVERSE, 35)
    wait(0.6, SECONDS)  # Move backward for 1.8 seconds

    # Gradual stop of motors after moving backward
    rightGearsMove(REVERSE, 0)
    leftGearsMove(REVERSE, 0)
    wait(0.2, SECONDS)  # Wait for 0.5 seconds

    rightGearsMove(REVERSE, 35)
    leftGearsMove(FORWARD, 35)
    wait(0.4, SECONDS)  # Move backward for 1.8 seconds

    # Gradual stop of motors after moving backward
    rightGearsMove(REVERSE, 0)
    leftGearsMove(FORWARD, 0)
    wait(0.2, SECONDS)


    rightGearsMove(REVERSE, 35)
    leftGearsMove(REVERSE, 35)
    wait(0.6, SECONDS)  # Move backward for 1.8 seconds

    # Gradual stop of motors after moving backward
    rightGearsMove(REVERSE, 0)
    leftGearsMove(REVERSE, 0)
    wait(0.2, SECONDS)  # Wait for 0.5 seconds


    three_wire_mogo_clamp_auton.set(False)  # Close the pneumatic system
    brain.screen.set_cursor(3, 1)
    brain.screen.print("Back Piston: Closed")

    allIntakes(REVERSE, 100) 
    wait(1.4, SECONDS) 

    rightGearsMove(REVERSE, 35)
    leftGearsMove(FORWARD, 35)
    wait(0.1, SECONDS)  # Move backward for 1.8 seconds

    # Gradual stop of motors after moving backward
    rightGearsMove(REVERSE, 0)
    leftGearsMove(FORWARD, 0)
    wait(0.2, SECONDS)


    rightGearsMove(FORWARD, 30)
    leftGearsMove(FORWARD, 30)
    wait(1.3, SECONDS)  

    rightGearsMove(FORWARD, 0)
    leftGearsMove(FORWARD, 0)
    wait(0.3, SECONDS)

 
    allIntakes(REVERSE, 100) 
    wait(1, SECONDS) 

    rightGearsMove(FORWARD, 35)
    leftGearsMove(REVERSE, 35)
    wait(0.2, SECONDS)  # Move backward for 1.8 seconds

    # Gradual stop of motors after moving backward
    rightGearsMove(FORWARD, 0)
    leftGearsMove(REVERSE, 0)
    wait(0.2, SECONDS)


    rightGearsMove(FORWARD, 30)
    leftGearsMove(FORWARD, 30)
    wait(1.2, SECONDS)  

    rightGearsMove(FORWARD, 0)
    leftGearsMove(FORWARD, 0)
    wait(0.2, SECONDS)

    allIntakes(REVERSE, 100) 
    wait(1.8, SECONDS)  

    wait(0.2, SECONDS)  # Wait for 2 second to allow the pneumatic to activate


    drive_task()

comp = Competition(drive_task, autonomous_task)