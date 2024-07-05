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
        self.visivel = False
        self.screen = 'selectAcount'
        self.lookingAtContact = 'none'
        self.nickName = ''
        self.objetos = []
        self.contatosServidor = {}
        self.contatoSelecionado = None

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        self.PORT = 3001
        self.HOST = s.getsockname()[0]
        self.running = True
        while True:
            if self.portaEstaLivre(self.HOST,self.PORT): break
            else: self.PORT += 1
        Thread(target=self.IniciarServidor).start()

        self.generateWindow()
        self.loginScreen()
        self.window.mainloop()

    def addAcount(self,entry):
        acount = entry.get()
        if acount not in self.data: self.data[acount] = {}
        self.enterAcount(acount=entry.get())

        #adicionar conta ao servidor
        return

    def enterAcount(self,acount):
        self.nickName = acount
        self.contactsScreen()

    def tratarRequest(self,request):

        print("request:",request)

        payload = json.loads(request)
        print(f'tratando request: {payload}')

        #foi recebida uma mensagem
        if payload["tipo"] == "mensagem":
            usuario = payload["usuario"]
            mensagem = payload["mensagem"]
            host = payload["host"]
            porta = payload["porta"]
            contato = f'{payload["host"]}:{payload["porta"]}'
            if usuario in self.data and self.data[usuario]["messages"] != []:
                self.data[usuario]['messages'].append(f"{usuario}: {mensagem}")
            else:
                if mensagem[:11] == "addUsuario:":
                    self.data[usuario] = {'messages':[mensagem[11:]],'contact':contato}
                else:
                    self.data[usuario] = {'messages':[f"{usuario}: {mensagem}"],'contact':contato}
                
                payloadAddUsuario = {
                    "tipo":"mensagem",
                    "usuario":self.nickName,
                    "host":self.HOST,
                    "porta":self.PORT,
                    "mensagem":f"addUsuario:{mensagem}"
                }
                self.enviarRequest(payloadAddUsuario,host,porta)

            self.messageScreen(usuario)

        elif payload["tipo"] == "atualizacaoContatos":
            self.contatosServidor = payload["contatos"]      
            self.newMessageScreen()  
    
    def enviarMensagem(self,name):
        if name == 'newMessage':
            usuario = self.entradaHost.get()
            if usuario in self.contatosServidor:
                host = self.contatosServidor[usuario]["host"]
                porta = self.contatosServidor[usuario]["porta"]
                HOST = [host,int(porta)]
            else:
                HOST = self.entradaHost.get().split(':')
        else: 
            HOST = self.data[name]['contact'].split(':')

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
            self.data[name]['messages'].append(self.NovaMensagem.get())
            return self.messageScreen(name)      

    def atualizarServidor(self):
        print("atualizando servidor")
        servidor = self.ipServidor.get().split(":")
        host = servidor[0]
        porta = int(servidor[1])

        payload = {
            "tipo":"atualizarContatos",
            "usuario":self.nickName,
            "host":self.HOST,
            "porta":self.PORT,
            "visivel":self.visivel
        }
        self.enviarRequest(payload,host,porta)       



APP()