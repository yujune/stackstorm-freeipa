import sys

from st2common.runners.base_action import Action
from python_freeipa import ClientMeta

class ChangePassword(Action):
  def run(self, user_id, old_password, new_password):
     
    freeipa_link = self.config.get('freeipa_account', None)['link_address']

    client = ClientMeta(freeipa_link, verify_ssl=False)
    client.login(user_id, old_password)

    client.change_password(user_id, new_password, old_password)

    return(True, "Password has been changed successfully")
