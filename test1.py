import os
from threading import Thread
from functools import partial
import time
import platform

comando = ""
if platform.system() == "Linux":
    comando = 'python3 EasyChat.py'
else: 
    comando = 'python EasyChat.py'

Thread(target=partial(os.system,comando)).start()
time.sleep(1)
Thread(target=partial(os.system,comando)).start()