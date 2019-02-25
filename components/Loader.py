from magicbot import StateMachine, state, timed_state
import wpilib
class Loader(StateMachine):
    frontShooterMotor = wpilib.Victor
    ball_center = wpilib.DigitalInput
    is_running = False
    def check_for_ball(self):
        if not self.ball_center.get():
            return True
        else:
            return False

    def stop(self):
        self.frontShooterMotor.set(0)
        self.is_running = False
    def running(self):
        return self.is_running
    def load(self):
        self.engage()
        self.is_running = True
    @state(first=True)
    def load_ball(self):
        self.frontShooterMotor.set(-1)
        if self.check_for_ball():
            self.next_state_now('end')

    @timed_state(duration=.1,must_finish=True)
    def end(self):
        self.frontShooterMotor.set(0)
        self.is_running = False


