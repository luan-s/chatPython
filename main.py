import sala
import socket
import sala

KEYCONTROLLER = 'KEYCONTROLLER'
TCP_IP = socket.gethostbyname(socket.gethostname())
TCP_PORT = 8000
BUFFER_SIZE = 2048

def goServidor():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sair = False
	while not sair:
		try:
			s.connect((TCP_IP, TCP_PORT))
			sair = True
		except :
			sair = False
	return s


def criaSala():

	


	nome = raw_input("Seu nome:")
	nomeSala = raw_input("Nome da sala:")

	MESSAGE = "LS"
	s = goServidor()
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)
	s.close()

	if(data!=""):
		print 'data: '+data
		salas = data.split('\n')

		for i in range(len(salas)):
			salas[i] = salas[i][2:]
		if nomeSala in salas:
			op = int(raw_input("A sala ja existe, deseja entrar nela ?\n1-Sim\n2-Nao"))
			if(op==2): return


	MESSAGE = "CS"+KEYCONTROLLER+nome+KEYCONTROLLER+nomeSala
	s = goServidor()
	s.send(MESSAGE)
	while True:
		data = s.recv(BUFFER_SIZE)
		print data
# criaSala()

def separaNomeSala(lista, op):
	for i in lista:
		input()
		if(op in i):
			return i[2:]

#separaNomeSala():

def envia():
	nome = raw_input("Seu nome: ")

	MESSAGE = "LS"
	s = goServidor()
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)
	print "Salas:"
	print data
	sala = raw_input("Escolha uma sala: ")
	sala = separaNomeSala(data.split('\n'),sala)
	
	while True:
		msg = raw_input("Messsagem: ")
		s = goServidor()
		MESSAGE = "EM"+KEYCONTROLLER+nome+KEYCONTROLLER+sala+KEYCONTROLLER+msg
		s.send(MESSAGE)
		data  = s.recv(BUFFER_SIZE)
		if data == 'sair' : break
		if(data[0]=='L' and data[1]=='U'):
			data = data.split("LUSER-")
			print(data[1])
		s.close()
#Envia()


def main():
	while True:
		print "1-Criar Sala"
		print "2-Enviar texto para uma sala"
		op = int(raw_input("Opcao:"))

		if op==1 :
			criaSala()
		if op==2 :
			envia()
#Main()
main()