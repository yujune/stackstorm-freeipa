import sys

from st2common.runners.base_action import Action

class ChangePassword(Action):
  def run(self, passw_daysleft):
    print(" Your password is going to be expired in " + str(passw_daysleft) + " days.")  
    return(True, "Succesfully executed action")
