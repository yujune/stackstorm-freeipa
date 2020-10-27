import eventlet
from datetime import datetime
from st2reactor.sensor.base import Sensor
from python_freeipa import ClientMeta
from sharedcode import get_expired_timeleft
from sharedcode import freeipa_login

class SensorPassword(Sensor):

  def __init__(self, sensor_service, config):
    super(SensorPassword, self).__init__(sensor_service=sensor_service, config=config)
    self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
    self._stop = False
    self._client = freeipa_login(self)

  def setup(self):
    pass
   
  def run(self):
    
    while not self._stop:
    #---------------- get all user id, mail and password expiration date -------------------
      all_users = self._client.user_find()
      total_users = all_users.get('count', 0)    # get the total number of users from the freeipa
      print('Total users: ' + str(total_users))
       
      i = 1
      while i<= total_users:
        current_user = all_users.get('result',None)[i-1]    # get the a current user in the list
        user_id = current_user.get('uid','no id')                  # get the current user id
        user_id = user_id[0]                                # initially is e.g. " {u "ahjune123"}, after put [0] become "ahjune"
        print('User ID: ' + user_id)
          
        user_email = current_user.get('personalmail','no email')            # get the current user email
        user_email = user_email[0]
        print('User email: ' + user_email)
          
        user_password_expiration_date = current_user.get('krbpasswordexpiration',None)    # get the current user's password expiration date and time
          
        daysleft = get_expired_timeleft(self, user_password_expiration_date)                      # calculate the effective password time left start from today 
          #secondsleft = timeleft.seconds
        print('Day(s) left: ' + str(daysleft))
             
        user_name = current_user.get('cn','no name')                # get the current user name
        user_name = user_name[0]
        print('User name: ' + user_name+ "\n\n")
 
        self._logger.debug('Dispatchng the trigger....')
        payload = {'user_id': user_id, 'user_name': user_name, 'user_email': user_email,'password_daysleft': int(daysleft)}
        self.sensor_service.dispatch(trigger='freeipa.password_expired_event', payload=payload)

        i += 1
      
      eventlet.sleep(86400)
      
  def cleanup(self):
      self._stop = True

    # Methods required for programmable sensors.
  def add_trigger(self, trigger):
      pass

  def update_trigger(self, trigger):
      pass

  def remove_trigger(self, trigger):
      pass

