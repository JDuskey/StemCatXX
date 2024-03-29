from magicbot import StateMachine, state, timed_state
import wpilib
import time
class ReverseShooterControl(StateMachine):
    frontShooterMotor = wpilib.Victor
    stagerMotor = wpilib.Victor
    isrunning = False


    def fire(self):
        self.isrunning = True
        self.engage()

    def running(self):
        return self.isrunning

    @timed_state(first=True, duration= 0,next_state='firing', must_finish=True)
    def spin_up_shooter(self):
        self.frontShooterMotor.set(1)

    @timed_state(duration=2, next_state='end', must_finish=True)
    def firing(self):
        self.stagerMotor.set(.4)

    @timed_state(duration=.4,must_finish=True)
    def end(self):
        self.isrunning = False
        self.frontShooterMotor.set(0)
        self.stagerMotor.set(0)

