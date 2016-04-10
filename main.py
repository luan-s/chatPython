import sala
import socket
import sala

KEYCONTROLLER = 'KEYCONTROLLER'
TCP_IP = '127.0.0.1'
TCP_PORT = 8000
BUFFER_SIZE = 2048

def goServidor():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((TCP_IP, TCP_PORT))
	return s

def criaSala():
	nome = raw_input("Nome da sala:")
	MESSAGE = "CS"+nome
	s = goServidor()
	s.send(MESSAGE)
	while True:
		data = s.recv(BUFFER_SIZE)
		print data
# criaSala()

def separaNomeSala(lista, op):
	for i in lista:
		if(op in i):
			return i[2:]

#separaNomeSala():

def envia():
	TCP_IP = '127.0.0.1'
	TCP_PORT = 8000
	BUFFER_SIZE = 2048
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
		MESSAGE = "EM"+KEYCONTROLLER+nome+KEYCONTROLLER+sala+KEYCONTROLLER+msg
		s = goServidor()
		s.send(MESSAGE)
	s.close()
#Envia()


def main():
	print "1-Criar Sala"
	print "2-Entrar em uma sala"
	op = int(raw_input("Opcao:"))

	if op==1 :
		criaSala()
	if op==2 :
		envia()
#Main()
main()