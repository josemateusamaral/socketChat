import tkinter as tk
from functools import partial
import socket
import json

class SCREENS:
    def generateWindow(self):
        self.window = tk.Tk()
        self.window.config(bg='white')
        tamanho = int(self.window.winfo_screenheight()/2)
        px = int(self.window.winfo_screenwidth()/2 - tamanho / 2)
        py = int(self.window.winfo_screenheight()/2 - tamanho / 2)
        self.window.geometry('{}x{}+{}+{}'.format(tamanho,tamanho,px,py))
        self.window.title('EASY CHAT - Mensagens')
        
    def zeroWindow(self):
        for i in self.window.winfo_children(): i.destroy()

    def defaultWidgets(self):
        tk.Label(text=f'Servindo em {self.HOST}:{self.PORT} as {self.nickName}',bg='green').pack()

    def selectAcountScreen(self):
        self.screen = 'selectAcount'
        self.zeroWindow()
        tk.Label(text='choose acount',master=self.window).pack(side='top')
        tk.Button(text='add acount',master=self.window,command=self.loginScreen).pack(side='top')
        for nickname in self.data: 
            tk.Button(text=nickname,command=partial(self.enterAcount,nickname)).pack(expand=True)

    def loginScreen(self):
        self.screen = 'loginScreen'
        self.zeroWindow()
        tk.Label(text='nome de usuário',master=self.window).pack(side='top')
        entrada = tk.Entry(master=self.window)
        entrada.pack()
        tk.Button(text='entrar',master=self.window,command=partial(self.addAcount,entrada)).pack(side='top')

    def contactsScreen(self):
        self.lookingAtContact = 'none'
        self.screen = 'contacts'
        self.zeroWindow()
        self.window.title('EASY CHAT - Mensagens')
        self.defaultWidgets()
        done = []
        tk.Button(text='NOVA MENSAGEM',command=partial(self.newMessageScreen),bg='yellow',fg='black').pack(pady=15)
        for name in self.data[self.nickName]:
            buttonText = name
            botao = tk.Button(text=buttonText,master=self.window,command=partial(self.messageScreen,name))
            botao.pack()
        tk.Button(text='sair',command=self.fecharServidor,bg='red').pack(side='bottom')
        #tk.Button(text='change acount',command=self.selectAcountScreen,bg='blue').pack(side='bottom')

    def newMessageScreen(self):

        self.screen = 'messages'
        self.zeroWindow()

        #bannerText = f'Servindo em {self.HOST}:{self.PORT} as {self.nickName}'
        self.window.title('EASY CHAT - Nova Mensagem')
        frame = tk.Frame()
        frame.config(bg='white')
        tk.Button(text='<',command=self.contactsScreen,master=frame,bg='yellow',fg='black').pack(side='left')  
        tk.Label(master=frame,text="Contatos do Servidor",bg='white',fg='black').pack(side='left',fill='x',expand=True)  
        frame.pack(fill='x',pady=4)  

        frame = tk.Frame(master=self.window)
        listbox = tk.Listbox(master=frame,bg='gray',fg='black')
        listbox.pack(fill='both',expand=True,side='left')
        scrollbar = tk.Scrollbar(master=frame)
        scrollbar.pack(side='left',fill='y')
        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview)
        frame.pack(fill='both',side='top',expand=True)

        frame = tk.Frame()
        frame.config(bg='white')
        tk.Label(text='to: ',master=frame,bg='white',fg='black').pack(side='left')
        self.entradaHost = tk.Entry(master=frame)
        self.entradaHost.insert(0,'192.168.0.11:3001')
        self.entradaHost.pack(side='left',fill='x')
        frame.pack(fill='x',pady=4)

        frame = tk.Frame(master=self.window)
        frame.config(bg='black')
        self.NovaMensagem = tk.Entry(master=frame)
        self.NovaMensagem.pack(fill='x',side='left',expand=True)
        sendButton = tk.Button(text='SEND',bg='green',command=partial(self.enviarMensagem,"newMessage"),master=frame)
        sendButton.pack(side='left')
        frame.pack(fill='x',side='bottom')

        listbox.yview_moveto(1.0)

    def messageScreen(self,name):

        self.lookingAtContact = name
        self.screen = 'messages'
        self.zeroWindow()

        #bannerText = f'Servindo em {self.HOST}:{self.PORT} as {self.nickName}'
        bannerText = f'Messages from {name}'
        self.window.title('EASY CHAT - Messages from ' + name)
        frame = tk.Frame()
        frame.config(bg='white')
        tk.Button(text='<',command=self.contactsScreen,master=frame,bg='yellow',fg='black').pack(side='left')  
        tk.Label(master=frame,text=bannerText,bg='white',fg='black').pack(side='left',fill='x',expand=True)  
        frame.pack(fill='x',pady=4)  

        frame = tk.Frame(master=self.window)
        listbox = tk.Listbox(master=frame,bg='gray',fg='black')
        listbox.pack(fill='both',expand=True,side='left')
        scrollbar = tk.Scrollbar(master=frame)
        scrollbar.pack(side='left',fill='y')
        listbox.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = listbox.yview)
        frame.pack(fill='both',side='top',expand=True)

        frame = tk.Frame(master=self.window)
        frame.config(bg='black')
        self.NovaMensagem = tk.Entry(master=frame)
        self.NovaMensagem.pack(fill='x',side='left',expand=True)
        sendButton = tk.Button(text='SEND',command=partial(self.enviarMensagem,name),bg='green',master=frame)
        sendButton.pack(side='left')
        frame.pack(fill='x',side='bottom')
        
        for message in self.data[self.nickName][name]['messages']:
            listbox.insert(tk.END,message)

        listbox.yview_moveto(1.0)

