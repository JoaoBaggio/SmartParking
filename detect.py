from __future__ import division
from time import sleep

from models import *
from utils.utils import *
from utils.datasets import *

import os
import sys
import time
import datetime
import argparse

from PIL import Image

import torch
from torch.utils.data import DataLoader
from torchvision import datasets
from torch.autograd import Variable

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.ticker import NullLocator

import paho.mqtt.client as mqtt
import json

def bb_IoU(boxA, boxB):
    xA = max(boxA[0], boxB[0])
    yA = max(boxA[1], boxB[1])
    xB = min(boxA[2], boxB[2])
    yB = min(boxA[3], boxB[3])
    
    interArea = max(0, xB - xA + 1) * max(0, yB - yA + 1)
    boxAArea = (boxA[2] - boxA[0] + 1) * (boxA[3] - boxA[1] + 1)
    boxBArea = (boxB[2] - boxB[0] + 1) * (boxB[3] - boxB[1] + 1)

    iou = interArea / float(boxAArea + boxBArea - interArea)

    return iou


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--image_folder", type=str, default="/home/joao.victor/p2/", help="path to dataset")
    #parser.add_argument("--output_folder", type=str, default="output", help="path to output folder")
    parser.add_argument("--model_def", type=str, default="/home/joao.victor/PyTorch-YOLOv3/config/yolov3.cfg", help="path to model definition file")
    parser.add_argument("--weights_path", type=str, default="/home/joao.victor/PyTorch-YOLOv3/weights/yolov3.weights", help="path to weights file")
    parser.add_argument("--class_path", type=str, default="/home/joao.victor/PyTorch-YOLOv3/data/coco.names", help="path to class label file")
    parser.add_argument("--conf_thres", type=float, default=0.8, help="object confidence threshold")
    parser.add_argument("--nms_thres", type=float, default=0.4, help="iou thresshold for non-maximum suppression")
    parser.add_argument("--batch_size", type=int, default=1, help="size of the batches")
    parser.add_argument("--n_cpu", type=int, default=0, help="number of cpu threads to use during batch generation")
    parser.add_argument("--img_size", type=int, default=416, help="size of each image dimension")
    parser.add_argument("--checkpoint_model", type=str, help="path to checkpoint model")
    opt = parser.parse_args()
    #print(opt)

    max_vagas = 16
    client = mqtt.Client()
    client.username_pw_set("8qttpktuerb8", "wBlCJgB8hbJU")
    #client.connect("mqtt.demo.konkerlabs.net", 1883)
    # client.publish("data/8qttpktuerb8/pub/Vagas", 88)
    # client.publish("data/8qttpktuerb8/pub/Vagas", json.dumps({"Veiculos": 22, "Vagas": MAX - VEICULOS}))


    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    
    #os.makedirs(opt.output_folder, exist_ok=True)

    # Set up model
    model = Darknet(opt.model_def, img_size=opt.img_size).to(device)

    if opt.weights_path.endswith(".weights"):
        # Load darknet weights
        model.load_darknet_weights(opt.weights_path)
    else:
        # Load checkpoint weights
        model.load_state_dict(torch.load(opt.weights_path))

    model.eval()  # Set in evaluation mode

    dataloader = DataLoader(
        ImageFolder(opt.image_folder, img_size=opt.img_size),
        batch_size=opt.batch_size,
        shuffle=False,
        num_workers=opt.n_cpu,
    )

    classes = load_classes(opt.class_path)  # Extracts class labels from file

    Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor

    while(1):
        imgs = []  # Stores image paths
        img_detections = []  # Stores detections for each image index


        os.system('rm ~/p2/*.jpg')
        try:
            os.system('python2 /home/joao.victor/SmartParking/takepic.py ')
        
        except Exception as e:
            print("houve algum erro tirando a foto, tentando de novo dentro de 1 min")
            print("type error: " +str(e))
            sleep(2*60)
            continue
        else:
            print("\nPerforming object detection:")
            dataloader = DataLoader(
                ImageFolder(opt.image_folder, img_size=opt.img_size),
                batch_size=opt.batch_size,
                shuffle=False,
                num_workers=opt.n_cpu,
            )
            prev_time = time.time()
            for batch_i, (img_paths, input_imgs) in enumerate(dataloader):
                # Configure input
                input_imgs = Variable(input_imgs.type(Tensor))

                # Get detections
                with torch.no_grad():
                    detections = model(input_imgs)
                    detections = non_max_suppression(detections, opt.conf_thres, opt.nms_thres)

                # Log progress
                current_time = time.time()
                inference_time = datetime.timedelta(seconds=current_time - prev_time)
                prev_time = current_time
                print("\t+ Batch %d, Inference Time: %s" % (batch_i, inference_time))

                # Save image and detections
                imgs.extend(img_paths)
                img_detections.extend(detections)

            print("\nSaving images:")
            # Iterate through images and save plot of detections
            nv = 0
            for img_i, (path, detections) in enumerate(zip(imgs, img_detections)):

                print("(%d) Image: '%s'" % (img_i, path))

                # Create plot
                img = np.array(Image.open(path))
                
                # Draw bounding boxes and labels of detections
                if detections is not None:
                    # Rescale boxes to original image
                    detections = rescale_boxes(detections, opt.img_size, img.shape[:2])
                    
                    for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:
                        #print("\t+ Label: %s, Conf: %.5f" % (classes[int(cls_pred)], cls_conf.item()))
                        v = True
                        for x1u, y1u, x2u, y2u, confu, cls_confu, cls_predu in detections:
                            if int(cls_pred) == int(cls_predu): ## IoU to diferent classes
                                continue
                            else:
                                iou = bb_IoU((x1,y1, x2, y2), (x1u, y1u, x2u, y2u))
                                if iou > 0.8 and float(cls_conf) < float(cls_confu):
                                    v = False
                        if (classes[int(cls_pred)] == 'vehicle' and v):
                            nv += 1
                    
            print ("Number of vehicles in the image = " + str(nv))
            client.connect("mqtt.demo.konkerlabs.net", 1883)
            client.publish("data/8qttpktuerb8/pub/Vagas", max(0, max_vagas-nv))
            os.system('rm ~/p2/*.jpg')