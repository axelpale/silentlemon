# Light control abstraction
import requests

class Lights:
    
    ## Turn on selected lights
    def setLights(self, colorX, colorY, level, deviceId=-1):
        ## Set parameters
        colorX = int(colorX*32768)
        colorY = int(colorY*32768) 
        
        ## If deviceID is 1,2,3 then set it, otherwise leave it from the parameters and all of the lights are set
        if (deviceId == 0 or deviceId == 3 or deviceId == 8 ):
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