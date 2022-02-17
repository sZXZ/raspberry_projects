import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import cv2
from examples.lite.examples.image_classification.raspberry_pi.image_classifier import ImageClassifier, ImageClassifierOptions
from pathlib import Path

MODEL_DIR = Path('/home/ubuntu/models')


def create_last_mnasnet_classifier(max_results=5):
    net_file = ''
    for a in MODEL_DIR.glob('mnasnet*.tflite'):
        net_file = a
    return create_classifier(net_file, max_results)

def default(max_results=5):
    return create_classifier('/home/ubuntu/examples/lite/examples/image_classification/raspberry_pi/efficientnet_lite0.tflite', max_results)
    
def create_classifier(model, max_results):
    option = ImageClassifierOptions(max_results=max_results)
    return ImageClassifier(model, options=option)
