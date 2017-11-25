# Business logic

import time
import datetime
import threading
from math import floor
from calendar_api import Calendar
from lights import Lights

MINUTE = 60
HOUR = 60 * MINUTE
TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

DEVICE = 3

DEFAULT_SETTING = {
    'start': {
        'fade_sec': 10,
        'color_x': 0.3,
        'color_y': 0.3,
        'level': 150,
        'devices': [DEVICE]
    },
    'end': {
        'fade_sec': 10,
        'color_x': 0.3,
        'color_y': 0.3,
        'level': 0,
        'devices': [DEVICE]
    }
}

KEYWORD_SETTING_MAP = {
  'energizing': {
    'start': {
      'offset_sec': -HOUR / 2,
      'fade_sec': 10,
      'color_x': 0.25,
      'color_y': 0.08,
      'level': 200,
      'devices': [DEVICE]
    },
    'end': {
      'color_x': 0.25,
      'color_y': 0.08,
      'level': 100,
      'devices': [DEVICE]
    }
  },
  'happy': {
    'start': {
      # Easter
      'color_x': 0.2,
      'color_y': 0.5,
      'level': 200,
      'devices': [DEVICE]
    },
    'end': {
      'color_x': 0.3,
      'color_y': 0.3,
      'level': 50,
      'devices': [DEVICE]
    }
  },
  'relaxed': DEFAULT_SETTING,
  'tasty': {
    'start': {
        'color_x': 0,
        'color_y': 0,
        'level': 100,
        'devices': [DEVICE]
    },
    'start': {
        'color_x': 0,
        'color_y': 0,
        'level': 100,
        'devices': [DEVICE]
    }
  }
}

light_api = Lights()

def find_setting(ev):
    wordlist = ev['description'].split()
    smallcaps = map(lambda x: x.lower(), wordlist)

    for word in smallcaps:
        if word in KEYWORD_SETTING_MAP:
            return KEYWORD_SETTING_MAP[word]
    return DEFAULT_SETTING

def call_light(lc, dt):
    '''
    lc light call
    '''
    setting = lc['setting']

    print(lc['type'] + ' ' + lc['event']['description'] + ' @' + str(dt) + 's')

    for device_id in setting['devices']:
        x = setting['color_x']
        y = setting['color_y']
        l = setting['level']
        light_api.setLights(x, y, l, device_id)
        print('  Device {0}: ({1}, {2}) {3}%'.format(device_id, x, y, l))

def schedule(light_call):
    now_time = 1511674500
    delta_seconds = light_call['at_time'] - now_time
    # Make quick
    dt = delta_seconds / 1000.0

    if dt > 0:
        threading.Timer(dt, call_light, [light_call, dt]).start()

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

    for light_call in light_calls:
        schedule(light_call)

if __name__ == "__main__":
    main()
