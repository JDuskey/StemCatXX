import magicbot
import wpilib
from wpilib.drive import DifferentialDrive
from networktables import NetworkTables

class MyRobot(magicbot.MagicRobot):

    def createObjects(self):
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.coStick = wpilib.Joystick(2)
        self.stagerMotor = wpilib.Victor(3)
        self.frontshootMotor= wpilib.Victor(4)
        self.rearshootMotor = wpilib.Victor(5)
        self.shooterRotateMotor = wpilib.Victor(7)
        self.shooterPivotMotor = wpilib.Victor(8)
        self.climbMotor = wpilib.Victor(2)
        self.elevatorMotor = wpilib.Victor(6)
        self.leftMotor = wpilib.Victor(0)
        self.rightMotor = wpilib.Victor(1)
        self.myRobot = DifferentialDrive(self.leftMotor, self.rightMotor)
        self.ultra = wpilib.AnalogInput(0)
        self.data = NetworkTables.getTable("SmartDashboard")
        self.gyro = wpilib.AnalogGyro(1)
        self.pdp = wpilib.PowerDistributionPanel(0)
        self.gyro.reset()

    def teleopInit(self):
        stage_speed = self.data.putNumber("StageSpeed",0)
        front_speed = self.data.putNumber("FrontSpeed",0)
        rear_speed = self.data.putNumber("RearSpeed",0)
        active = self.data.putBoolean("Activator",False)


    def teleopPeriodic(self):
        self.myRobot.tankDrive(-self.leftStick.getY(), -self.rightStick.getY())
        self.elevatorMotor.set(self.coStick.getY())
        ultra_value = self.ultra.getVoltage()
        ultra_mv = ultra_value*1000
        ultra_mm = (ultra_mv/4.883) * 5
        ultra_ft = (ultra_mm/304.8)
        self.data.putNumber("Ultrasonic", ultra_ft)
        self.data.putString("Distance","{feet} feet".format(feet=ultra_ft))
        stage_speed = self.data.getNumber("StageSpeed",0)
        front_speed = self.data.getNumber("FrontSpeed",0)
        rear_speed = self.data.getNumber("RearSpeed",0)
        self.stagerMotor.set(stage_speed)
        self.rearshootMotor.set(rear_speed)
        self.frontshootMotor.set(front_speed)
        if self.coStick.getRawButton(8):
            self.climbMotor.set(1)

        elif self.coStick.getRawButton(7):
            self.climbMotor.set(-1)

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

        if self.coStick.getRawButton(1):
            self.rearshootMotor.set(1)

        elif self.coStick.getRawButton(2):
            self.rearshootMotor.set(-1)

        else:
             self.rearshootMotor.set(0)

        wpilib.DriverStation.reportWarning(str(ultra_ft),False)


if __name__ == '__main__':
	wpilib.run(MyRobot)
