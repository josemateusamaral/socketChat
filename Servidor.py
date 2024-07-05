import socket, os
from threading import Thread
from modulos.database import DATABASE
from modulos.server import SERVER
from modulos.screens import SCREENS
import tkinter as tk
import sqlite3
from functools import partial
            
class APP(SERVER,SCREENS,DATABASE):
    def __init__(self):
        self.screen = 'selectAcount'
        self.nickName = ''
        self.objetos = []
        self.mensagensRecebidas = ["jhiojij","jijgg7g67g","ivjoidjvoxijv"]
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
        self.window.title('Servidor online')
        frame.pack(fill='x',pady=4)  

        frame = tk.Frame(master=self.window)
        listbox = tk.Listbox(master=frame,bg='gray',fg='black')
        listbox.pack(fill='both',expand=True,side='left')
        scrollbar = tk.Scrollbar(master=frame)
        scrollbar.pack(side='left',fill='y')
        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview)
        frame.pack(fill='both',side='top',expand=True)
        
        for message in self.mensagensRecebidas:
            listbox.insert(tk.END,message)

        listbox.yview_moveto(1.0)

    def tratarRequest(self,data):
        self.mensagensRecebidas.append(data)
        self.serverStatus()

APP()