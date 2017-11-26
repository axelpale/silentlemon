# Light control abstraction
import requests

class Lights:

    def __init__(self):
        self._colorX = 0
        self._colorY = 0

    ## Turn on selected lights
    def setLights(self, colorX, colorY, level, deviceId=-1):
        ## Set parameters
        self._colorX = int(colorX*65536)
        self._colorY = int(colorY*65536)

        ## If deviceID is 0,3,8 then set it, otherwise leave it from the parameters and all of the lights are set
        if (deviceId == 0 or deviceId == 3 or deviceId == 8 ):
                payload = {'device': deviceId, 'level': level, 'colour_x': self._colorX, 'colour_y': self._colorY}
        else:
                payload = {'level': level, 'colour_x': self._colorX, 'colour_y': self._colorY}

        ## Send the request to change the lights
        request = requests.get('https://5nk8a0rfn5.execute-api.eu-west-1.amazonaws.com/v1/command', params=payload)

     ## Turn off all of the lights
    def lightsOff(self):
        ## Set the parameters
        level = 0 # 0-100

        ## Send the request to turn off the lights
        payload = {'level': level, 'colour_x': self._colorX, 'colour_y': self._colorY}
        request = requests.get('https://5nk8a0rfn5.execute-api.eu-west-1.amazonaws.com/v1/command', params=payload)
