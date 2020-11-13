import sys
from python_freeipa import exceptions
from st2common.runners.base_action import Action
from python_freeipa import ClientMeta


class ChangePassword(Action):
    def run(self):
        return(True)
