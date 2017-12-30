from datetime import datetime
import time
start=datetime.now()
print start
time.sleep(5)
later=datetime.now()
print later
print (later-start).total_seconds()
