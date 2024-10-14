from character import Character


class Script:
    """
    The script that contains the commands that controll the character.
    """
    def __init__(self, character):
        """
        Parameters
        ----------
        character : Character
        The character that the script controls.
        """
        self.character = character
        self.funcs = []
        self.current_func = None
        self.executing = False
        self.executed = False

    def set_script(self, script):
        """
        Sets the script to be executed.
        Parameters
        ----------
        script : list
        The list of functions that will be executed.
        """
        self.funcs = script

    def start(self):
        """
        Starts the execution of the script.
        """
        if not self.executed:
            self.executed = True
            self.executing = True
            if self.funcs:
                self.current_func = self.funcs.pop(0)

    def update(self):
        """
        Once the script is being executed, it updates the character.
        """
        # If a func is active, execute it
        if self.executing and self.current_func:
            action_done = self.current_func()
            if action_done:
                self.current_func = None
                # Move to the next func if available
                if self.funcs:
                    self.current_func = self.funcs.pop(0)
                else:
                    self.executing = False
