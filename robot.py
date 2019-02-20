import magicbot
from components import Loader, ShooterControl, FloorLoader
import wpilib
from wpilib.drive import DifferentialDrive
from robotpy_ext.control.button_debouncer import ButtonDebouncer
from networktables import NetworkTables

class MyRobot(magicbot.MagicRobot):
    # loader = Loader.Loader
    # floor_loader = FloorLoader.Loader
    shooter_control = ShooterControl.ShooterControl
    sd = NetworkTables.getTable('SmartDashboard')
    def createObjects(self):
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.coStick = wpilib.Joystick(2)

        self.leftMotor = wpilib.Victor(0)
        self.rightMotor = wpilib.Victor(1)
        self.climbMotor = wpilib.Victor(2)
        self.stager_motor = wpilib.Victor(3)
        #Practice bot front_shooter_motor is pwm port 9, comp bot is port 4
        self.front_shooter_motor = wpilib.Victor(9)
        # self.rear_shooter_motor = wpilib.Victor(5)
        self.elevatorMotor = wpilib.Victor(6)
        self.elevatorMotor.setInverted(True)
        self.shooterTiltMotor = wpilib.Victor(7)
        self.myRobot = DifferentialDrive(self.leftMotor, self.rightMotor)
        # # self.pdp = wpilib.PowerDistributionPanel(0)
        self.climbMotor.setInverted(True)
        # self.rear_shooter_motor.setInverted(True)
        self.stager_motor.setInverted(True)
        self.shifter = wpilib.DoubleSolenoid(0, 0, 1)
        self.trigger = ButtonDebouncer(self.rightStick, 1, period=.5)
        self.shifter.set(2)
        self.skis = wpilib.DoubleSolenoid(4, 5)
        self.launcherRotate = wpilib.AnalogInput(0)
        self.climbLimitSwitch = wpilib.DigitalInput(8)
        self.ball_center = wpilib.DigitalInput(9)
        self.elevator_limit = wpilib.DigitalInput(7)
        self.pins = wpilib.DoubleSolenoid(2,3)
        # self.climbMotor.setInverted(True)
        self.tilt_limit = wpilib.DigitalInput(6)
        self.tilt_controller = wpilib.PIDController(4,0,0, self.launcherRotate, self.shooterTiltMotor)
                        #Practice bot(4,0,0)
                        #Comp bot(0,0,0)
        self.tilt_controller.setPercentTolerance(5)
        self.elevator_encoder = wpilib.Encoder(0, 1)
        self.elevator_controller = wpilib.PIDController(.0025, 0,0.001, self.elevator_encoder, self.elevatorMotor)
                        #practice bot(0.0125,0,0.0125)
        #               #Comp bot(0,0,0)
        self.elevator_controller.setOutputRange(-1,.25)
        self.elevator_controller.setPercentTolerance(10)
        self.stager_running = False
        self.gears = wpilib.DoubleSolenoid(6,7)
    def teleopInit(self):
        self.shifter.set(2)
        self.skis.set(2)
        self.gears.set(1)

        # if self.elevator_limit == False:
        #     self.elevatorMotor.set(.5)
        self.elevator_controller.disable()
        self.tilt_controller.enable()
        self.tilt_controller.setSetpoint(3.55)
    def teleopPeriodic(self):
        self.myRobot.tankDrive(-self.leftStick.getY(), -self.rightStick.getY())
        # controlY = 2 * ((self.controlBoard.getY() - 0) / (.1181 - 0)) - 1
        wpilib.DriverStation.reportWarning(str(self.leftMotor.get),False)

        # if self.coStick.getRawButton(1):
        #     self.tilt_controller.setSetpoint(2.35)
        # else:
        #     self.elevatorMotor.set(0)

        if self.rightStick.getRawButton(5):
            self.tilt_controller.enable()
            self.tilt_controller.setSetpoint(2.55)
            #Comp bot 2.55
            #Practice bot 2.4

        if self.rightStick.getRawButton(2):
            self.elevatorMotor.set(self.rightStick.getY())
        # if self.rightStick.getY() >.1 or self.rightStick.getY() < .1:
        #     self.elevatorMotor.set(self.rightStick.getY())
        # else:
        #     if self.elevator_controller.isEnabled() == False:
        #         self.elevatorMotor.set(0)
        #     else:
        #         pass
        # elif self.rightStick.getRawButton(4):
        #     self.shooterTiltMotor.set(-.5)

        # if self.coStick.getRawButton(12):
        #     if self.ball_center.get() == True:
        #         self.stager_motor.set(.5)
        #         self.front_shooter_motor.set(.5)
        # else:
        #     if self.shooter_control.running():
        #         pass
        #     else:
        #         self.front_shooter_motor.set(0)
        #         self.stager_motor.set(0)
        #
        if self.rightStick.getRawButton(3):
            self.tilt_controller.enable()
            self.tilt_controller.setSetpoint(3.65)
            #Comp bot 3.65
            #comp bot 3.55
        #

        # if self.tilt_limit.get() == True:
        #     if self.tilt_controller.isEnabled():
        #         if self.tilt_controller.get() < 0:
        #             pass
        #         else:
        #             self.tilt_controller.disable()
        #     else:
        #         self.shooterTiltMotor.set(0)
        #
        # elif self.tilt_controller.isEnabled():
        #     pass
        # else:
        #     self.shooterTiltMotor.set(0)
        #
        # # if self.tilt_limit.get() == True:
        # #     if self.tilt_controller.isEnabled():
        # #         if self.tilt_controller.get() > 0:
        # #             pass
        # #         else:
        # #             self.tilt_controller.disable()
        # #     else:
        # #         self.shooterTiltMotor.set(0)
        #
        # wpilib.DriverStation.reportWarning(str(self.launcherRotate.getAverageVoltage()), False)
        # #
        # if self.coStick.getRawButton(2):
        #     self.shooter_control.fire()
        # #
        # if self.elevator_limit.get() == True:
        #     self.elevator_encoder.reset()
        #     if self.coStick.getY() < 0:
        #         self.elevatorMotor.set(self.coStick.getY())
        #     else:
        #         self.elevatorMotor.set(0)
        #
        # else:
        #     self.elevatorMotor.set(self.coStick.getY())
        # #
        # #
        # # # if self.elevator_limit.get() == False:
        # # #     self.elevatorMotor.set(self.coStick.getY())
        # # # else:
        # # #     self.elevator_encoder.reset()
        # # #     if self.coStick.getY() > 0:
        # # #         self.elevatorMotor.set(self.coStick.getY())
        # # #     else:
        # # #         self.elevatorMotor.set(0)
        # # if self.coStick.getRawButton(4):
        # #     self.elevator_controller.enable()
        # #     self.elevator_controller.setSetpoint(-3500)
        # #
        # #
        # if self.coStick.getRawButton(5):
        #     self.elevatorMotor.set(.8)
        # elif self.coStick.getRawButton(3):
        #     self.elevatorMotor.set(-.5)
        # else:
        #     self.elevatorMotor.set(0)

        if self.coStick.getRawButton(9):
            self.elevator_controller.enable()
            self.elevator_controller.setSetpoint(-2494)

        if self.coStick.getRawButton(10):
            self.elevator_controller.enable()
            self.elevator_controller.setSetpoint(-3040)

        if self.coStick.getRawButton(11):
            self.elevator_controller.setSetpoint(0)

        if self.coStick.getRawButton(7):
            self.elevator_controller.enable()
            self.elevator_controller.setSetpoint(-4843)

        if self.coStick.getRawButton(8):
            self.elevator_controller.enable()
            self.elevator_controller.setSetpoint(-5358)

        if self.coStick.getRawButton(12):
            self.elevator_controller.enable()
            self.elevator_controller.setSetpoint(-725)

        if self.coStick.getRawButton(3):
            self.elevator_controller.enable()
            self.elevator_controller.setSetpoint(-1038)

        if self.coStick.getRawButton(5):
            self.elevator_controller.enable()
            self.elevator_controller.setSetpoint(-1753)

        if self.elevator_limit.get():
            self.elevator_encoder.reset()

        # if self.rightStick.getRawButton(3):
        #     self.tilt_controller.setSetpoint(3.55)

        if self.rightStick.getRawButton(4):
            self.tilt_controller.setSetpoint(3.7)
        if self.tilt_limit.get() == True:
            pass
        if self.rightStick.getTrigger():
            self.shifter.set(2)
        else:
            self.shifter.set(1)

        if self.coStick.getTrigger():
            self.shooter_control.fire()
        if self.coStick.getRawButton(2):
            if self.ball_center.get() == True:
                self.front_shooter_motor.set(-1)

            else:
                self.front_shooter_motor.set(0)
        else:
            if not self.shooter_control.running():
                self.front_shooter_motor.set(0)


        if self.coStick.getRawButton(4):
            self.climbMotor.set(1)

        elif self.coStick.getRawButton(6):
            self.climbMotor.set(-1)

        else:
            self.climbMotor.set(0)

        if self.leftStick.getRawButton(12):
            self.skis.set(2)
        if self.leftStick.getRawButton(11):
            self.skis.set(1)

        if self.leftStick.getTrigger():
            self.gears.set(2)
        if self.leftStick.getRawButton(2):
            self.gears.set(1)

        if self.leftStick.getRawButton(7):
            self.pins.set(1)
        try:
            self.sd.putNumber("PID OUTPUT", self.tilt_controller.get())
        except:
            pass

if __name__ == '__main__':
    wpilib.run(MyRobot)
