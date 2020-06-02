from datetime import datetime
from time import sleep
import urllib
import sys
import os

import onvifconfig


def getNameInfo():
    data, time = str(datetime.now()).split()
    year, month, day = data.split('-')
    time, a = time.split('.')
    hour, minute, second = time.split(':')
    return year, month, day, hour, minute, second

def getPic(t100):
    year, month, day, hour, minute, second = getNameInfo()
    nome = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '.jpg'
    myPath = "/home/joao.victor/photos2pos/"
    fullfilename = os.path.join(myPath, nome)

    URL = 'http://177.220.84.10/webcapture.jpg?command=snap&channel=1&user=admin&password=tlJwpbo6'
    urllib.urlretrieve(URL, fullfilename)

    if (hour == '09' and t100[0] == False):
        t100[0] = True
        t = str(len(os.listdir("/home/joao.victor/photosTake100/"))) #numero do teste segundo numero de arq
        os.mkdir("/home/joao.victor/photosTake100/T"+ t) #cria nova pasta
        for i in range(100):
            nome = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '-' + str(i).zfill(2) + '.jpg'
            myPath = "/home/joao.victor/photosTake100/T"+ t
            fullfilename = os.path.join(myPath, nome)
            urllib.urlretrieve(URL, fullfilename)

    if (hour == '15' and t100[1] == False):
        t100[1] = True
        t = str(len(os.listdir("/home/joao.victor/photosTake100/"))) #numero do teste segundo numero de arq
        os.mkdir("/home/joao.victor/photosTake100/T"+ t) #cria nova pasta
        for i in range(100):
            nome = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '-' + str(i).zfill(2) + '.jpg'
            myPath = "/home/joao.victor/photosTake100/T"+ t
            fullfilename = os.path.join(myPath, nome)
            urllib.urlretrieve(URL, fullfilename)

    if (hour == '21' and t100[2] == False):
        t100[2] = True
        t = str(len(os.listdir("/home/joao.victor/photosTake100/"))) #numero do teste segundo numero de arq
        os.mkdir("/home/joao.victor/photosTake100/T"+ t) #cria nova pasta
        for i in range(100):
            nome = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '-' + str(i).zfill(2) + '.jpg'
            myPath = "/home/joao.victor/photosTake100/T"+ t
            fullfilename = os.path.join(myPath, nome)
            urllib.urlretrieve(URL, fullfilename)

    if (hour == '22'):
        t100[0] = [False]
        t100[1] = [False]
        t100[2] = [False]

if __name__ == '__main__':
    t100 = [False, False, False]
    t100t = [True, True, True]
    #Do all setup initializations
    ptz = onvifconfig.ptzcam()
    ptz.move_pan(-1.0, 20)
    while(1):

        # move right -- (velocity, duration of move)
        ptz.move_pan(1.0, 7.5)
        #tira a foto e salva
        getPic(t100)
        
        # move right -- (velocity, duration of move)
        ptz.move_pan(1.0, 2.5)
        
        #tira a foto e salva
        getPic(t100t)
        
        #volta para a posicao inicial
        ptz.move_pan(-1.0, 20)

        sleep(10*60)
