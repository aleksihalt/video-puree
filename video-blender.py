import os
from scripts.funcs import *

from PyInquirer import prompt
from examples import custom_style_2
print("")
print("WELCOME TO VIDEOPUREE")
print("")
print("IT BLENDS VIDEOS TOGETHER")
print("")
print("SHAMELESSLY PLAGIARISED FROM TENSORFLOW AND 'REPURPOSED' BY https://github.com/aleksihalt/")
print("")

questions = [
    {
        "type": "input",
        "name": "style_path",
        "message": "1. drag and drop STYLE video or type path"
    },
    {
        "type": "input",
        "name": "content_path",
        "message": "2. drag and drop CONTENT video or type path"
    }
]

def main(style_input, content_input):
    os.environ['TFHUB_MODEL_LOAD_FORMAT'] = 'COMPRESSED'

    print("1/6 converting content video to frames...")
    video_to_frames(content_input, "./imgs/content/")

    print("2/6 converting style video to frames...")
    video_to_frames(style_input, "./imgs/style/")
    
    print("3/6 generating blend...")
    loop_frames("./imgs/content/", "./imgs/style/", "./imgs/output/", "https://tfhub.dev/google/magenta/arbitrary-image-stylization-v1-256/2")
    
    print("4/6 converting frames to video...")
    output_path = frames_to_video("./imgs/output/", "./videos/output/")

    print("5/6 deleting temporary files...")
    delete_files("./imgs/output/")
    delete_files("./imgs/content/")
    delete_files("./imgs/style/")
    delete_files("./videos/input/")

    print("6/6 done~")
    print("")
    
    print(f"blended video can be found in {output_path}")

if __name__ == "__main__":
    answers = prompt(questions, style=custom_style_2)
    print(answers["style_path"])
    main(answers["style_path"].replace("'",""), answers["content_path"].replace("'",""))