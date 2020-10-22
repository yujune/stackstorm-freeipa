from datetime import datetime

def get_expired_timeleft(self,expired_date):
  today = datetime.now()    # get the current time (datetime object)
  today = datetime.strftime(today, '%Y%m%d%H%M%SZ')    # convert the current time to string with the specified format, parameter of strftime must be obj
  today = datetime.strptime(today, '%Y%m%d%H%M%SZ')    # convert the current time back to datetime object in order to do substraction. Parameter of strptime must be str
  expired_date = datetime.strptime(expired_date, '%Y%m%d%H%M%SZ')    # convert expired_date to datetime object for substraction 
  timeleft = expired_date - today    # get the remaining password effective time
  daysleft = timeleft.days           # get the remaning days
  return daysleft
