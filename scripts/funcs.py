import tensorflow as tf
import PIL.Image
from PIL import Image
import numpy as np
import os
import tensorflow_hub as hub
import imageio
from pathlib import Path
from datetime import datetime
import cv2
import glob


def tensor_to_image(tensor):
    tensor = tensor*255
    tensor = np.array(tensor, dtype=np.uint8)
    if np.ndim(tensor)>3:
        assert tensor.shape[0] == 1
        tensor = tensor[0]
        return PIL.Image.fromarray(tensor)    

def load_img(path_to_img):
    max_dim = 512
    img = tf.io.read_file(path_to_img)
    img = tf.image.decode_image(img, channels=3)
    img = tf.image.convert_image_dtype(img, tf.float32)

    shape = tf.cast(tf.shape(img)[:-1], tf.float32)
    long_dim = max(shape)
    scale = max_dim / long_dim

    new_shape = tf.cast(shape * scale, tf.int32)

    img = tf.image.resize(img, new_shape)
    img = img[tf.newaxis, :]
    return img



def loop_frames(content_path, style_path, output_path, model_path):
    content_ls = os.listdir(content_path)
    style_ls = os.listdir(style_path)
    number_imgs = min(len(content_ls), len(style_ls))       
    for i in range(number_imgs):
        content_image = load_img(f"{content_path}{i}.png")
        style_image = load_img(f"{style_path}{i}.png")
        hub_model = hub.load(model_path)
        stylized_image = hub_model(tf.constant(content_image), tf.constant(style_image))[0]
        output_img= tensor_to_image(stylized_image)
        output_img.save(f"{output_path}{i}.png")
        progress = int(int(i)/int(number_imgs)*100)
        print("", end=f"\r{progress} %")
    print("100%")

def frames_to_video(input_path, output_path):
    cur_time = datetime.now()
    date_and_time = cur_time.strftime("%d-%m-%y_%H-%M-%S")
    input_ls = os.listdir(input_path)
    ims=[]
    for i in range(len(input_ls)):
        my_file = Path(f"{input_path}{i}.png")
        if my_file.is_file():
            im = Image.open(my_file)
            ima = np.array(im)
            ims.append(ima)
            im.close()
        else:
            pass
    filepath = f"{output_path}{date_and_time}.mp4"
    imageio.mimwrite(filepath, ims , fps = 30)
    return filepath

def video_to_frames(input_path, output_path):
    cap= cv2.VideoCapture(input_path)
    i=0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if ret == False:
            break
        cv2.imwrite(f"{output_path}{i}.png", frame)
        i+=1
    cap.release()
    cv2.destroyAllWindows()

def delete_files(in_path):
    files = glob.glob(f"{in_path}*")
    for f in files:
        os.remove(f)