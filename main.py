#encoding: utf-8
import sala, socket, ttk
from Tkinter import *

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
#GoServidor()

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
#GetSalas()

def getNumeroSalas():
	MESSAGE = "NS"
	s = goServidor()
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)

	return int(data)
#GetNumeroSalas

textoAjuda = '''\nComandos:\n
	\n    /listar -> lista os usuários presentes na sala
	\n    /remover -> remove um usuário da sala. Só pode ser usado pelo admin
	\n    /sair -> sai da sala atual'
	\n    /ajuda -> mostra o menu de ajuda\n\n'''
#textoAjuda

def criarSalaSelected():
	global op
	nomeSalaCampo['state'] = NORMAL
	nomeUsuarioCampo1['state'] = NORMAL
	nomeUsuarioCampo2['state'] = DISABLED
	salasComboBox['state'] = DISABLED
	
	btnOk['text'] = 'Criar'
	btnOk.grid(row = 6, column = 1)
	op = 1
#criarSalasSelected()

def entrarSalaSelected():
	global op
	global listasComboBox
	nomeSalaCampo['state'] = DISABLED
	nomeUsuarioCampo1['state'] = DISABLED
	nomeUsuarioCampo2['state'] = NORMAL
	salasComboBox['state'] = NORMAL

	print getNumeroSalas()
	if (getNumeroSalas() > 0):
		salasComboBox['values'] = getSalas().split('\n')

	btnOk['text'] = 'Entrar'
	btnOk.grid(row = 6, column = 1)
	op = 2
#entrarSalaSelected()

def okPressed():
	print op
#okPressed()

def main():
	global nomeSalaCampo
	global nomeUsuarioCampo1
	global nomeUsuarioCampo2
	global salasComboBox
	global btnOk

	root = Tk()
	root.geometry('350x250')
	root.wm_title('Menu')

	container = Frame(root)
	container.pack(anchor = W, padx = 20, pady = 10)

	radioButtonCriarSala = Radiobutton(container, text="Criar sala", value=2, command = criarSalaSelected)
	radioButtonCriarSala.grid(row = 0, column = 0)

	container2 = Frame(root)
	container2.pack(anchor = W, padx = 35)

	nomeSalaLabel = Label(container2, text = '      Nome da sala: ')
	nomeSalaLabel.grid(row = 1, column = 0)

	nomeSalaCampo = Entry(container2, state = DISABLED)
	nomeSalaCampo.grid(row = 1, column = 1)

	nomeUsuarioLabel1 = Label(container2, text = 'Seu nome: ')
	nomeUsuarioLabel1.grid(row = 2, column = 0)

	nomeUsuarioCampo1 = Entry(container2, state = DISABLED)
	nomeUsuarioCampo1.grid(row = 2, column = 1)

	container3 = Frame(root)
	container3.pack(anchor = W, padx = 20, pady = 10)

	radioButtonEntrarSala = Radiobutton(container3, text="Entrar em sala", value=1, command = entrarSalaSelected)
	radioButtonEntrarSala.grid(row = 3, column = 0)

	container4 = Frame(root)
	container4.pack(anchor = W, padx = 55)

	nomeUsuarioLabel2 = Label(container4, text = 'Seu nome:       ')
	nomeUsuarioLabel2.grid(row = 4, column = 0)

	nomeUsuarioCampo2 = Entry(container4, state = DISABLED)
	nomeUsuarioCampo2.grid(row = 4, column = 1)

	listaSalasLabel = Label(container4, text = 'Sala:                 ')
	listaSalasLabel.grid(row = 5, column = 0)

	salasComboBox = ttk.Combobox(container4, width = 17, state = DISABLED)
	salasComboBox.grid(row = 5, column = 1)

	container5 = Frame(root)
	container5.pack(pady = 25)

	btnOk = Button(container5, width = 15,  command = okPressed)

	

	'''while True:
		print "1-Criar Sala"
		print "2-Enviar texto para uma sala"
		print "3-Entrar em uma sala"
		op = int(raw_input("Opcao:"))

		if op==1 :
			criaSala()
		if op==2 :
			envia()
		if op==3 :
			entrar()'''
	mainloop()
	
#Main()

# Declarando variáveis globais
nomeSalaCampo = Entry
nomeUsuarioCampo1 = Entry
nomeUsuarioCampo2 = Entry
salasComboBox = ttk.Combobox
btnOk = Button
op = 0
# Fim variáveis globais

main()


