# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       Basking Main Code                                            #
# 	Author:       Yulania                                                      #
# 	Created:      1/4/2025, 6:19:05 PM                                         #
# 	Description:  Default code for Basking VeXU Robot - Python                 #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

# Port 20 front left 
# Port 19 bottom left 
# Port 18 top left 

# Port 17 front right 
# Port 15 bottom right 
# Port 16 top right 

brain = Brain()
controller = Controller()

intake = Motor(Ports.PORT9, GearSetting.RATIO_18_1, True)
intake.set_velocity(200, RPM)

frontIntake = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
frontIntake.set_velocity(200, RPM)

allIntakes = MotorGroup(intake, frontIntake)

frontRightMotor = Motor(Ports.PORT17, GearSetting.RATIO_6_1, False)
backRightMotor = Motor(Ports.PORT15, GearSetting.RATIO_6_1, False)

frontLeftMotor = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
backLeftMotor = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)

TopRightMotor = Motor(Ports.PORT16, GearSetting.RATIO_6_1, True)
TopLeftMotor = Motor(Ports.PORT18, GearSetting.RATIO_6_1, False)

rightGears = MotorGroup(frontRightMotor, backRightMotor, TopRightMotor)
leftGears = MotorGroup(frontLeftMotor, backLeftMotor, TopLeftMotor)

allGears = MotorGroup(frontRightMotor, backRightMotor, TopRightMotor, frontLeftMotor, backLeftMotor, TopLeftMotor)

digOutFront = DigitalOut(brain.three_wire_port.a)
digOutFront.set(False)


def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    while True:
        # testing time -------
        # OLD AUTON - NOT GONNA TEST IT NOW
        rightGears.spin(FORWARD, 75, PERCENT)
        leftGears.spin(FORWARD, 75, PERCENT)
        wait(1.6 ,SECONDS)

        rightGears.spin(FORWARD, 0, PERCENT)
        leftGears.spin(FORWARD, 0, PERCENT)

        allIntakes.spin(FORWARD, 75, PERCENT)
        wait(2, SECONDS)

        allIntakes.spin(FORWARD, 0, PERCENT)
        wait(2, SECONDS)

        # rightGears.spin(FORWARD, 50, PERCENT)
        # leftGears.spin(FORWARD, 50, PERCENT)
        # wait(2.6, SECONDS)

        # rightGears.spin(FORWARD, -50, PERCENT)
        # leftGears.spin(FORWARD, 50, PERCENT)
        # wait(1.1, SECONDS)

        # rightGears.spin(FORWARD, 50, PERCENT)
        # leftGears.spin(FORWARD, 50, PERCENT)
        # wait(2.7, SECONDS)

        # rightGears.spin(FORWARD, -50, PERCENT)
        # leftGears.spin(FORWARD, 50, PERCENT)
        # wait(.9, SECONDS)
        
        # rightGears.spin(FORWARD, 50, PERCENT)
        # leftGears.spin(FORWARD, 50, PERCENT)
        # wait(2, SECONDS)

        # rightGears.spin(FORWARD, -50, PERCENT)
        # leftGears.spin(FORWARD, 50, PERCENT)
        # wait(2.6, SECONDS)

        wait(20, MSEC)


def userControl():
    brain.screen.clear_screen()
    brain.screen.print("driver control")

    digOutState = True  # Track the state of digOut (open or closed)
    buttonUpState = False  # Track the previous state of buttonUp (pressed or not)    
    digOutFrontState = False
    buttonDownState = False

    while True:

        maxRPM = 450
        ForwardBackwardJS = (controller.axis3.position() / 100) * maxRPM
        turningJS = (controller.axis1.position() / 100) * maxRPM

        rightJSspeed = ForwardBackwardJS + turningJS
        leftJSspeed = ForwardBackwardJS - turningJS

        rightGears.spin(FORWARD, leftJSspeed, RPM)
        leftGears.spin(FORWARD, rightJSspeed, RPM)

        brain.screen.clear_screen()
        brain.screen.set_cursor(1, 1)
        brain.screen.print("Left Speed: {:.2f} RPM".format(leftGears.velocity(RPM)))
        brain.screen.set_cursor(2, 1)
        brain.screen.print("Right Speed: {:.2f} RPM".format(rightGears.velocity(RPM)))
        
        # Handle arrow left press for toggling digOut
        if controller.buttonDown.pressing() and not buttonDownState:        # Detect a new press
            digOutFrontState = not digOutFrontState     # Toggle the pneumatic state
            digOutFront.set(digOutFrontState)       # Apply the toggle to the pneumatic system
            if digOutFrontState:
                brain.screen.set_cursor(4, 1)
                brain.screen.print("Pneumatic Opened")
            else:
                brain.screen.set_cursor(4, 1)
                brain.screen.print("Pneumatic Closed")
            buttonDownState = True      # Mark the button as pressed
        
        if not controller.buttonDown.pressing():
            buttonDownState = False     # Reset the button state when released


        maxIntakeAllRPM = 200
        intakeInOutAll = (controller.buttonL1.pressing() - controller.buttonR1.pressing()) * maxIntakeAllRPM 
        intakeInOut = (controller.buttonL2.pressing() - controller.buttonR2.pressing()) * maxIntakeAllRPM
        if intakeInOutAll != 0:
            allIntakes.spin(FORWARD, intakeInOutAll, RPM)
        else:
            allIntakes.spin(FORWARD, 0, RPM)
            intake.spin(FORWARD, intakeInOut, RPM)

        wait(20, MSEC)


# Create competition instance
comp = Competition(userControl, autonomous)

# Actions to do when the program starts
brain.screen.clear_screen()



                                                            ######### ARCHIVE #########


