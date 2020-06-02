import os

i = 0
while (1):
    print("tentativa ", i)
    i += 1
    os.system('rm -rf ~/p2/*.jpg ')
    print("removi todas as fotos antigas")
    print("iniciando o programa....")
    os.system('python2 take2post3.py')
