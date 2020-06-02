from datetime import datetime
from time import sleep
import urllib
import sys
import os

from onvif import ONVIFCamera

XMAX = 1
XMIN = -1
YMAX = 1
YMIN = -1

def perform_move(ptz, request, timeout):
    # Start continuous move
    request.timeout = timeout
    ptz.ContinuousMove(request)
    # Wait a certain time
    sleep(timeout)
    request.PanTilt = 1
    # Stop continuous move
    ptz.Stop(request)

def move_right(ptz, request, timeout):
    #print 'move right...'
    request.Velocity.PanTilt._x = XMAX
    request.Velocity.PanTilt._y = 0
    perform_move(ptz, request, timeout)

def move_left(ptz, request, timeout):
    #print 'move left...'
    request.Velocity.PanTilt._x = XMIN
    request.Velocity.PanTilt._y = 0
    perform_move(ptz, request, timeout)

def getNameInfo():
    data, time = str(datetime.now()).split()
    year, month, day = data.split('-')
    time, a = time.split('.')
    hour, minute, second = time.split(':')
    return year, month, day, hour, minute, second

def getPic():
    year, month, day, hour, minute, second = getNameInfo()
    nome = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '.jpg'
    myPath = "/home/joao.victor/photos2pos/"
    fullfilename = os.path.join(myPath, nome)

    URL = 'http://177.220.84.10/webcapture.jpg?command=snap&channel=1&user=admin&password=tlJwpbo6'
    urllib.urlretrieve(URL, fullfilename)

def continuous_move():
    mycam = ONVIFCamera('177.220.84.10', 8899, 'admin', '', '/home/joao.victor/.local/wsdl/')
    # Create media service object
    media = mycam.create_media_service()
    # Create ptz service object
    ptz = mycam.create_ptz_service()

    # Get target profile
    media_profile = media.GetProfiles()[0];

    # Get PTZ configuration options for getting continuous move range
    request = ptz.create_type('GetConfigurationOptions')
    request.ConfigurationToken = media_profile.PTZConfiguration._token
    ptz_configuration_options = ptz.GetConfigurationOptions(request)

    request = ptz.create_type('ContinuousMove')
    request.ProfileToken = media_profile._token

    ptz.Stop({'ProfileToken': media_profile._token})

    global XMAX, XMIN, YMAX, YMIN
    XMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Max
    XMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].XRange.Min
    YMAX = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Max
    YMIN = ptz_configuration_options.Spaces.ContinuousPanTiltVelocitySpace[0].YRange.Min
    
    timeout = 2.5
    
    #tira a foto e salva
    getPic()
    
    move_right(ptz, request, timeout)
    
    #tira a foto e salva
    getPic()
    
    move_left(ptz, request, timeout)

while(1):
    continuous_move()
    sleep(10*60)