import eventlet
from datetime import datetime
from st2reactor.sensor.base import Sensor
from python_freeipa import ClientMeta

class SensorPassword(Sensor):

  def __init__(self, sensor_service, config):
    super(SensorPassword, self).__init__(sensor_service=sensor_service, config=config)
    self._logger = self.sensor_service.get_logger(name=self.__class__.__name__)
    self._stop = False
    self._client = ClientMeta('tst-freeipa-master.cirosolution.com',verify_ssl=False)

  def setup(self):
  
    self._client.login('admin', 'asdf1234password')
    # user = client.user_show('ahjune')
    # all_user = client.user_find('ahjune')
    # print(all_user)
    # print(user.get('result',None).get('krbpasswordexpiration',None)[0].get('__datetime__',None)
 
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
          
        user_email = current_user.get('mail','no email')            # get the current user email
        user_email = user_email[0]
        print('User email: ' + user_email)
          
        user_password_expiration_date = current_user.get('krbpasswordexpiration','199910102211Z')[0]    # get the current user's password expiration date and time
         
        if  user_password_expiration_date == '1':
          print('No Password has been set in this account')
        else:
          user_password_expiration_date = user_password_expiration_date.get('__datetime__')        # get the password expiration date
          
          timeleft = self.get_expired_timeleft(user_password_expiration_date)                      # calculate the effective password time left start from today 
          print('Time left:    ' + str(timeleft)) 
             
        user_name = current_user.get('cn','no name')                # get the current user name
        user_name = user_name[0]
        print('User name: ' + user_name+ "\n\n")
        #print(str(i) + ") ID: " + user_id + "\n Name: " + user_name + "\n Email: " + user_email + "\n Password Expiration Date: " +' user_password_expiration_date' + "\n")
        i += 1
      
      self._logger.debug('Dispatchng the trigger....')
      # count = self.sensor_service.get_value('hello_st2.count') or 0
      payload = {'user_id': user_id, 'user_name': user_name, 'user_email': user_email,'password_expiration':{'expired_date':expired_date,'expired_time':expired_time}}
      self.sensor_service.dispatch(trigger='freeipa.password_expired_event', payload=payload)
      # self.sensor_service.set_value('hello_st2.count', payload['count'])
      
      eventlet.sleep(60)

  def get_expired_timeleft(self,expired_date):
      today = datetime.now()    # get the current time (datetime object)
      today = datetime.strftime(today, '%Y%m%d%H%M%SZ')    # convert the current time to string with the specified format, parameter of strftime must be obj
      today = datetime.strptime(today, '%Y%m%d%H%M%SZ')    # convert the current time back to datetime object in order to do substraction. Parameter of strptime must be str
      expired_date = datetime.strptime(expired_date, '%Y%m%d%H%M%SZ')    # convert expired_date to datetime object for substraction 
      print("Expired Date: " + str(expired_date))
      print("Today: " + str(today))   
      timeleft = expired_date - today    # get the remaining password effective time
      return timeleft
      
  def cleanup(self):
      self._stop = True

    # Methods required for programmable sensors.
  def add_trigger(self, trigger):
      pass

  def update_trigger(self, trigger):
      pass

  def remove_trigger(self, trigger):
      pass

