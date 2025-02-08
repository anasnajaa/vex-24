#-----------------------------------------------------------------------------*/
#                                                                             */
#     Module:       Great White Main Code                                     */
#     Authors:      Bashayer / Abdulaziz / Thamer                             */
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

motor_01 = Motor(Ports.PORT1, GearSetting.RATIO_18_1, False) # left
motor_02 = Motor(Ports.PORT2, GearSetting.RATIO_18_1, False) # left
motor_03 = Motor(Ports.PORT3, GearSetting.RATIO_18_1, False) # left

sensor_rotation = Rotation(Ports.PORT4, False)

motor_08 = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True) # right
motor_09 = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True) # right
motor_10 = Motor(Ports.PORT10, GearSetting.RATIO_18_1, True) # right

motor_07 = Motor(Ports.PORT7, GearSetting.RATIO_18_1, True)
motor_13 = Motor(Ports.PORT13, GearSetting.RATIO_36_1, True)
motor_20 = Motor(Ports.PORT20, GearSetting.RATIO_36_1, False)

motor_05 = Motor(Ports.PORT5, GearSetting.RATIO_18_1, False)
motor_06 = Motor(Ports.PORT6, GearSetting.RATIO_18_1, False)
motor_12 = Motor(Ports.PORT12, GearSetting.RATIO_18_1, False)

# wait for all motors and sensors to fully initialize
wait(30, MSEC)

# The controller
controller_1 = Controller(ControllerType.PRIMARY)


# Assign generic motor to more useful names
right_drive_1 = motor_08
right_drive_2 = motor_09
right_drive_3 = motor_10

left_drive_1 =  motor_01
left_drive_2 = motor_02
left_drive_3 = motor_03

lift_left = motor_13
lift_right = motor_20

intake_roller = motor_07
chain_and_hook = motor_12

#set rpm for intake & chain&hook
intake_roller.set_velocity(200, RPM)
chain_and_hook.set_velocity(200, RPM)

# Max motor speed (percent) for motors controlled by buttons
MAX_SPEED_LIFT = 50
MAX_SPEED_INTAKE = 100
mogo_clamp_on = True
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


def mogo_clamp_button_pressed():
    global mogo_clamp_on
    mogo_clamp_on = not mogo_clamp_on
    three_wire_mogo_clamp = DigitalOut(brain.three_wire_port.h)
    three_wire_mogo_clamp.set(mogo_clamp_on)
    return 


def intake_toggle_button_pressed():
    global intake_on
    intake_on = not intake_on
    return 


# special buttons events
controller_1.buttonA.pressed(mogo_clamp_button_pressed)
controller_1.buttonDown.pressed(intake_toggle_button_pressed)

def drive_task():
    drive_left = 0
    drive_right = 0

    # setup the claw motor
    #claw_motor.set_max_torque(25, PERCENT)
    #claw_motor.set_stopping(HOLD)

    # setup the arm motor
    #arm_motor.set_stopping(HOLD)

    # loop forever
    while True:
        # buttons
        chain_and_hook_m_12 = (controller_1.buttonR2.pressing() - controller_1.buttonL2.pressing()) * MAX_SPEED_INTAKE
        intake_roller_m_19 = (controller_1.buttonR2.pressing() - controller_1.buttonL2.pressing()) * MAX_SPEED_INTAKE
        
        drive_lift = (controller_1.buttonR1.pressing() - controller_1.buttonL1.pressing()) * MAX_SPEED_LIFT
        drive_left = controller_1.axis3.position() + controller_1.axis1.position()
        drive_right = controller_1.axis3.position() - controller_1.axis1.position()


        # threshold the variable channels so the drive does not
        # move if the joystick axis does not return exactly to 0
        deadband = 15
        if abs(drive_left) < deadband:
            drive_left = 0
        if abs(drive_right) < deadband:
            drive_right = 0

        # The drivetrain
        left_drive_1.spin(FORWARD, drive_left, PERCENT)
        right_drive_1.spin(FORWARD, drive_right, PERCENT)

        left_drive_2.spin(FORWARD, drive_left, PERCENT)
        right_drive_2.spin(FORWARD, drive_right, PERCENT)

        left_drive_3.spin(FORWARD, drive_left, PERCENT)
        right_drive_3.spin(FORWARD, drive_right, PERCENT)

        if controller_1.buttonR1.pressing() or controller_1.buttonL1.pressing():
            if sensor_rotation.angle() < 90 or sensor_rotation.angle() > 400:
                # do nothing, the arm is above operational range
                lift_left.stop()
                lift_right.stop()
            else:
                # spin normally
                lift_left.spin(FORWARD, drive_lift, PERCENT)
                lift_right.spin(FORWARD, drive_lift, PERCENT)
        else:
            lift_left.stop(BRAKE)
            lift_right.stop(BRAKE)


        # intake roller + chain and hook
        # if intake is toggled on spin forever
        if intake_on == True:
            chain_and_hook.spin(FORWARD, 100, PERCENT)
            intake_roller.spin(FORWARD, 100, PERCENT)
        else:
            chain_and_hook.spin(FORWARD, chain_and_hook_m_12, PERCENT)
            intake_roller.spin(FORWARD, intake_roller_m_19, PERCENT)

        # No need to run too fast
        sleep(15)

# Run the drive code
drive = Thread(drive_task)


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

    brain.screen.print_at("ROTATION", x=90, y=175)
    brain.screen.print_at(sensor_rotation.angle(), x=90, y=190)

#-----------------------------------------------------------------------------*/
#   @brief  Display task - show some useful motor data                        */
#-----------------------------------------------------------------------------*/

def display_task():
    brain.screen.set_font(FontType.PROP20)
    brain.screen.set_pen_color(Color.RED)
    brain.screen.print_at("TEST DRIVE CODE", x=90, y=160)

    motors = [motor_01,
              motor_02,
              motor_03,
              motor_20,
              motor_13,
              motor_06,
              motor_07,
              motor_12,
              motor_09,
              motor_10]

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
