import os
from threading import Thread
from functools import partial
import time
import platform

clientes = 2

if platform.system() == "Linux":
    for i in range(clientes): Thread(target=partial(os.system,'python3 Cliente.py')).start()
    time.sleep(1)
    Thread(target=partial(os.system,'python3 Servidor.py')).start()
else: 
    for i in range(clientes): Thread(target=partial(os.system,'python Cliente.py')).start()
    time.sleep(1)
    Thread(target=partial(os.system,'python Servidor.py')).start()

