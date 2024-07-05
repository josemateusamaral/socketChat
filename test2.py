import os
from threading import Thread
from functools import partial
import time
import platform

comando = ""
if platform.system() == "Linux":
    Thread(target=partial(os.system,'python3 EasyChat.py')).start()
    time.sleep(1)
    Thread(target=partial(os.system,'python3 Servidor.py')).start()
else: 
    Thread(target=partial(os.system,'python EasyChat.py')).start()
    time.sleep(1)
    Thread(target=partial(os.system,'python Servidor.py')).start()

