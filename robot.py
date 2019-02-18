import magicbot
from components import Loader, ShooterControl, FloorLoader
import wpilib
from wpilib.drive import DifferentialDrive
from robotpy_ext.control.button_debouncer import ButtonDebouncer
from networktables import NetworkTables

class MyRobot(magicbot.MagicRobot):
    loader = Loader.Loader
    floor_loader = FloorLoader.Loader
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
        self.rear_shooter_motor = wpilib.Victor(5)
        self.elevatorMotor = wpilib.Victor(6)
        self.shooterTiltMotor = wpilib.Victor(7)
        self.myRobot = DifferentialDrive(self.leftMotor, self.rightMotor)
        # self.pdp = wpilib.PowerDistributionPanel(0)
        self.front_shooter_motor.setInverted(True)
        self.rear_shooter_motor.setInverted(True)
        self.stager_motor.setInverted(True)
        self.shifter = wpilib.DoubleSolenoid(0, 1)
        self.trigger = ButtonDebouncer(self.rightStick, 1, period=.5)
        self.shifter.set(2)
        self.skis = wpilib.DoubleSolenoid(6, 7)
        self.launcherRotate = wpilib.AnalogInput(0)
        self.climbLimitSwitch = wpilib.DigitalInput(8)
        self.ball_center = wpilib.DigitalInput(9)
        self.elevator_limit = wpilib.DigitalInput(7)
        self.tilt_controller = wpilib.PIDController(4,0,0, self.launcherRotate, self.shooterTiltMotor)
        self.tilt_controller.setPercentTolerance(5)
        self.stager_running = False
    def teleopInit(self):
        self.shifter.set(2)
        self.skis.set(2)
        self.tilt_controller.enable()
        self.tilt_controller.setSetpoint(3.5)
    def teleopPeriodic(self):
        # self.myRobot.tankDrive(-self.leftStick.getY(), self.rightStick.getY())
        #
        # climbStop = self.climbLimitSwitch.get()
        #
        wpilib.DriverStation.reportWarning(str(self.ball_center.get()), False)
        #
        angle = self.launcherRotate.getAverageVoltage()
        if not angle:
               pass
        else:
            self.sd.putNumber("Pot", angle)

        if self.coStick.getRawButton(7):
            self.tilt_controller.setSetpoint(3.54)

        elif self.coStick.getRawButton(8):
            self.tilt_controller.disable()

        elif self.coStick.getRawButton(9):
            self.tilt_controller.setSetpoint(2.29)

        elif self.coStick.getRawButton(11):
            self.tilt_controller.setSetpoint(1.04)

        elif self.coStick.getRawButton(10):
            self.tilt_controller.setSetpoint(1.79)

        if self.coStick.getRawButton(1):
            if self.elevator_limit.get() == False:
                self.elevatorMotor.set(self.coStick.getY(-.01))

            elif self.coStick.getY() < 0 and self.elevator_limit.get() == True:
                self.elevatorMotor.set(self.coStick.getY(-.01))
            else:
                self.elevatorMotor.set(0)

        else:
            self.elevatorMotor.set(0)
        #
        # if self.coStick.getRawButton(2):
        #     if self.launcherRotate.getVoltage() > 1.16 and self.coStick.getY() < 0:
        #         self.shooterTiltMotor.set(self.coStick.getY() * .5)
        #     elif self.launcherRotate.getVoltage() < 3.5 and self.coStick.getY() > 0:
        #         self.shooterTiltMotor.set(self.coStick.getY() * .5)
        # else:
        #     self.shooterTiltMotor.set(0)
        #
        #
        # if self.coStick.getRawButton(6):
        #     self.climbMotor.set(-1)
        #
        # elif self.coStick.getRawButton(4):
        #     self.climbMotor.set(1)
        #
        # else:
        #     self.climbMotor.set(0)
        #
        if self.coStick.getRawButton(12):
            self.shooter_control.fire()
        #
        if self.leftStick.getTrigger():
            self.shifter.set(1)
        else:
            self.shifter.set(2)
        #
        # if self.coStick.getRawButton(4) == True and climbStop == True:
        #     self.climbMotor.set(0)
        #
        #
        if self.coStick.getRawButton(3):
            self.loader.load()
        else:
            if not self.shooter_control.running():
                if not self.floor_loader.running():
                    if self.stager_running == False:
                        self.loader.stop()

        if self.coStick.getRawButton(6):
            self.stager_running = True
            self.stager_motor.set(.5)
        else:
            self.stager_running = False
            if not self.shooter_control.running():
                if not self.floor_loader.running():
                    if not self.loader.running():
                        if self.stager_running == False:
                            self.stager_motor.set(0)

        if self.coStick.getRawButton(4):
            self.floor_loader.load()
        else:
            if not self.shooter_control.running():
                if not self.loader.running():
                    if self.stager_running == False:
                        self.floor_loader.stop()

        if self.leftStick.getRawButton(11):
            self.skis.set(1)

        if self.leftStick.getRawButton(12):
            self.skis.set(2)





if __name__ == '__main__':
    wpilib.run(MyRobot)
