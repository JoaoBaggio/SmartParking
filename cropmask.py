import os
from PIL import Image
import numpy as np

def croptype1(path_in, path_out, photos_name):
   im = Image.open(path_in + photos_name)
   np_im = np.array(im)
   for i in range(75):
       for j in range(np_im.shape[1]):
           np_im[i][j] = [128, 128, 128]
                               
   for i in range(190):
       for j in range(150):
           np_im[i][j] = [128, 128, 128]                                                

   for i in range(np_im.shape[0]):
       for j in range(610, np_im.shape[1]):
           np_im[i][j] = [128, 128, 128]
                                                                                          
                                                                                                      
   for i in range(225, np_im.shape[0]):
       for j in range(300, np_im.shape[1]):
           np_im[i][j] = [128, 128, 128]


   new_im = Image.fromarray(np_im)
   new_im.save(path_out + photos_name)


def croptype2(path_in, path_out, photos_name):
   im = Image.open(path_in + photos_name)
   np_im = np.array(im)
   for i in range(50):
       for j in range(np_im.shape[1]):
           np_im[i][j] = [128, 128, 128]

   for i in range(180):
       for j in range(210):
           np_im[i][j] = [128, 128, 128]

   for i in range(np_im.shape[0]):
       for j in range(150):
           np_im[i][j] = [128, 128, 128]


   for i in range(np_im.shape[0]):
       for j in range(625, np_im.shape[1]):
           np_im[i][j] = [128, 128, 128]



   for i in range(50, 150):
       for j in range(420, 610):
           if (19.0*i/10.0 + 345 < j):
               np_im[i][j] = [128, 128, 128]

   for i in range(330, 576):
       for j in range(150, 270):
           if (20.0*i/41.0 - 450.0/41 > j):
               np_im[i][j] = [128, 128, 128] 


   new_im = Image.fromarray(np_im)
   new_im.save(path_out + photos_name)
