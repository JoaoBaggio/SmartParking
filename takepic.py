from datetime import datetime
from time import sleep
import urllib
import sys
import os

import onvifconfig

from cropmask import croptype1, croptype2

def getNameInfo():
    data, time = str(datetime.now()).split()
    year, month, day = data.split('-')
    time, a = time.split('.')
    hour, minute, second = time.split(':')
    return year, month, day, hour, minute, second

def getPic():
    year, month, day, hour, minute, second = getNameInfo()
    name = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '.jpg'
    myPath = "/home/joao.victor/photos2pos/"
    myPath2 = "/home/joao.victor/p2/"
    fullfilename = os.path.join(myPath, name)
    URL = 'http://177.220.84.10/webcapture.jpg?command=snap&channel=1&user=admin&password=tlJwpbo6'
    urllib.urlretrieve(URL, fullfilename)

    return myPath, myPath2, name

if __name__ == '__main__':
    #Do all setup initializations
    print("inicializando")
    ptz = onvifconfig.ptzcam()
    ptz.move_pan(-1.0, 30)
    #os.system('mkdir /home/joao.victor/p2')
    print("Primeira movimentacao a direita")
    ptz.zoom(-1,1)
    ptz.move_pan(1.0, 7.0)
    #tira a foto e salva
    print("Tira foto")
    pin, pout, name = getPic()
    #Aplica a mascara 
    croptype1(pin, pout, name)
    print("Segunda movimentacao a direita")
    ptz.move_pan(1.0, 2.5)
    #tira a foto e salva
    print("Tira segunda foto")
    pin, pout, name = getPic()
    #Aplica a mascara
    croptype2(pin, pout, name)
    #volta para a posicao inicial
    ptz.move_pan(-1.0, 20)
    print("inicia a classificacao")