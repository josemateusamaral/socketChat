import socket
import sys
import json
import time


class SERVER:
    def IniciarServidor(self):      
        while self.running:       
            with socket.socket(socket.AF_INET,socket.SOCK_STREAM) as s:
                s.bind((self.HOST,self.PORT))
                s.listen()
                conn,addr = s.accept()
                with conn:
                    while True:
                        dataRaw = conn.recv(2048)
                        data = repr(dataRaw)[2:-1]
                        if not dataRaw: break
                        self.tratarRequest(data)
                        
    def enviarRequest(self,payload,host,porta):
        payload = json.dumps(payload)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((host,porta))
            s.sendall(payload.encode('utf-8'))   

    def tratarRequest(self,request):
        print("Request:",request)

    def fecharServidor(self):
        self.running = False
        self.window.destroy()
        sys.exit()

    def portaEstaLivre(self,host,port):
        try:      
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host,port))
                s.close()
            return True
        except: return False