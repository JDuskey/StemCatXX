import magicbot
from components import Loader, ShooterControl
import wpilib
from wpilib.drive import DifferentialDrive
from robotpy_ext.control.button_debouncer import ButtonDebouncer


class MyRobot(magicbot.MagicRobot):
    loader = Loader.Loader
    shooter_control = ShooterControl.ShooterControl
    def createObjects(self):
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.coStick = wpilib.Joystick(2)

        self.leftMotor = wpilib.Victor(0)
        self.rightMotor = wpilib.Victor(1)
        self.climbMotor = wpilib.Victor(2)
        self.stager_motor = wpilib.Victor(3)
        self.shooter_motor = wpilib.Victor(4)
        self.rearshootMotor = wpilib.Victor(5)
        self.elevatorMotor = wpilib.Victor(6)
        self.shooterTiltMotor = wpilib.Victor(7)
        self.myRobot = DifferentialDrive(self.leftMotor, self.rightMotor)
        # self.pdp = wpilib.PowerDistributionPanel(0)
        self.shooter_motor.setInverted(True)
        self.stager_motor.setInverted(True)
        self.shifter = wpilib.DoubleSolenoid(0, 1)
        self.trigger = ButtonDebouncer(self.rightStick, 1, period=.5)
        self.shifter.set(1)

        self.climbLimitSwitch = wpilib.DigitalInput(8)
        self.ball_center = wpilib.DigitalInput(9)

    def teleopInit(self):
        self.shifter.set(1)

    def teleopPeriodic(self):
        self.myRobot.tankDrive(-self.leftStick.getY(), self.rightStick.getY())

        climbStop = self.climbLimitSwitch.get()


        if self.coStick.getRawButton(1):
            self.elevatorMotor.set(-self.coStick.getY(-.01))

        if self.coStick.getRawButton(6):
            self.climbMotor.set(-1)

        elif self.coStick.getRawButton(4):
            self.climbMotor.set(1)

        else:
            self.climbMotor.set(0)

        if self.coStick.getRawButton(12):
            self.shooter_control.fire()

        if self.coStick.getRawButton(8):
            self.rearshootMotor.set(1)

        elif self.coStick.getRawButton(7):
            self.rearshootMotor.set(-1)

        else:
            self.rearshootMotor.set(0)

        if self.coStick.getRawButton(1):
            self.shooterTiltMotor.set(1)

        elif self.coStick.getRawButton(2):
            self.shooterTiltMotor.set(-1)
        else:
            self.shooterTiltMotor.set(0)

        if self.leftStick.getRawButton(1):
            if self.shifter.get() == 1:
                self.shifter.set(2)
            else:
                self.shifter.set(1)

        if self.coStick.getRawButton(4) == True and climbStop == True:
            self.climbMotor.set(0)


        if self.coStick.getRawButton(3):
            self.loader.load()
        else:
            if not self.shooter_control.running():
                self.loader.stop()







if __name__ == '__main__':
    wpilib.run(MyRobot)
