#encoding: utf-8
import socket, sala, threading, time, usuario
from Tkinter import *

KEYCONTROLLER = '<ctrl>'
def trocaStatus(codBotao):
	global status
	global statusLabel

	print codBotao
	if not status  and codBotao == 1:
		statusLabel['text'] = 'rodando'
		statusLabel['fg'] = '#0C0'
		status = True
	elif status and codBotao == 2:
		statusLabel['text'] = 'parado'
		statusLabel['fg'] = '#C00'
		status = False
#trocaStatus()

def iniciaThread():
	global t1_stop
	trocaStatus(1)
	t1_stop = threading.Event()
	t1 = threading.Thread(target = thread1, args = (1, t1_stop))
	t1.start()
#iniciaThread()

def thread1(arg1, eventoDeParada):
	global numeroSalasLabel
	global numeroSalas
	
	ipLabel['text'] = TCP_IP
	portaLabel['text'] = TCP_PORT
	while not eventoDeParada.is_set():
		#print 'Thread 1 rodando \n'
		s.listen(1)
		conn, addr = s.accept()

		data = conn.recv(BUFFER_SIZE)

		if(data[:2] == 'CS'): #Cria Sala
			

			aux = data.split(KEYCONTROLLER)
			user = usuario.usuario(aux[1],addr[0],conn)
			if not salas.criaSala(user,aux[2],addr[0]):
				msg = KEYCONTROLLER+'salaInvalida'+KEYCONTROLLER
				conn.send(msg)

		if(data[:2] == 'EM'): #Envia Msg
			msg = data.split(KEYCONTROLLER)
			comando = verificaComando(msg[3])

			if comando != None:
				executaComando(comando,conn,addr[0])
			else: 
				salas.enviaMsg(msg[2], msg[3], msg[1])
			conn.send('ok')

		if(data[:2] == 'LS'): #Lista de Salas
			lista = salas.listaSalas()
			out = ""
			for i in range(len(lista)):
				out = out + str(i+1)+'-'+lista[i]+'\n'
			conn.send(out)

		if(data[:2] == 'ES'): #Entrar em Sala
			aux = data.split(KEYCONTROLLER)
			user = usuario.usuario(aux[1],addr[0],conn)
			salas.adicionaUsuario(user,aux[2])


		atualizaNSalas()
#thread1()

def verificaComando(msg):
	comando = ''
	if msg == '': return None
	if msg[0]=='/':
		for i in msg:
			if i == ' ': break
			comando = comando + i;
		comando = comando[1:]
		if(comando=="listar"): return comando
		if(comando=="sair"): return comando
		if(comando=="ajuda"): return comando
		if(comando=="remover"): return comando
	return None
#VerificaComando()

def executaComando(comando, conn, ip):
	if(comando=="listar"): listar(ip,conn)
	if(comando=="sair"): sair(conn)
	if(comando=="ajuda"): ajuda(conn)
	if(comando=="remover"): revome()
#ececutaComando()

def listar(ip,conn):
	aux = ''
	lista = salas.listaUsuarios(ip)
	for i in lista:
		aux = aux + i + '\n'
	aux = 'LUSER-'+aux
	conn.send(aux)
#listar()

def sair(conn):
	conn.send(KEYCONTROLLER+"sair"+KEYCONTROLLER)
#sair()

def ajuda(conn):
	conn.send(KEYCONTROLLER+"textoAjuda"+KEYCONTROLLER)
#ajuda()

def remove():
	pass
#remove()

def parar():
	global t1_stop
	t1_stop.set()
	trocaStatus(2)
#parar()

def atualizaNSalas():
	numeroSalasLabel['text'] = salas.getNumSalas()


status = False
numeroSalas = 0
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
root.geometry('180x290')
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

NSL = Label(container2, text = 'Salas: ')
NSL.grid(row = 3, column = 0)

numeroSalasLabel = Label(container2, text = '0')
numeroSalasLabel.grid(row = 3, column = 1)

# Fim da GUI --------------------------------------------------------------------------

root.mainloop()



