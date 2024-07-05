import socket, os
from threading import Thread
from modulos.server import SERVER
from modulos.screens import SCREENS
from functools import partial
import json
import time
            
class APP(SERVER,SCREENS):
    def __init__(self):
        
        self.data = {}

        self.screen = 'selectAcount'
        self.lookingAtContact = 'none'
        self.nickName = ''
        self.objetos = []
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        self.PORT = 3001
        self.HOST = s.getsockname()[0]
        self.running = True
        while True:
            if self.portaEstaLivre(self.HOST,self.PORT): break
            else: self.PORT += 1
        Thread(target=self.IniciarServidor).start()
        #self.newMessageScreen()
        self.mensagemArquivada = ""

        self.generateWindow()
        self.loginScreen()
        self.window.mainloop()

    def addAcount(self,entry):
        acount = entry.get()
        data = self.data
        if acount not in data: data[acount] = {}
        self.data = data
        self.enterAcount(acount=entry.get())

        #adicionar conta ao servidor
        return

    def enterAcount(self,acount):
        self.nickName = acount
        self.contactsScreen()

    def tratarRequest(self,request):

        payload = json.loads(request)
        print(f'Payload: {payload}')

        #foi recebida uma mensagem
        if payload["tipo"] == "mensagem":
            data = self.data
            usuario = payload["usuario"]
            mensagem = payload["mensagem"]
            host = payload["host"]
            porta = payload["porta"]
            contato = f'{payload["host"]}:{payload["porta"]}'
            if usuario in data[self.nickName]:
                data[self.nickName][usuario]['messages'].append(f"{usuario}: {mensagem}")
            else:
                data[self.nickName][usuario] = {'messages':[mensagem],'contact':contato}
                
                payloadAddUsuario = {
                    "tipo":"mensagem",
                    "usuario":self.nickName,
                    "host":self.HOST,
                    "porta":self.PORT,
                    "mensagem":f"{mensagem}"
                }
                self.enviarRequest(payloadAddUsuario,host,porta)

            self.data = data
            self.messageScreen(usuario)

        elif payload["tipo"] == "pedirNome":
            host = payload["host"]
            porta = payload["porta"]
            payloadMandarNome = {
                "tipo":"nome",
                "usuario":self.nickName,
                "host":self.HOST,
                "porta":self.PORT
            }
            self.enviarRequest(payloadMandarNome,host,porta)

        elif payload["tipo"] == "nome":
            usuario = payload["usuario"]
            host = payload["host"]
            porta = payload["porta"]
            bd = self.data
            contato = f'{host}:{porta}'
            bd[self.nickName][usuario] = {"mensagens":[],"contato":contato}
            self.data = bd
            self.messageScreen(usuario)
    
    def enviarMensagem(self,name):
        if name == 'newMessage':
            HOST = self.entradaHost.get().split(':')
        else: 
            HOST = self.data[self.nickName][name]['contact'].split(':')

        #enviar mensagem
        mensagem = self.NovaMensagem.get()
        payload = {
            "tipo":"mensagem",
            "mensagem":mensagem,
            "usuario":self.nickName,
            "host":self.HOST,
            "porta":self.PORT
        }
        self.enviarRequest(payload,HOST[0],int(HOST[1]))

        if name == 'newMessage':
            self.contactsScreen()
        else:
            data = self.data
            data[self.nickName][name]['messages'].append(self.NovaMensagem.get())
            self.data = data 
            return self.messageScreen(name)      



APP()