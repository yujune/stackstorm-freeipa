import sys
from python_freeipa import ClientMeta
from st2common.runners.base_action import Action
from datetime import datetime
from sharedcode import get_expired_timeleft
from sharedcode import freeipa_login

class ShowUserInfo(Action):
  def run(self, user_id):
    
    client = freeipa_login(self)
 
    user = client.user_find(o_uid= user_id).get('result', None)[0]
    name = user.get('cn', '-')[0]
    email = user.get('mail', '-')[0]
    password_expired_date = user.get('krbpasswordexpiration', None)
  
    pwd_daysleft = get_expired_timeleft(self, password_expired_date)
    
    if pwd_daysleft == 999 :
      password_expired_date = "Permanent Password"
    else:
      password_expired_date = password_expired_date[0].get('__datetime__')

      password_expired_date = datetime.strptime(password_expired_date, '%Y%m%d%H%M%SZ')
      password_expired_date = datetime.strftime(password_expired_date, '%d-%b-%Y, %H:%M:%S')
        
    account_status = client.user_status(user_id).get('result', None)[0]
    password_failed_times = account_status.get('krbloginfailedcount', 0 )[0]
    password_last_failed_date = account_status.get('krblastfailedauth' , None)[0]

    if password_last_failed_date == 'N/A':
      password_last_failed_date = '-'

    else:
      password_last_failed_date = password_last_failed_date.get('__datetime__')

      password_last_failed_date = datetime.strptime(password_last_failed_date, '%Y%m%d%H%M%SZ')
      password_last_failed_date = datetime.strftime(password_last_failed_date, '%d-%b-%Y, %H:%M:%S')
   
    password_policy = client.pwpolicy_show(o_user= user_id).get('result', None)
    max_password_failure = password_policy.get('krbpwdmaxfailure', 0)[0]
    chances_left = int(max_password_failure) - int(password_failed_times)
    
    accoount_status = 'Unlock'
  
    if password_failed_times < max_password_failure:
      
      account_status = 'Active'
    
    else:
      account_status = 'Permanent Locked'
    
    output = \
    '\n-------------------- Account Status -----------------------\n\n' \
    'User Name                  : ' + name + '\n\n' \
    'Account Status             : ' + account_status + '\n\n' \
    'Failed Password Attempted  : ' + password_failed_times + '\n\n' \
    'Last Failed Attempted      : ' + str(password_last_failed_date) + '\n\n' \
    'Password Expired Date      : ' + str(password_expired_date) + '\n\n' \
    'Password Valid Days        : ' + str(pwd_daysleft) + '\n\n\n' \
    'Max failure is ' + max_password_failure + ' times. You have '+ str(chances_left) +' chances left.\n\n' \
    '\n-------------------- Account Status -----------------------\n'

    print('\n-------------------- Account Status -----------------------\n')
    print('User Name                  : ' + name + '\n')
    print('Account Status             : ' + account_status + '\n')
    print('Failed Password Attempted  : ' + password_failed_times + '\n')
    print('Last Failed Attempted      : ' + str(password_last_failed_date) + '\n')
    print('Password Expired Date      : ' + str(password_expired_date) + '\n')
    print('Password Valid Days        : ' + str(pwd_daysleft) + '\n')
    print('Max failure is ' + max_password_failure + ' times. You have '+ str(chances_left) +' chances left.\n')
    print('\n-------------------- Account Status -----------------------\n')

    client.logout()
    self.logger.info('Successfully log out')
    return(True, output)


