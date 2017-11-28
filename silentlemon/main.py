# Business logic

import time
import datetime
import threading
import copy
from math import floor
from calendar_api import Calendar
from lights import Lights

MINUTE = 60
HOUR = 60 * MINUTE
TIME_FORMAT = '%Y-%m-%dT%H:%M:%SZ'

DEVICE = 8

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
      'color_x': 0.25,
      'color_y': 0.08,
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
      'level': 0,
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

    dtime = datetime.datetime.fromtimestamp(lc['at_time']) + datetime.timedelta(hours=2)

    print(dtime.strftime('%H:%M') + ' ' + lc['event']['description'] + ' / ' + lc['type'] + ' @ ' + str(dt) + 's')

    for device_id in setting['devices']:
        x = setting['color_x']
        y = setting['color_y']
        l = setting['level']
        light_api.setLights(x, y, l, device_id)
        print('  Device {0}: ({1}, {2}) {3}%'.format(device_id, x, y, l))

def schedule(light_call):
    now_time = 1511668000  # sunday morning 7:30 AM in finland 2017-11-26
    delta_seconds = light_call['at_time'] - now_time
    # Make quick
    dt = delta_seconds / 400.0

    if dt > 0:
        threading.Timer(dt, call_light, [light_call, dt]).start()
    #else:
    #    print('skip')
    #    print(light_call)

def main():
    cal = Calendar()
    evs = cal.get_upcoming_events(20)
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
        dim_setting = copy.copy(light_setting['start'])
        dim_setting['level'] = floor(dim_setting['level'] / 2)
        light_calls.append({
            'at_time': end_epoch.timestamp() - 30 * 60,
            'event': ev,
            'type': 'dim',
            'setting': dim_setting
        })
        light_calls.append({
            'at_time': end_epoch.timestamp() - 20 * 60,
            'event': ev,
            'type': 'postdim',
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
