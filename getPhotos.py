
from datetime import datetime
import time
import urllib
import os

def getNameInfo():
    data, time = str(datetime.now()).split()
    year, month, day = data.split('-')
    time, a = time.split('.')
    hour, minute, second = time.split(':')
    return year, month, day, hour, minute, second

while(1):
    year, month, day, hour, minute, second = getNameInfo()
    nome = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '.jpg'
    myPath = "/home/joao.victor/photos/"
    fullfilename = os.path.join(myPath, nome)
    URL = 'http://177.220.84.10/webcapture.jpg?command=snap&channel=1&user=admin&password=tlJwpbo6'
    urllib.urlretrieve(URL, fullfilename)
    time.sleep(60*10) 
