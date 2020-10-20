import eventlet

from st2reactor.sensor.base import Sensor
from python_freeipa import ClientMeta

class SensorPassword(Sensor):

  def __init__(self, sensor_service, config):
    super(SensorPassword, self).__init__(sensor_service=sensor_service, config=config)
    self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
    self._stop = False

  def setup(self):
  
    client = ClientMeta('tst-freeipa-master.cirosolution.com',verify_ssl=False)
    client.login('admin', 'asdf1234password')
    # user = client.user_show('ahjune')
    # all_user = client.user_find('ahjune')
    # print(all_user)
    # print(user.get('result',None).get('krbpasswordexpiration',None)[0].get('__datetime__',None))

    #---------------- get all user id, mail and password expiration date -------------------
    all_users = client.user_find()
    total_users = all_users.get('count', 0)    # get the total number of users from the freeipa
    print('Total users: ' + str(total_users)) 
    i = 1
    while i<= total_users:
      current_user = all_users.get('result',None)[i-1]    # get the a current user in the list
      user_id = current_user.get('uid','no id')                  # get the current user id
      encoded_id = user_id[0]
      print('User ID: ' + encoded_id)
       
      user_email = current_user.get('mail','no email')            # get the current user email
      encoded_email = user_email[0]
      print('User email: ' + encoded_email)

      user_password_expiration_date = current_user.get('krbpasswordexpiration','199910102211Z')[0]    # get the current user's password expiration date and time
      print(user_password_expiration_date) 
      user_name = current_user.get('cn','no name')                # get the current user name
      encoded_name = user_name[0]
      print('User name: ' + encoded_name)
      #print(str(i) + ") ID: " + user_id + "\n Name: " + user_name + "\n Email: " + user_email + "\n Password Expiration Date: " +' user_password_expiration_date' + "\n")
      i += 1

  def run(self):
      while not self._stop:
          self._logger.debug('Dispatchng the trigger....')
          # count = self.sensor_service.get_value('hello_st2.count') or 0
          payload = {'expired_date':'today'}
          self.sensor_service.dispatch(trigger='freeipa.expired_event', payload=payload)
          # self.sensor_service.set_value('hello_st2.count', payload['count'])
          eventlet.sleep(60)

  def cleanup(self):
      self._stop = True

    # Methods required for programmable sensors.
  def add_trigger(self, trigger):
      pass

  def update_trigger(self, trigger):
      pass

  def remove_trigger(self, trigger):
      pass

