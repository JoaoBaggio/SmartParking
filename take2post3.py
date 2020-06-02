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

def getPic(t100):
    year, month, day, hour, minute, second = getNameInfo()
    name = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '.jpg'
    myPath = "/home/joao.victor/photos2pos/"
    myPath2 = "/home/joao.victor/p2/"
    fullfilename = os.path.join(myPath, name)

    URL = 'http://177.220.84.10/webcapture.jpg?command=snap&channel=1&user=admin&password=tlJwpbo6'
    urllib.urlretrieve(URL, fullfilename)

    if (hour == '09' and t100[0] == False):
        t100[0] = True
        t = str(len(os.listdir("/home/joao.victor/photosTake100/"))) #numero do teste segundo numero de arq
        os.mkdir("/home/joao.victor/photosTake100/T"+ t) #cria nova pasta
        for i in range(100):
            nome = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '-' + str(i).zfill(2) + '.jpg'
            myPath = "/home/joao.victor/photosTake100/T"+ t + '/'
            fullfilename = os.path.join(myPath, nome)
            urllib.urlretrieve(URL, fullfilename)

    if (hour == '15' and t100[1] == False):
        t100[1] = True
        t = str(len(os.listdir("/home/joao.victor/photosTake100/"))) #numero do teste segundo numero de arq
        os.mkdir("/home/joao.victor/photosTake100/T"+ t) #cria nova pasta
        for i in range(100):
            nome = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '-' + str(i).zfill(2) + '.jpg'
            myPath = "/home/joao.victor/photosTake100/T"+ t + '/'
            fullfilename = os.path.join(myPath, nome)
            urllib.urlretrieve(URL, fullfilename)

    if (hour == '21' and t100[2] == False):
        t100[2] = True
        t = str(len(os.listdir("/home/joao.victor/photosTake100/"))) #numero do teste segundo numero de arq
        os.mkdir("/home/joao.victor/photosTake100/T"+ t) #cria nova pasta
        for i in range(100):
            nome = "pic" +'_'+ year + '-' + month  + '-' + day  + '_' + hour  + ':' + minute  + ':' + second + '-' + str(i).zfill(2) + '.jpg'
            myPath = "/home/joao.victor/photosTake100/T"+ t + '/'
            fullfilename = os.path.join(myPath, nome)
            urllib.urlretrieve(URL, fullfilename)

    if (hour == '22'):
        t100[0] = [False]
        t100[1] = [False]
        t100[2] = [False]

    return myPath, myPath2, name

if __name__ == '__main__':
    #t100 = [False, False, False]
    t100 = [True, True, True]
    t100t = [True, True, True]
    #Do all setup initializations
    print("inicializando")
    ptz = onvifconfig.ptzcam()
    ptz.move_pan(-1.0, 30)
    #os.system('mkdir /home/joao.victor/p2')
    while(1):

        try:
            # move right -- (velocity, duration of move)
            print("Primeira movimentacao a direita")
            ptz.zoom(-1,1)
            ptz.move_pan(1.0, 7.0)
            #tira a foto e salva
            print("Tira foto")
            pin, pout, name = getPic(t100)
            #Aplica a mascara 
            croptype1(pin, pout, name)
            # move right -- (velocity, duration of move)
            #ptz.zoom(-1,1)
            print("Segunda movimentacao a direita")
            ptz.move_pan(1.0, 2.5)
        
            #tira a foto e salva
            print("Tira segunda foto")
            pin, pout, name = getPic(t100t)
            #Aplica a mascara
            croptype2(pin, pout, name)
            #volta para a posicao inicial
            ptz.move_pan(-1.0, 20)
            print("inicia a classificacao")
            os.system('python3 /home/joao.victor/PyTorch-YOLOv3/detectv4.py ')

         
            sleep(1*60)
        except Exception as e:
            print("houve algum erro")
            print("type error: " +str(e))
            sleep(2*60)

