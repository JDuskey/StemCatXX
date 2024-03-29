import magicbot
from components import ShooterControl, ReverseShooterControl
import wpilib
from wpilib.drive import DifferentialDrive
from networktables import NetworkTables



class MyRobot(magicbot.MagicRobot):
    shooter_control = ShooterControl.ShooterControl
    reverse_shooter_control = ReverseShooterControl.ReverseShooterControl
    sd = NetworkTables.getTable('SmartDashboard')
    use_teleop_in_autonomous = True
    kp = .1
    drivekP = 1.23

#All Items used in code

    def createObjects(self):
        self.stager_used = False
        # self.pdp = wpilib.PowerDistributionPanel()
        self.reverse_stager_used = False
        self.leftStick = wpilib.Joystick(0)
        self.rightStick = wpilib.Joystick(1)
        self.ll = NetworkTables.getTable("limelight")
        self.controlPanel = wpilib.Joystick(5)
        self.leftMotor = wpilib.Victor(0)
        self.rightMotor = wpilib.Victor(1)
        self.climbMotor = wpilib.Victor(2)
        self.stagerMotor = wpilib.Victor(3)
        self.frontShooterMotor = wpilib.Victor(9)
        self.elevatorMotor = wpilib.Victor(6)
        self.elevatorMotor.setInverted(True)
        self.shooterTiltMotor = wpilib.Victor(7)
        self.myRobot = DifferentialDrive(self.leftMotor, self.rightMotor)
        self.climbMotor.setInverted(True)
        self.stagerMotor.setInverted(True)
        self.punchers = wpilib.DoubleSolenoid(0, 0, 1)
        self.skis = wpilib.DoubleSolenoid(4, 5)
        self.launcherRotate = wpilib.AnalogInput(0)
        self.climbLimitSwitch = wpilib.DigitalInput(8)
        self.climb_raise_limitswitch = wpilib.DigitalInput(4)
        self.ball_center = wpilib.DigitalInput(9)
        self.elevator_limit = wpilib.DigitalInput(7)
        self.pins = wpilib.DoubleSolenoid(2,3)
        self.pins.set(2)
        self.tilt_limit = wpilib.DigitalInput(6)
        self.tilt_controller = wpilib.PIDController(2,0,0, self.launcherRotate, self.shooterTiltMotor)
        #                 #Practice bot(2,0,0)
        #                 #Comp bot(3.66,0,0)
        self.tilt_controller.setOutputRange(-1,.5)
        self.tilt_controller.setPercentTolerance(5)
        self.elevator_encoder = wpilib.Encoder(0, 1)
        self.elevator_controller = wpilib.PIDController(.0025, 0, .001, self.elevator_encoder, self.elevatorMotor)
        #                 #practice bot(0.008,0,0.005)
        #                #Comp bot(.0025,0,.001)
        self.elevator_controller.setOutputRange(-1,.44)
        self.elevator_controller.setPercentTolerance(10)
        self.gears = wpilib.DoubleSolenoid(6,7)
        self.tilt_disabled = True
        self.punchers.set(2)
        self.skis.set(2)
        self.oldtx = 0
        self.gears.set(1)
        self.tilt_disabled = True
        self.controlPanel.setOutputs(False)
        self.color_sensor_left = wpilib.DigitalInput(3)
        self.color_sensor_mid = wpilib.DigitalInput(5)
        self.color_sensor_right = wpilib.DigitalInput(2)
        self.ultra = wpilib.AnalogInput(1)



    def teleopInit(self):
        #runs at the beginning of teleop
        pass
    def teleopPeriodic(self):
        #main teleop code
        targethistory = []
        targettotal = 0
        targetcount = 0
        # vision tracking variables
        for t in targethistory:
            targetcount += 1
            targettotal += t
        if targetcount > 10:
            targethistory=[]
        if targetcount == 0:
            targetcount = 1
        if self.elevator_controller.onTarget():
            self.controlPanel.setOutput(2, True)
        else:
            self.controlPanel.setOutput(2, False)
        tx = self.ll.getNumber("tx", 0)
        ta = self.ll.getNumber("ta", 0)
        ta = -ta




        if self.controlPanel.getRawButton(14):
            # co pilot intake
            if self.ball_center.get() == True:
                        self.stager_used = True
                        self.frontShooterMotor.set(-.7)
                        self.stagerMotor.set(-.2)#-.2
            else:
                if not self.reverse_shooter_control.running():
                    if not self.reverse_stager_used:
                        if not self.leftStick.getRawButton(4) == True or not self.leftStick.getRawButton(6) == True:
                            self.stagerMotor.set(0)
                            self.frontShooterMotor.set(0)
        else:
            self.stager_used = False
            if self.shooter_control.running() or self.reverse_shooter_control.running() or self.reverse_stager_used:
                pass
            else:
                if not self.leftStick.getRawButton(4) == True or not self.leftStick.getRawButton(6) == True:
                    self.frontShooterMotor.set(0)
                    self.stagerMotor.set(0)

        if self.leftStick.getRawButton(4):
            #ground intake
            if self.ball_center.get() == True:
                        self.stager_used = True
                        self.frontShooterMotor.set(.9)
                        self.stagerMotor.set(1)#-.2


        if self.leftStick.getRawButton(6):

            if self.ball_center.get() == True:
                        self.stager_used = True
                        self.frontShooterMotor.set(-.9)
                        self.stagerMotor.set(-.8)#-.2



        if self.rightStick.getRawButton(3):
            self.ll.putNumber('pipeline', 0)
            tv = self.ll.getNumber('tv', 0)
            tx = tx - 1.5
            if tv > 0:
                if self.ball_center.get() == True:
                    self.stager_used = True
                    self.frontShooterMotor.set(-.9)
                    self.stagerMotor.set(-.8)  # -.2
                steering_adjust = self.kp * tx
                distance_adjust = self.drivekP * (1.2 - ta)
                if distance_adjust > .9:
                    distance_adjust = .9
                if ta >= 1.21:
                    self.tilt_controller.setSetpoint(3.4)
                    self.ll.putNumber('pipeline',1)
                self.myRobot.arcadeDrive(distance_adjust, steering_adjust)


        elif self.rightStick.getRawButton(5):
            self.ll.putNumber('pipeline', 0)
            tv = self.ll.getNumber('tv', 0)
            tx = tx -.03

            if tx > (targettotal / targetcount) + 3:
                pass
            elif tx < (targettotal / targetcount) - 3:
                pass
            targethistory.append(tx)

            if tv > 0:
                steering_adjust = self.kp * tx
                distance_adjust = self.drivekP * (1.2 - ta)

                if distance_adjust > .65:
                    distance_adjust = .65

                if ta <= -2.8:
                    self.myRobot.arcadeDrive(0,0)
                else:
                    self.myRobot.arcadeDrive(distance_adjust, steering_adjust)

        elif self.rightStick.getRawButton(4):
            self.drivekP = .8
            self.ll.putNumber('pipeline', 0)
            tv = self.ll.getNumber('tv', 0)
            if tx > (targettotal / targetcount) + 4:
                pass
            elif tx < (targettotal / targetcount) - 4:
                pass
            targethistory.append(tx)
            if tv > 0:
                steering_adjust = self.kp * tx -.03
                distance_adjust = self.drivekP

                if distance_adjust > .65:
                    distance_adjust = .65


                self.myRobot.arcadeDrive(distance_adjust, steering_adjust)
        else:
            self.ll.putNumber('pipeline', 1)
            self.myRobot.tankDrive(-self.leftStick.getY(), -self.rightStick.getY())

        if self.leftStick.getRawButton(1):
            self.myRobot.arcadeDrive(.5,.1)


        if not self.controlPanel.getRawButton(5):
            if self.elevator_controller.isEnabled():
                self.elevator_controller.disable()
            if self.controlPanel.getY() > 0:
                self.elevatorMotor.set(self.controlPanel.getY() * -1)
            else:
                if self.elevator_limit.get() == False:
                    self.elevatorMotor.set(self.controlPanel.getY() * -.4)
                else:
                    self.elevatorMotor.set(0)

        if self.elevator_limit.get():
            self.elevator_encoder.reset()

        if not self.controlPanel.getRawButton(8):
            self.controlPanel.setOutput(3, False)
            if self.tilt_disabled == False:
                self.tilt_disabled = True
                self.tilt_controller.disable()
            if self.controlPanel.getX() > 0:
                self.shooterTiltMotor.set(self.controlPanel.getX() * -.6)
            else:
                if self.tilt_limit.get() == False:
                    self.shooterTiltMotor.set(self.controlPanel.getX() * -.5)

        if self.controlPanel.getRawButton(8):
            self.controlPanel.setOutput(3, True)
            if self.tilt_disabled == True:
                self.tilt_controller.enable()
                self.tilt_disabled = False
                self.tilt_controller.setSetpoint(self.launcherRotate.getAverageVoltage())


        if self.controlPanel.getRawButton(7):
            self.tilt_controller.disable()
            self.shooterTiltMotor.set(.65)

        if self.tilt_limit.get() == True:
            self.shooterTiltMotor.set(0)


        if self.controlPanel.getRawButton(13):
            if self.controlPanel.getRawButton(8):
                self.tilt_disabled = False
                self.tilt_controller.enable()
                self.tilt_controller.setSetpoint(3.4)

        if self.controlPanel.getRawButton(12):
            if self.controlPanel.getRawButton(8):
                self.tilt_disabled = False
                self.tilt_controller.enable()
                self.tilt_controller.setSetpoint(2.35)#2.49 comp

        if self.controlPanel.getRawButton(9):
             if not self.climb_raise_limitswitch.get():
                 self.climbMotor.set(1)
        elif self.controlPanel.getRawButton(10):
            if not self.climbLimitSwitch.get():
                self.climbMotor.set(-1)
        else:
            self.climbMotor.set(0)

        if self.climbLimitSwitch.get():
            self.climbMotor.set(0)

        if self.controlPanel.getRawButton(16):
            self.shooter_control.fire()
        if self.controlPanel.getRawButton(11):
            self.reverse_shooter_control.fire()

        if self.controlPanel.getRawButton(5):
            self.controlPanel.setOutput(1, True)
        else:
            self.controlPanel.setOutput(1, False)

        if self.controlPanel.getRawButton(4):
            if self.controlPanel.getRawButton(5):
                self.elevator_controller.enable()
                if not self.controlPanel.getRawButton(3):
                    self.elevator_controller.setSetpoint(-725)
                else:
                    self.elevator_controller.setSetpoint(5)

        if self.controlPanel.getRawButton(2):
            if self.controlPanel.getRawButton(5):
                self.elevator_controller.enable()
                if not self.controlPanel.getRawButton(3):
                    self.elevator_controller.setSetpoint(-3040)
                else:
                    self.elevator_controller.setSetpoint(-2494)

        # wpilib.DriverStation.reportWarning(str(self.launcherRotate.getVoltage()), False)

        if self.controlPanel.getRawButton(1):
            if self.controlPanel.getRawButton(5):
                self.elevator_controller.enable()
                if not self.controlPanel.getRawButton(3):
                    self.elevator_controller.setSetpoint(-5340)  ##5360 comp, 5320 practice##
                else:
                    self.elevator_controller.setSetpoint(-4843)


        if self.controlPanel.getRawButton(6):
            if self.controlPanel.getRawButton(5):
                self.elevator_controller.enable()
                self.elevator_controller.setSetpoint(-2100)

        if self.controlPanel.getRawButton(15):
            if self.controlPanel.getRawButton(5):
                self.elevator_controller.enable()
                self.elevator_controller.setSetpoint(-3200)


        if self.leftStick.getTrigger():
            self.punchers.set(2)
        else:
            self.punchers.set(1)

        if self.leftStick.getRawButton(12):
            self.skis.set(2)
        if self.leftStick.getRawButton(11):
            self.skis.set(1)

        if self.rightStick.getTrigger():
            self.gears.set(2)
        if self.rightStick.getRawButton(2):
            self.gears.set(1)

        if self.leftStick.getRawButton(7):
            self.pins.set(1)
        if self.leftStick.getRawButton(8):
            self.pins.set(2)

        # if self.pdp.getCurrent(15) > 2:
        #     self.tilt_controller.disable()
        #     self.ti.set(0)
if __name__ == '__main__':
    wpilib.run(MyRobot)
