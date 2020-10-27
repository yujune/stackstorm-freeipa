from datetime import datetime
from python_freeipa import ClientMeta

def get_expired_timeleft(self,expired_date):

  if expired_date is None:
    daysleft = 999

  else:
    
    expired_date = expired_date[0].get('__datetime__')
  
    today = datetime.now()    # get the current time (datetime object)
    today = datetime.strftime(today, '%Y%m%d%H%M%SZ')    # convert the current time to string with the specified format, parameter of strftime must be obj
    today = datetime.strptime(today, '%Y%m%d%H%M%SZ')    # convert the current time back to datetime object in order to do substraction. Parameter of strptime must be str
    expired_date = datetime.strptime(expired_date, '%Y%m%d%H%M%SZ')    # convert expired_date to datetime object for substraction 
    timeleft = expired_date - today    # get the remaining password effective time
    daysleft = timeleft.days           # get the remaning days

  return daysleft

def freeipa_login(self):
  freeipa_account = self.config.get('freeipa_account', None)
  
  if freeipa_account is None:
    raise ValueError('"freeipa_account" config value is required to login as admin')

  client = ClientMeta(freeipa_account['link_address'],verify_ssl=False)
  client.login(freeipa_account['admin_id'], freeipa_account['admin_password'])

  return client

