import socket, os
from threading import Thread
from modulos.server import SERVER
from modulos.screens import SCREENS
import tkinter as tk
import json
from functools import partial
            
class APP(SERVER,SCREENS):
    def __init__(self):
        self.screen = 'selectAcount'
        self.nickName = ''
        self.objetos = []
        self.contatos = {}
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8",80))
        self.PORT = 3001
        self.HOST = s.getsockname()[0]
        self.running = True
        self.generateWindow()
        while True:
            if self.portaEstaLivre(self.HOST,self.PORT): break
            else: self.PORT += 1
        Thread(target=self.IniciarServidor).start()
        self.serverStatus()
        
        self.window.mainloop()

    def serverStatus(self):

        self.screen = 'status'
        self.zeroWindow()

        bannerText = f'Servidor rodando em {self.HOST}:{self.PORT}'
        frame = tk.Frame()
        frame.config(bg='white')
        tk.Button(text='Desligar',command=self.contactsScreen,master=frame,bg='red',fg='white').pack(side='left')  
        tk.Label(master=frame,text=bannerText,bg='white',fg='black').pack(side='left',fill='x',expand=True)  
        self.window.title('Servidor de contatos')
        frame.pack(fill='x',pady=4)  
        frame = tk.Frame(master=self.window)
        listbox = tk.Listbox(master=frame,bg='gray',fg='black')
        listbox.pack(fill='both',expand=True,side='left')
        scrollbar = tk.Scrollbar(master=frame)
        scrollbar.pack(side='left',fill='y')
        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview)
        frame.pack(fill='both',side='top',expand=True)
        
        listbox.insert(tk.END,f"")
        listbox.insert(tk.END,f"")
        listbox.insert(tk.END,f"  SERVIDOR DE CONTATOS")
        listbox.insert(tk.END,f"  Total de {len(self.contatos)} usuario encontrados")
        listbox.insert(tk.END,f"")
        listbox.insert(tk.END,f"")

        for contato in self.contatos:
            listbox.insert(tk.END,"  " + contato)
            listbox.insert(tk.END,"  --- host:" + self.contatos[contato]["host"])
            listbox.insert(tk.END,"  --- porta:" + str(self.contatos[contato]["porta"]))
            listbox.insert(tk.END,f"")
            listbox.insert(tk.END,f"")


        listbox.yview_moveto(1.0)

    def tratarRequest(self,data):

        payload = json.loads(data)
        if payload["tipo"] not in [
            "atualizarContatos",
            "mudarVisibilidade"
        ]: return

        usuario = payload["usuario"]
        host = payload["host"]
        porta = payload["porta"]
        visivel = payload["visivel"]

        if usuario not in self.contatos and visivel:
            self.contatos[usuario] = {
                "host":host,
                "porta":porta
            }

        if payload["tipo"] == "atualizarContatos":
            payloadAtualizaacao = {
                "tipo":"atualizacaoContatos",
                "contatos":self.contatos
            }
            self.enviarRequest(payloadAtualizaacao,host,porta)

        elif payload["tipo"] == "mudarVisibilidade":
            print("alterando a visibilidade do usuario:",usuario)
            if not visivel and usuario in self.contatos:
                del self.contatos[usuario]
            payloadAtualizaacao = {
                "tipo":"atualizacaoContatos",
                "contatos":self.contatos
            }
            self.enviarRequest(payloadAtualizaacao,host,porta)

        self.serverStatus()

    def atualizarTodoMundo(self,excessoes=[]):
        for contato in self.contatos:
            if contato in excessoes:
                continue
            payloadAtualizaacao = {
                "tipo":"atualizacaoContatos",
                "contatos":self.contatos
            }
            host = self.contatos[contato]["host"]
            porta = self.contatos[contato]["porta"]
            self.enviarRequest(payloadAtualizaacao,host,porta)
            

APP()