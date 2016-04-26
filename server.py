#encoding: utf-8
import socket, sala, threading, time, usuario, os
from Tkinter import *

KEYCONTROLLER = '<ctrl>'

def trocaStatus(codBotao):
	'''
		Função que troca o Status da label do servidor 
		para rodando ou Parado.
	'''
	global status
	global statusLabel

	print codBotao
	if not status  and codBotao == 1:
		statusLabel['text'] = 'Rodando'
		statusLabel['fg'] = '#0C0'
		status = True
	elif status and codBotao == 2:
		statusLabel['text'] = 'Parado'
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
	'''
		Caso o servidor esteja com o estado "rodando", a função mostra o ip do Servidor,
		e a  porta.
		Além disso, a partir desse momento, fica "escutando" qualquer mensagem que possa
		vir dos clientes conectados a ele, que pode ser:

		CS: Criar Sala
			o servidor verifica se a sala já existe, se sim é retornado uma msg de erro
			se não, é criada uma nova sala com o nome informado pelo cliente, o cliente 
			que criou, é setado como adm da sala.

		EM: Enviar mensagem
			Recebe o nome da sala, o nome do usuario e a mensagem a ser enviada, a função 
			verifica se a mensagem é um comando especial (/sair, /ajuda, /remover ou /listar)
			caso seja um desses é feito o encaminhamento pra uma função que vai tratar o comando
			caso não seja, a mensagem é enviada para todos que estão na sala.

		LS: Listar Salas
			Envia para o cliente o nome de todas as salas já criadas.

		ES:
			Recebe do usuario o nome dele, e a sala que ele deseja entrar
			verifica se já existe um usuario com aquele nome na sala, se sim 
			é retornado uma msg de erro, se não, o usuário é adicionado na sala
			que ele escolheu.

		NS:
			Retorna o numero de salas existentes.

	'''
	global numeroSalasLabel
	global numeroSalas
	
	ipLabel['text'] = TCP_IP
	portaLabel['text'] = TCP_PORT
	while not eventoDeParada.is_set():
		#print 'Thread 1 rodando \n'
		s.listen(1)
		conn, addr = s.accept()

		data = conn.recv(BUFFER_SIZE)

		print "recebeu : " + data

		if(data[:2] == 'CS'): #Cria Sala
			aux = data.split(KEYCONTROLLER)
			user = usuario.usuario(aux[1],addr[0],conn)
			if not salas.criaSala(user,aux[2],addr[0]):
				msg = KEYCONTROLLER+'salaInvalida'+KEYCONTROLLER
				conn.send(msg)
			else:
				conn.send('ok')

		if(data[:2] == 'EM'): #Envia Msg
			msg = data.split(KEYCONTROLLER)
			comando = verificaComando(msg[3])

			if comando != None:
				executaComando(comando,conn,addr[0],msg)
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

			if salas.usuarioInSala(aux[1],aux[2]):
				msg = KEYCONTROLLER+'usuarioInvalido'+KEYCONTROLLER
				conn.send(msg)
			else:
				user = usuario.usuario(aux[1],addr[0],conn)
				salas.adicionaUsuario(user,aux[2])

		if(data[:2] == 'NS'): #Numero de Salas
			conn.send(str(salas.getNumSalas()))

		atualizaNSalas()
#thread1()

def verificaComando(msg):
	'''
		Função que verifica se a mensagem enviada pelo cliente é uma comando.
		retorna uma string contendo o comando caso seja um, caso não seja retorna None.
	'''
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

def executaComando(comando, conn, ip,msg):
	'''
		Recebe o comando e encaminha para a função de tratamento.
	'''
	if(comando=="listar"): listar(ip,conn)
	if(comando=="sair"): sair(conn, comando, ip,msg)
	if(comando=="ajuda"): ajuda(conn)
	if(comando=="remover"): remove(conn, comando,ip,msg)
#ececutaComando()

def listar(ip,conn):
	'''
		Lista todos usuarios dentro de uma sala
	'''
	aux = ''
	lista = salas.listaUsuarios(ip)
	for i in lista:
		aux = aux + i + '\n'
	aux = 'LUSER-'+aux
	conn.send(aux)
#listar()

def sair(conn,comando,ip,msg):
	'''
		Remove o usuario que enviou a mensagem da sala.
	'''
	nomeSala = salas.nomeSalaByUser(ip,msg[1])
	'''if salas.isAdmin(ip,msg[1],msg[2]): 
		salas.removeTodoss(nomeSala)'''
		
	conn.send(KEYCONTROLLER+"sair"+KEYCONTROLLER)
	salas.removeUsuario(msg[1],nomeSala,conn)

#sair()

def ajuda(conn):
	'''
		Exibe o texto de ajuda
	'''
	conn.send(KEYCONTROLLER+"textoAjuda"+KEYCONTROLLER)
#ajuda()

def remove(conn,comando,ip,msg ):
	'''
		Verifica se o usuario é o admin, se sim retira um usuario da sala.
	'''
	if not salas.isAdmin(ip,msg[1],msg[2]):
		conn.send(KEYCONTROLLER+"isNotAdm"+KEYCONTROLLER)
	else:
		nomeSala = salas.nomeSalaByAdim(ip)
		if nomeSala == None: print "brecou"
		msg =  msg[3].split(" ")[1]
		salas.removeUsuario(msg,nomeSala,conn)
#remove()

def parar():
	global t1_stop
	t1_stop.set()
	trocaStatus(2)
#parar()

def atualizaNSalas():
	'''
		atualiza a label com o numero coorente de salas.
	'''
	numeroSalasLabel['text'] = salas.getNumSalas()
#atualizaNSalas()

if os.name != "nt":
    import fcntl
    import struct

    def get_interface_ip(ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(s.fileno(), 0x8915, struct.pack('256s', ifname[:15]))[20:24])

def getIP():
    ip = socket.gethostbyname(socket.gethostname())
    if ip.startswith("127.") and os.name != "nt":
        interfaces = ["eth0","eth1","eth2","wlan0","wlan1","wifi0","ath0","ath1","ppp0",]
        for ifname in interfaces:
            try:
                ip = get_interface_ip(ifname)
                break
            except IOError:
                pass
    return ip
#getIP()

status = False
numeroSalas = 0
TCP_IP = getIP()
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
root.wm_title('Servidor')
root.resizable(0,0)
container = Frame(root)
container.pack()

btnStart = Button(container)
btnStart.configure(text = 'Iniciar', padx = 30, pady = 10, command = iniciaThread)
btnStart.configure(background='#CFD8DC')
btnStart.pack(pady = 30)
btnStop = Button(container)
btnStop.configure(text = 'Parar', padx = 30, pady = 10, command = parar)
btnStop.configure(background='#CFD8DC')
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

iniciaThread()

root.mainloop()

