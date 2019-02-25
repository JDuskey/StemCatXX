import wpilib
class Loader:
    frontShooterMotor = wpilib.Victor
    ball_center = wpilib.DigitalInput
    shoot_speed = -1.0

    def __init__(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def execute(self):
        if self.enabled and self.ball_center == True:
            self.frontShooterMotor.set(self.shoot_speed)
        else:
            self.frontShooterMotor.set(0)
        self.enabled = False