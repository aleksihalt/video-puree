from scripts.funcs import *

def main():
    frames_to_video("./imgs/output/", "./videos/output/")
    print("deleting files...")
    delete_files("./imgs/output/")
    delete_files("./imgs/content/")
    delete_files("./imgs/style/")
    delete_files("./videos/input/")

    print("done~")


if __name__ == "__main__":
    main()
