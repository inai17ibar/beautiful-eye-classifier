import gradio as gr
import cv2
import numpy as np

def detect_eyes(image):
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')
    eyes = eye_cascade.detectMultiScale(image, 1.3, 5)
    
    for (ex,ey,ew,eh) in eyes:
        cv2.rectangle(image,(ex,ey),(ex+ew,ey+eh),(0,255,0),2)
    
    return image

interface = gr.Interface(fn=detect_eyes, inputs="image", outputs="image")
interface.launch()