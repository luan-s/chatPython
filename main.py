#encoding: utf-8
import sala
import socket
import time

KEYCONTROLLER = '<ctrl>'
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

	MESSAGE = "CS"+KEYCONTROLLER+nome+KEYCONTROLLER+nomeSala
	s = goServidor()
	s.send(MESSAGE)
	while True:
		data = s.recv(BUFFER_SIZE)

		if data == KEYCONTROLLER+'sair'+KEYCONTROLLER: break
		if data == KEYCONTROLLER+'salaInvalida'+KEYCONTROLLER: 
			print "Ja existe uma sala com esse nome!\n"
			break

		print data
# criaSala()

def separaNomeSala(lista, op):
	for i in lista:
		if(op in i):
			return i[2:]

#separaNomeSala():

def envia():
	nome = raw_input("Seu nome: ")

	data = getSalas()
	print data
	sala = raw_input("Escolha uma sala: ")
	sala = separaNomeSala(data.split('\n'),sala)
	
	while True:
		msg = raw_input("Mensagem: ")
		s = goServidor()
		MESSAGE = "EM"+KEYCONTROLLER+nome+KEYCONTROLLER+sala+KEYCONTROLLER+msg
		s.send(MESSAGE)
		data  = s.recv(BUFFER_SIZE)
		
		if data == KEYCONTROLLER+'sair'+KEYCONTROLLER : break

		if data == KEYCONTROLLER+'textoAjuda'+KEYCONTROLLER: print textoAjuda

		if(data[0]=='L' and data[1]=='U'):
			data = data.split("LUSER-")
			print(data[1])

		s.close()
#Envia()

def entrar():
	nome = raw_input("Seu nome:")

	data = getSalas()
	print data
	sala = raw_input("Escolha uma sala: ")
	sala = separaNomeSala(data.split('\n'),sala)

	MESSAGE = "ES"+KEYCONTROLLER+nome+KEYCONTROLLER+sala
	s = goServidor()
	s.send(MESSAGE)
	while True:
		data = s.recv(BUFFER_SIZE)

		if data == KEYCONTROLLER+'sair'+KEYCONTROLLER: break
		if data == KEYCONTROLLER+'salaInvalida'+KEYCONTROLLER: 
			print "Ja existe uma sala com esse nome!\n"
			break

		print data
	
#Envia()

def getSalas():
	MESSAGE = "LS"
	s = goServidor()
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)

	return data




textoAjuda = '''\nComandos:\n
	\n    /listar -> lista os usuários presentes na sala
	\n    /remover -> remove um usuário da sala. Só pode ser usado pelo admin
	\n    /sair -> sai da sala atual'
	\n    /ajuda -> mostra o menu de ajuda\n\n'''

def main():
	while True:
		print "1-Criar Sala"
		print "2-Enviar texto para uma sala"
		print "3-Entrar em uma sala"
		op = int(raw_input("Opcao:"))

		if op==1 :
			criaSala()
		if op==2 :
			envia()
		if op==3 :
			entrar()
#Main()

main()