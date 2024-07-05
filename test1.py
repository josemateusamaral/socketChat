import os
from threading import Thread
from functools import partial
import time
import platform

if platform.system() == "Linux":
    comando = 'python3 Cliente.py'
else: 
    comando = 'python Cliente.py'

clientes = 2
for i in range(clientes):
    Thread(target=partial(os.system,comando)).start()
    time.sleep(2)
