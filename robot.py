import magicbot
import wpilib
from wpilib.drive import DifferentialDrive
from robotpy_ext.control.button_debouncer import ButtonDebouncer
from networktables import NetworkTables


class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.coStick = wpilib.Joystick(2)

        self.leftMotor = wpilib.Victor(0)
        self.rightMotor = wpilib.Victor(1)
        self.climbMotor = wpilib.Victor(2)
        self.stagerMotor = wpilib.Victor(3)
        self.frontshootMotor = wpilib.Victor(4)
        self.rearshootMotor = wpilib.Victor(5)
        self.elevatorMotor = wpilib.Victor(6)
        self.shooterTiltMotor = wpilib.Victor(7)
        self.myRobot = DifferentialDrive(self.leftMotor, self.rightMotor)

        self.shifter = wpilib.DoubleSolenoid(0, 1)
        self.trigger = ButtonDebouncer(self.rightStick, 1, period=.5)
        self.shifter.set(1)

        self.limitSwitch = wpilib.DigitalInput(9)

    def teleopInit(self):
        self.shifter.set(1)

    def teleopPeriodic(self):
        self.myRobot.tankDrive(-self.leftStick.getY(), self.rightStick.getY())

        limit = self.limitSwitch.get()

        if self.coStick.getRawButton(1):
            self.elevatorMotor.set(-self.coStick.getY(-.01))

        if self.coStick.getRawButton(6):
            self.climbMotor.set(-1)

        elif self.coStick.getRawButton(4):
            self.climbMotor.set(1)

        else:
            self.climbMotor.set(0)

        if self.coStick.getRawButton(10):
            self.stagerMotor.set(1)

        elif self.coStick.getRawButton(9):
            self.stagerMotor.set(-1)

        else:
            self.stagerMotor.set(0)

        if self.coStick.getRawButton(12):
            self.frontshootMotor.set(1)

        elif self.coStick.getRawButton(11):
            self.frontshootMotor.set(-1)

        else:
            self.frontshootMotor.set(0)

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

        if self.coStick.getRawButton(4) == True and limit == True:
            self.climbMotor.set(0)


if __name__ == '__main__':
    wpilib.run(MyRobot)
