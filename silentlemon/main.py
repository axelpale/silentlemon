# Business logic

import time
import threading
from calendar_api import Calendar

def schedule():
    print(time.ctime())
    threading.Timer(10, schedule).start()

def main():
    cal = Calendar()
    evs = cal.get_upcoming_events()


    #schedule()
    #print(evs[0]['start'])

if __name__ == "__main__":
    main()
