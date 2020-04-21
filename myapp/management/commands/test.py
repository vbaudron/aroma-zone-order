import os


def start():
    print("let's see ...")
    print("django setting module :", os.environ.get("DJANGO_SETTINGS_MODULE"))


if __name__ == '__main__':
    start()