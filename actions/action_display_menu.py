import sys
from st2common.runners.base_action import Action


class DisplayMenu(Action):
    def run(self):
        return(True, "Hello!")
