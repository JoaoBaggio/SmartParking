from datetime import datetime
from time import sleep
import urllib
import sys
import os

def getNameInfo():
    data, time = str(datetime.now()).split()
    #print(time)
    year, month, day = data.split('-')
    if ('.' in time):
        time, a = time.split('.')
    hour, minute, second = time.split(':')
    return year, month, day, hour, minute, second

while(1):
    year, month, day, hour, minute, second = getNameInfo()
    if (hour == '09' or hour == '15' or hour == '21'):
        if(minute == '00'): 
            t = str(len(os.listdir("/home/joao.victor/photosTake100/"))) #numero do teste segundo numero de arq
            os.mkdir("/home/joao.victor/photosTake100/T"+ t) #cria nova pasta
            for i in range(100):
                nome = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '-' + str(i).zfill(2) + '.jpg'
                myPath = "/home/joao.victor/photosTake100/T"+ t
                fullfilename = os.path.join(myPath, nome)

                URL = 'http://177.220.84.10/webcapture.jpg?command=snap&channel=1&user=admin&password=tlJwpbo6'
                urllib.urlretrieve(URL, fullfilename)
            sleep(60*60*5)
