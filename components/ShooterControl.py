from magicbot import StateMachine, state, timed_state
import wpilib
import time
class ShooterControl(StateMachine):
    front_shooter_motor = wpilib.Victor
    stager_motor = wpilib.Victor
    isrunning = False


    def fire(self):
        self.isrunning = True
        self.engage()

    def running(self):
        return self.isrunning

    @timed_state(first=True, duration=.4,next_state='firing', must_finish=True)
    def spin_up_shooter(self):
        self.front_shooter_motor.set(1)

    @timed_state(duration=1, next_state='end', must_finish=True)
    def firing(self):
        self.stager_motor.set(1)

    @timed_state(duration=.2,must_finish=True)
    def end(self):
        self.isrunning = False
        self.front_shooter_motor.set(0)
        self.stager_motor.set(0)

