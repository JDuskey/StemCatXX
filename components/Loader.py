from magicbot import StateMachine, state, timed_state
import wpilib
class Loader(StateMachine):
    front_shooter_motor = wpilib.Victor
    rear_shooter_motor = wpilib.Victor
    stager_motor = wpilib.Victor
    ball_center = wpilib.DigitalInput
    coStick = wpilib.Joystick
    def check_for_ball(self):
        if not self.ball_center.get():
            return True
        else:
            return False

    def stop(self):
        self.shooter_motor.set(0)
    def load(self):
        self.engage()

    @state(first=True)
    def load_ball(self):
        self.shooter_motor.set(-.5)
        if self.check_for_ball():
            self.next_state_now('end')

    @timed_state(duration=.1,must_finish=True)
    def end(self):
        self.shooter_motor.set(0)


