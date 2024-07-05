import socket, os
from threading import Thread
from modulos.server import SERVER
from modulos.screens import SCREENS
import json
            
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
        self.numeroIpServidor = '192.168.0.14:3002'

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

    def enterAcount(self,acount):
        self.nickName = acount
        self.contactsScreen()

    def tratarRequest(self,request):

        payload = json.loads(request)

        if payload["tipo"] == "mensagem":
            usuario = payload["usuario"]
            mensagem = payload["mensagem"]
            host = payload["host"]
            porta = payload["porta"]
            contato = f'{payload["host"]}:{payload["porta"]}'
            if usuario in self.data and self.data[usuario]["messages"] != []:
                if "$>>ADDUSUARIO<<$" not in mensagem:
                    self.data[usuario]['messages'].append(f"{usuario}: {mensagem}")                     
            else:
                
                payloadAddUsuario = {
                    "tipo":"mensagem",
                    "usuario":self.nickName,
                    "host":self.HOST,
                    "porta":self.PORT,
                    "mensagem":f"$>>ADDUSUARIO<<${mensagem}"
                }
                self.enviarRequest(payloadAddUsuario,host,porta)

                if "$>>ADDUSUARIO<<$" in mensagem:
                    self.data[usuario] = {'messages':[mensagem.replace("$>>ADDUSUARIO<<$","")],'contact':contato}
                    return self.messageScreen(usuario)
                else:
                    self.data[usuario] = {'messages':[f"{usuario}: {mensagem}"],'contact':contato}
                    if self.screen == "contacts":
                        self.contactsScreen()
                    return

            

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
        self.numeroIpServidor = self.ipServidor.get()
        servidor = self.numeroIpServidor.split(":")
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