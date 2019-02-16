import wpilib
class Shooter:
    shooter_motor = wpilib.Victor
    shoot_speed = 1.0

    def __init__(self):
        self.enabled = False

    def enable(self):
        self.enabled = True

    def execute(self):
        if self.enabled:
            self.shooter_motor.set(self.shoot_speed)
        else:
            self.shooter_motor.set(0)
        self.enabled = False