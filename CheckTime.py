from datetime import datetime, time
from pytz import timezone
now = datetime.now(timezone('US/Eastern'))
now_time = now.time()
def checktime():
    if now_time >= time(15,45):
        return True
    return False

print(checktime())
