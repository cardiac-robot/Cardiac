import qi

class BehaviorManager(object):
    def __init__(self, robot):
        #load robot
        self.Robot = robot
        #call nao behavior manager
        self.behavior = self.Robot.session.service("ALBehaviorManager")
        #create behavior dictionary container
        self.BehaviorContainer = {}
        #definde initial robot State
        self.State = "autonomous"

    def load_behaviors(self):
        self.BehaviorContainer['welcome'] = self.welcome_behavior
