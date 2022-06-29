import os
from scripts.funcs import *

def main():
    os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

    print("1/6 converting content video to frames...")
    video_to_frames("./videos/input/content.mp4", "./imgs/content/")

    print("2/6 converting style video to frames...")
    video_to_frames("./videos/input/style.mp4", "./imgs/style/")
    
    print("3/6 generating blend...")
    loop_frames("./imgs/content/", "./imgs/style/", "./imgs/output/", "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2")
    
    print("4/6 converting frames to video...")
    frames_to_video("./imgs/output/", "./videos/output/")

    print("5/6 deleting temporary files...")
    delete_files("./imgs/output/")
    delete_files("./imgs/content/")
    delete_files("./imgs/style/")
    delete_files("./videos/input/")

    print("6/6 done~")

if __name__ == "__main__":
    main()
