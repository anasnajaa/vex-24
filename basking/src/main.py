# ---------------------------------------------------------------------------- #
#                                                                              #
# 	Module:       Basking Main Code                                            #
# 	Author:       Yulania                                                      #
# 	Created:      1/4/2025, 6:19:05 PM                                         #
# 	Description:  Default code for Basking VeXU Robot - Python                 #
#                                                                              #
# ---------------------------------------------------------------------------- #

from vex import *

brain = Brain()
controller = Controller()

intake = Motor(Ports.PORT9, GearSetting.RATIO_18_1, False)
intake.set_velocity(200, RPM)

frontIntake = Motor(Ports.PORT10, GearSetting.RATIO_18_1, False)
frontIntake.set_velocity(200, RPM)

allIntakes = MotorGroup(intake, frontIntake)

frontRightMotor = Motor(Ports.PORT12, GearSetting.RATIO_6_1, False)
backRightMotor = Motor(Ports.PORT11, GearSetting.RATIO_6_1, False)

frontLeftMotor = Motor(Ports.PORT20, GearSetting.RATIO_6_1, True)
backLeftMotor = Motor(Ports.PORT19, GearSetting.RATIO_6_1, True)

rightGears = MotorGroup(frontRightMotor, backRightMotor)
leftGears = MotorGroup(frontLeftMotor, backLeftMotor)

allGears = MotorGroup(frontRightMotor, backRightMotor, frontLeftMotor, backLeftMotor)

digOut = DigitalOut(brain.three_wire_port.g)
digOut.set(True)

digOutFront = DigitalOut(brain.three_wire_port.h)
digOutFront.set(False)


def autonomous():
    brain.screen.clear_screen()
    brain.screen.print("autonomous code")
    while True:

        rightGears.spin(FORWARD, 25, PERCENT)
        leftGears.spin(FORWARD, 25, PERCENT)
        wait(.3, SECONDS)
        
        rightGears.spin(REVERSE, 25, PERCENT)
        leftGears.spin(FORWARD, 25, PERCENT)
        wait(.85, SECONDS)

        rightGears.spin(FORWARD, 25, PERCENT)
        leftGears.spin(FORWARD, 25, PERCENT)
        wait(1.15, SECONDS)

        rightGears.spin(FORWARD, 25, PERCENT)
        leftGears.spin(REVERSE, 25, PERCENT)
        wait(.9, SECONDS)

        rightGears.spin(REVERSE, 25, PERCENT)
        leftGears.spin(REVERSE, 25, PERCENT)
        wait(.1, SECONDS)

        intake.spin(FORWARD, 100, PERCENT)
        wait(.5, SECONDS)

        intake.spin(FORWARD, 0, PERCENT)
        wait(.5, SECONDS)

        rightGears.spin(FORWARD, 25, PERCENT)
        leftGears.spin(FORWARD, 25, PERCENT)
        wait(.45, SECONDS)

        rightGears.spin(REVERSE, 25, PERCENT)
        leftGears.spin(FORWARD, 25, PERCENT)
        wait(1.9, SECONDS)

        digOutFront.set(True)
        rightGears.spin(REVERSE, 25, PERCENT)
        leftGears.spin(REVERSE, 25, PERCENT)
        wait(.9, SECONDS)

        digOutFront.set(False)
        rightGears.spin(FORWARD, 25, PERCENT)
        leftGears.spin(REVERSE, 25, PERCENT)
        wait(.6, SECONDS)

        allIntakes.spin(FORWARD, 100, PERCENT)
        rightGears.spin(FORWARD, 25, PERCENT)
        leftGears.spin(FORWARD, 25, PERCENT)
        wait(.9, SECONDS)

        rightGears.spin(FORWARD, 0, PERCENT)
        leftGears.spin(FORWARD, 0, PERCENT)
        wait(1, SECONDS)
        
        rightGears.spin(FORWARD, 25, PERCENT)
        leftGears.spin(REVERSE, 25, PERCENT)
        wait(.7, SECONDS)

        allIntakes.spin(FORWARD, 100, PERCENT)
        rightGears.spin(FORWARD, 50, PERCENT)
        leftGears.spin(FORWARD, 50, PERCENT)
        wait(1.5, SECONDS)

        rightGears.spin(FORWARD, 0, PERCENT)
        leftGears.spin(FORWARD, 0, PERCENT)
        wait(5, SECONDS)

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
        if controller.buttonUp.pressing() and not buttonUpState:  # Detect a new press
            digOutState = not digOutState  # Toggle the pneumatic state
            digOut.set(digOutState)  # Apply the toggle to the pneumatic system
            if digOutState:
                brain.screen.set_cursor(3, 1)
                brain.screen.print("Pneumatic Opened")
            else:
                brain.screen.set_cursor(3, 1)
                brain.screen.print("Pneumatic Closed")
            buttonUpState = True  # Mark the button as pressed

        if not controller.buttonUp.pressing():
            buttonUpState = False  # Reset the button state when released
        

        if controller.buttonDown.pressing() and not buttonDownState:
            digOutFrontState = not digOutFrontState
            digOutFront.set(digOutFrontState)
            if digOutFrontState:
                brain.screen.set_cursor(4, 1)
                brain.screen.print("Pneumatic Opened")
            else:
                brain.screen.set_cursor(4, 1)
                brain.screen.print("Pneumatic Closed")
            buttonDownState = True
        
        if not controller.buttonDown.pressing():
            buttonDownState = False


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


# rightGears = MotorGroup(frontRightMotor, backRightMotor, TopRightMotor)
# leftGears = MotorGroup(frontLeftMotor, backLeftMotor, TopLeftMotor)

# TopRightMotor = Motor(Ports.PORT8, GearSetting.RATIO_18_1, True)
# TopLeftMotor = Motor(Ports.PORT18, GearSetting.RATIO_18_1, False)

# allGears = MotorGroup(frontRightMotor, backRightMotor, TopRightMotor, frontLeftMotor, backLeftMotor, TopLeftMotor)




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






        # rightGears.spin(FORWARD, 50, PERCENT)
        # leftGears.spin(FORWARD, 50, PERCENT)
        # wait(.8, SECONDS)
        # # testing time -------
        # # rightGears.spin(REVERSE, 25, PERCENT)
        # # leftGears.spin(REVERSE, 25, PERCENT)
        # # wait(.35 ,SECONDS)
        
        # # rightGears.spin(FORWARD, 0, PERCENT)
        # # leftGears.spin(FORWARD, 0, PERCENT)
        # # wait(.5, SECONDS)

        # # rightGears.spin(REVERSE, 45, PERCENT)
        # # leftGears.spin(FORWARD, 45, PERCENT)
        # # wait(.45, SECONDS)

        # # rightGears.spin(FORWARD, 50, PERCENT)
        # # leftGears.spin(FORWARD, 50, PERCENT)
        # # wait(.6, SECONDS)
