class Transition:
    def __init__(self, condition, destination):
        if type(condition).__name__ != 'function':
           raise ValueError('condition must be a function')
        self.condition = condition
        if isinstance(destination, str):
            self.destination = destination
        elif isinstance(destination, State):
            self.destination = destination.name
        else:
           raise ValueError('destination must be a str or State')

class State:
    def __init__(self, name, init=False, start=None, update=None, transitions=[]):
        self.name = name
        self.is_init = init
        self.start_func = start
        self.update_func = update
        self.transitions = transitions

class StateMachine:
    def __init__(self, states):
        self.states = states
        self.start_state = None
        self.running_state = None

        for state in self.states:
            if state.is_init and self.start_state != None:
                raise ValueError('multiple init States')
            if state.is_init:
                self.start_state = state
        if self.start_state == None:
            raise ValueError('no init State')
        self.activate_state(self.start_state.name)

    def activate_state(self, state_name):
        for state in self.states:
            if state.name == state_name:
                self.running_state = state
                if self.running_state.start_func != None:
                    self.running_state.start_func()

    def _tick(self):
        if self.running_state != None:
            if self.running_state.update_func != None:
                self.running_state.update_func()
            if len(self.running_state.transitions) > 0:
                for transition in self.running_state.transitions:
                    if transition.condition():
                        new_state = transition.destination
                        self.activate_state(new_state)
