# Business logic

import time
import datetime
import threading
from math import floor
from calendar_api import Calendar

MINUTE = 60
HOUR = 60 * MINUTE
TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

DEFAULT_SETTING = {
    'start': {
        'fade_sec': 10,
        'color_x': 0,
        'color_y': 0,
        'level': 100,
        'devices': [3]
    },
    'end': {
        'fade_sec': 10,
        'color_x': 0,
        'color_y': 0,
        'level': 100,
        'devices': [3]
    }
}

KEYWORD_SETTING_MAP = {
  'quick': {
    'start': {
      'offset_sec': -HOUR / 2,
      'fade_sec': 10,
      'color_x': 0,
      'color_y': 0,
      'level': 100,
      'devices': [3]
    },
    'end': {
      'fade_duration': 1234,
      'level': 0
    }
  },
  'creative': DEFAULT_SETTING,
  'relaxed': DEFAULT_SETTING,
  'tasty': {
    'offset_sec': -HOUR / 2,
    'fade_sec': 10,
    'color_x': 0,
    'color_y': 0,
    'level': 100,
    'devices': [3]
  }
}


def find_setting(ev):
    wordlist = ev['description'].split()
    for word in wordlist:
        if word in KEYWORD_SETTING_MAP:
            return KEYWORD_SETTING_MAP[word]
    return DEFAULT_SETTING

def schedule(light_calls, from_time):
    #print(time.ctime())

    if len(light_calls) == 0:
        return

    first = light_calls[0]
    delta_seconds = first['at_time'] - from_time
    # Make quick
    dt = delta_seconds / 1000.0

    print(first['type'] + ' ' + first['event']['description'] + ', ' + str(dt) + 's')

    threading.Timer(dt, schedule, [light_calls[1:], first['at_time']]).start()

def main():
    cal = Calendar()
    evs = cal.get_upcoming_events()
    light_calls = []

    for ev in evs:
        light_setting = find_setting(ev)
        start_epoch = datetime.datetime.strptime(ev['start'], TIME_FORMAT)
        end_epoch = datetime.datetime.strptime(ev['end'], TIME_FORMAT)
        light_calls.append({
            'at_time': start_epoch.timestamp(),
            'event': ev,
            'type': 'start',
            'setting': light_setting['start']
        })
        light_calls.append({
            'at_time': end_epoch.timestamp(),
            'event': ev,
            'type': 'end',
            'setting': light_setting['end']
        })

    #print(light_calls)
    now_epoch = time.time()
    schedule(light_calls, now_epoch)
    #print(evs[0]['start'])

if __name__ == "__main__":
    main()
