# coding: utf-8

import socket
import sala
import threading
import time
from Tkinter import *

def trocaStatus(codBotao):
	global status
	global statusLabel

	print codBotao
	if status == False and codBotao == 1:
		statusLabel['text'] = 'rodando'
		statusLabel['fg'] = '#0C0'
		status = True
	elif status == True and codBotao == 2:
		statusLabel['text'] = 'parado'
		statusLabel['fg'] = '#C00'
		status = False

def iniciaThread():
	trocaStatus(1)
	t1_stop = threading.Event()
	t1 = threading.Thread(target = thread1, args = (1, t1_stop))
	t1.start()

def thread1(arg1, eventoDeParada):
	ipLabel['text'] = TCP_IP
	portaLabel['text'] = TCP_PORT
	while not eventoDeParada.is_set():
		#print 'Thread 1 rodando \n'
		s.listen(1)
		conn, addr = s.accept()
		print 'Connection address:', addr

		data = conn.recv(BUFFER_SIZE)

		if(data[:2] == 'CS'): #Cria Sala
			salas.adicionaConexao(conn,data[2:],addr[0])

		if(data[:2] == 'EM'): #Envia Msg
			msg = data.split('KEYCONTROLLER')
			salas.enviaMsg(msg[2], msg[3], msg[1])

		if(data[:2] == 'LS'): #Lista de Salas
			lista = salas.listaSalas()
			out = ""
			for i in range(len(lista)):
				out = out + str(i+1)+'-'+lista[i]+'\n'
			conn.send(out)

def parar():
	t1_stop.set()
	trocaStatus(2)

status = False
TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_PORT = 8000
t1_stop = threading.Event()
salas = sala.sala()
BUFFER_SIZE = 2048  
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind((TCP_IP, TCP_PORT))


# Início da GUI ------------------------------------------------------------
root = Tk();
root.geometry('180x270')
container = Frame(root)
container.pack()

btnStart = Button(container)
btnStart.configure(text = 'Iniciar', padx = 30, pady = 10, command = iniciaThread)
btnStart.pack(pady = 30)
btnStop = Button(container)
btnStop.configure(text = 'Parar', padx = 30, pady = 10, command = parar)
btnStop.pack()

container2 = Frame()
container2.pack(pady = 30)
LS = Label(container2, text = 'Status: ')
LS.grid(row = 0, column = 0)

statusLabel = Label(container2, text = 'parado', fg = '#C00')
statusLabel.grid(row = 0, column = 1)

IL = Label(container2, text = 'IP: ')
IL.grid(row = 1, column = 0)

ipLabel = Label(container2)
ipLabel.grid(row = 1, column = 1)

PL = Label(container2, text = 'Porta: ')
PL.grid(row = 2, column = 0)

portaLabel = Label(container2)
portaLabel.grid(row = 2, column = 1)

# Fim da GUI --------------------------------------------------------------------------

root.mainloop()



