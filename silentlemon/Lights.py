# Light control abstraction
import requests

class Lights:
    
    ## Turn on selected lights
    def lightsOn(self):
        ## Set parameters
        colorX = 0.2 # 0-1
        colorY = 0.2 # 0-1
        level = 100 # 0-100
        deviceId = 2 # Device 1, 2, 3 or empty is 'all'
        colorX = int(colorX*32768)
        colorY = int(colorY*32768) 
        
        ## If deviceID is 1,2,3 then set it, otherwise leave it from the parameters and all of the lights are set
        if (deviceId == 1 or deviceId == 2 or deviceId == 3 ):
                payload = {'device': deviceId, 'level': level, 'colour_x': colorX, 'colour_y': colorY}
        else:
                payload = {'level': level, 'colour_x': colorX, 'colour_y': colorY}
        
        ## Send the request to change the lights
        request = requests.get('https://5nk8a0rfn5.execute-api.eu-west-1.amazonaws.com/v1/command', params=payload)
        
     ## Turn off all of the lights   
    def lightsOff(self):
        ## Set the parameters
        colorX = 0 # 0-1
        colorY = 0 # 0-1
        level = 0 # 0-100
        
        ## Send the request to turn off the lights
        payload = {'level': level, 'colour_x': colorX, 'colour_y': colorY}
        request = requests.get('https://5nk8a0rfn5.execute-api.eu-west-1.amazonaws.com/v1/command', params=payload)
        