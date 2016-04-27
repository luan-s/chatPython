#encoding: utf-8
import socket, ttk, threading
from Tkinter import *
import tkMessageBox


try:
	import winsound
except ImportError:
	import os
	def playsound(frequency,duration):
		os.system('beep -f %s -l %s'%(frequency,duration))
		os.system('beep -f %s -l %s'%(frequency,duration))
else:
	def playsound(frequency,duration):
		winsound.Beep(frequency,duration)
		winsound.Beep(frequency+100,duration+50)



def goServidor():
	'''
		Abre uma conexão com o servidor,
		caso de erro na conexão, é feita uma nova tentativa
		retorna o objeto Socket
	'''
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

def igBatePapo(titulo):
	'''
		Interface grafica da janeja "bate papo", onde é possivel enviar e
		receber menssagens.
	'''
	global root2
	global textoSala
	global inputTexto
	global scrollbar
	
	root2 = Tk()
	root2.geometry('380x335')
	root2.wm_title(titulo)
	root2.resizable(0,0)

	container0 = Frame(root2)
	container0.pack(padx = 10, pady = 10)

	scrollbar = Scrollbar(container0)
	scrollbar.pack(side=RIGHT, fill=Y)

	textoSala = Text(container0, width = 44, height = 15, wrap = WORD, yscrollcommand = scrollbar.set)
	textoSala.pack()

	scrollbar.config(command = textoSala.yview)

	container1 = Frame(root2)
	container1.pack(padx = 10)

	inputTexto = Entry(container1, width = 25)
	inputTexto.grid(row = 1, column = 0)
	inputTexto.bind('<Return>', enviarMensagem)
	inputTexto.focus_set()

	labelEspacadora1 = Label(container1, text = '   ')
	labelEspacadora1.grid(row = 1, column = 1)

	enviarMsgButton = Button(container1, width = 10, text = 'Enviar', command = enviarMensagem)
	enviarMsgButton.grid(row = 1, column = 2)

	#Emotes ------------------------------------------------------------------------------------------------

	container2 = Frame(root2)
	container2.pack(pady = 10)

	emoteFelizButton = Button(container2, width = 4, text = '(•‿•)', command = felizPressed)
	emoteFelizButton.grid(row = 2, column = 0)

	labelEspacadora2 = Label(container2, text = '  ')
	labelEspacadora2.grid(row = 2, column = 1)

	emoteTristeButton = Button(container2, width = 4, text = '(>▂<)', command = tristePressed)
	emoteTristeButton.grid(row = 2, column = 2)

	labelEspacadora3 = Label(container2, text = '  ')
	labelEspacadora3.grid(row = 2, column = 3)

	emoteRaivaButton = Button(container2, width = 4, text = '(¬_¬)', command = raivaPressed)
	emoteRaivaButton.grid(row = 2, column = 4)

	labelEspacadora4 = Label(container2, text = '  ')
	labelEspacadora4.grid(row = 2, column = 5)

	emoteCreepyButton = Button(container2, width = 4, text = '(ಠᴗಠ)', command = creepyPressed)
	emoteCreepyButton.grid(row = 2, column = 6)

	labelEspacadora5 = Label(container2, text = '  ')
	labelEspacadora5.grid(row = 2, column = 7)

	emoteCryButton = Button(container2, width = 4, text = '(ಥ_ಥ)', command = cryPressed)
	emoteCryButton.grid(row = 2, column = 8)

	#Fim emotes --------------------------------------------------------------------------------------------

	root2.mainloop()
#igBatePapo()

def tristePressed():
	global inputTexto
	inputTexto.insert(END, '(>▂<)')
	inputTexto.focus_set()
#tristePressed()

def felizPressed():
	global inputTexto
	inputTexto.insert(END, '(•‿•)')
	inputTexto.focus_set()
#felizPressed()

def raivaPressed():
	global inputTexto
	inputTexto.insert(END, '(¬_¬)')
	inputTexto.focus_set()
#raivaPressed()

def creepyPressed():
	global inputTexto
	inputTexto.insert(END, '(ಠᴗಠ)')
	inputTexto.focus_set()
#creepyPressed()

def cryPressed():
	global inputTexto
	inputTexto.insert(END, '(ಥ_ಥ)')
	inputTexto.focus_set()
#cryPressed()

def enviarMensagem(arg1=''):
	'''
		Abre uma conexão com o servidor, envia a mensagem EM (enviar mensage) para ele,
		em seguida recebe uma confirmação do servidor, caso a mensagem de confirmação for
		alguma palavra de controle (sair, ajuda, listar ou romover) é a execução é encaminhada
		para uma função especifica.
	'''
	global inputTexto
	global textoSala
	global nomeString
	global nomeSalaString
	global saiu

	msg = inputTexto.get()

	if msg == '' or saiu == True:
		return

	inputTexto.delete(0, len(msg))
	
	s = goServidor()
	MESSAGE = "EM"+KEYCONTROLLER+nomeString+KEYCONTROLLER+nomeSalaString+KEYCONTROLLER+msg

	s.send(MESSAGE.encode('utf8'))
	data = s.recv(BUFFER_SIZE)
	print root2.focus_get()
	if data == KEYCONTROLLER+"sair"+KEYCONTROLLER : 
		root2.destroy()
		root.deiconify()

	if data == KEYCONTROLLER+"textoAjuda"+KEYCONTROLLER: 
		textoSala.insert(END, textoAjuda + '\n')
		textoSala.see(END)

	if(data[0]=='L' and data[1]=='U'):
		data = data.split("LUSER-")
		textoSala.insert(END, 'Usuarios na sala:\n' + data[1] + '\n')
		textoSala.see(END)

	if data == KEYCONTROLLER+'isNotAdm'+KEYCONTROLLER:
		textoSala.insert(END, "\nVocê não é o administrador da sala!\n")
		textoSala.see(END)	

	s.close()
#enviarMensagem()

def entrarSala():
	'''
		Abre uma conexão com o servidor, envia a mensagem ES (entrar na sala) para ele e 
		recebe uma confirmação do servidor, em seguida fica esperando mensagens do servidor
	    através de thread.
	'''
	global nomeString
	global nomeSalaString
	global t2_stop
	global root2

	MESSAGE = "ES" + KEYCONTROLLER + nomeString + KEYCONTROLLER + nomeSalaString
	s = goServidor()
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)

	if data == KEYCONTROLLER+'usuarioInvalido'+KEYCONTROLLER: 
		root.deiconify()
		exibirMensagem("Username já utilizado!", "Erro")
	else:
		titulo = "Sala: "+nomeSalaString+" | Usuario: "+nomeString

		# Esta thread cuida de atualizar o campo onde as mensagens da sala aparecem
		t2_stop = threading.Event()
		t1 = threading.Thread(target = threadCaixaMensagens, args = (s, t2_stop))
		t1.start()

		# Cria a janela do bate papo
		igBatePapo(titulo)

#entrarSala()

def criaSala():
	'''
		Abre uma conexão com o servidor, envia a mensagem CS (criar sala) para ele,
		em seguida recebe uma confirmação do servidor, caso a mensagem de confirmação for
		sala invalida (salaInvalida) é porque a sala já existe. 
		para uma funcção especifica. 
	'''
	global nomeString
	global nomeSalaString
	global root
	global t2_stop

	MESSAGE = "CS"+KEYCONTROLLER+nomeString+KEYCONTROLLER+nomeSalaString
	s = goServidor()
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)

	titulo = "Sala: "+nomeSalaString+" | Usuario: "+nomeString

	if data == KEYCONTROLLER+'salaInvalida'+KEYCONTROLLER: 
		root.deiconify()
		exibirMensagem("A sala já existe!", "Erro")
	else:
		# Esta thread cuida de atualizar o campo onde as mensagens da sala aparecem
		t2_stop = threading.Event()
		t1 = threading.Thread(target = threadCaixaMensagens, args = (s, t2_stop))
		t1.start()

		# Cria a janela do bate papo
		igBatePapo(titulo)
	
#criaSala()

def threadCaixaMensagens(s, eventoDeParada):
	'''
		Função que escuta as mensagens digitadas pelo usuario
	'''
	global textoSala
	global t2_stop
	global root2
	global scrollbar
	global saiu
	global root

	while not eventoDeParada.is_set():
		if saiu: break
		data = s.recv(BUFFER_SIZE)
		

		if data == KEYCONTROLLER+'sair'+KEYCONTROLLER: 
			s.send("tchau")
			saiu = True
			t2_stop.set()
			break
		else:
			if(data.split(" ")[1].split(':')[0] != nomeString):
				t4 = threading.Thread(target = playsound, args = (500,100))
				t4.start()
			textoSala.insert(END, data + '\n')
			textoSala.see(END)	
#threadCaixaMensagens()

def exibirMensagem(mensagem, titulo):
	'''
		Exibe uma caixa de diálogo genérica, configurada pelos parâmetros
	'''
	root = Tk()
	root.geometry('170x60')
	root.wm_title(titulo)

	container0 = Frame(root)
	container0.pack(padx = 10, pady = 13)

	ipServidorLabel = Label(container0, text = mensagem)
	ipServidorLabel.grid(row = 0, column = 0)
	
	root.mainloop()
#exibirMensagem()

def getSalas():
	'''
		Recebe do servidor os nomes numerados de todas as salas já criadas.
	'''
	MESSAGE = "LS"
	s = goServidor()
	s.send(MESSAGE)
	data = s.recv(BUFFER_SIZE)

	return data
#GetSalas()

def getNumeroSalas():
	'''
		Abre uma conexão para o servidor, e recebe o numero de salas existentes
	'''
	MESSAGE = "NS"
	s = goServidor()
	s.send(MESSAGE)
	s.settimeout(1)
	data = s.recv(BUFFER_SIZE)

	return int(data)
#GetNumeroSalas

def criarSalaSelected():
	'''
		Verificar se a checkBox "criaSala" esta selecionada, 
		caso esteja desabilida as opções do "EntrarSala"	
	'''
	global op
	nomeSalaCampo['state'] = NORMAL
	nomeUsuarioCampo1['state'] = NORMAL
	nomeUsuarioCampo2['state'] = DISABLED
	salasComboBox['state'] = DISABLED
	
	btnOk['text'] = 'Criar'
	btnOk.grid(row = 6, column = 0)
	op = 1
#criarSalasSelected()

def entrarSalaSelected():
	'''
		Verificar se a checkBox "EntrarSala" esta selecionada, 
		caso esteja desabilida as opções do "criarSala"	
	'''
	global op
	global listasComboBox
	nomeSalaCampo['state'] = DISABLED
	nomeUsuarioCampo1['state'] = DISABLED
	nomeUsuarioCampo2['state'] = NORMAL
	salasComboBox['state'] = NORMAL

	if (getNumeroSalas() > 0):
		aux = getSalas().split('\n')
		aux.pop(len(aux)-1)
		salasComboBox['values'] = aux

	btnOk['text'] = 'Entrar'
	btnOk.grid(row = 6, column = 0)
	op = 2
#entrarSalaSelected()

def setIp():
	'''
		"Seta" o ip digitado na variavel de controle do servidor
	'''
	global TCP_IP
	global root1

	TCP_IP = ipServidorCampo.get()
	print TCP_IP
	root1.destroy()
#setIp()

def obtemIpServidor():
	'''
		Exibe uma caixa de texto perguntando o ip do servidor
		em seguida chama a função acima
	'''
	global root1
	global ipServidorCampo

	root1 = Tk()
	root1.resizable(0,0)
	root1.geometry('360x60')
	root1.wm_title('Chat')

	container0 = Frame(root1)
	container0.pack(padx = 10, pady = 13)

	ipServidorLabel = Label(container0, text = 'IP Servidor:       ')
	ipServidorLabel.grid(row = 0, column = 0)

	ipServidorCampo = Entry(container0)
	ipServidorCampo.grid(row = 0, column = 1)

	ipServidorCampo.focus_set()

	labelEspacadora = Label(container0, text = '   ')
	labelEspacadora.grid(row = 0, column = 2)

	dialogOk = Button(container0, text = 'OK', command = setIp)
	dialogOk.grid(row = 0, column = 3)
	
	root1.mainloop()
#obtemIpServidor()

def okPressed():
	'''
		Função chamada quando o botão ok é pressionado. Identifica qual radio button foi 
		selecionado no menu e direciona a linha de execução do programa para a funcionalidade
		escolhida.
	'''
	global nomeString
	global nomeSalaString
	global root
	global op
	global saiu

	saiu = False

	if (op == 1): #Clicou em "Criar sala"
		nomeString = nomeUsuarioCampo1.get()
		nomeSalaString = nomeSalaCampo.get()
		root.withdraw()
		criaSala()
	else:
		nomeString = nomeUsuarioCampo2.get()
		root.withdraw()
		entrarSala()
#okPressed()

def salaSelecionada(event):
	'''
		Função chamada quando uma sala é selecionada no ComboBox. "Seta" o nome da sala
		na variável global correspondente.
	'''
	global nomeSalaString
	nomeSalaString = salasComboBox.get()[2:]
#salaSelecionada()

def main():
	'''
		Método Main primeiro a ser executado pelo programa, define as propriedades da
		janela menu e exibe na tela.
	'''
	global nomeSalaCampo
	global nomeUsuarioCampo1
	global nomeUsuarioCampo2
	global salasComboBox
	global btnOk
	global root

	obtemIpServidor()

	root = Tk()
	root.geometry('330x250')
	root.wm_title('Menu')
	root.resizable(0,0)

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

	listaSalasLabel = Label(container4, text = 'Sala:                ')
	listaSalasLabel.grid(row = 5, column = 0)

	salasComboBox = ttk.Combobox(container4, width = 18, state = DISABLED)
	salasComboBox.bind("<<ComboboxSelected>>", salaSelecionada)
	salasComboBox.grid(row = 5, column = 1)

	container5 = Frame(root)
	container5.pack(pady = 25, padx = 30)

	btnOk = Button(container5, width = 15,  command = okPressed)
	mainloop()
#Main()

# Declarando variáveis globais
nomeSalaCampo = Entry
nomeUsuarioCampo1 = Entry
nomeUsuarioCampo2 = Entry
textoSala = Text
inputTexto = Entry
salasComboBox = ttk.Combobox
ipServidorCampo = Entry
scrollbar = Scrollbar
nomeSalaString = ''
nomeString = ''

root = Tk
root1 = Tk
root2 = Tk

saiu = False
TCP_IP = ''
btnOk = Button
op = 0
t2_stop = threading.Event()
# Fim variáveis globais

KEYCONTROLLER = '<ctrl>'
TCP_PORT = 8000
BUFFER_SIZE = 2048


#Texto usado no comendo /ajuda
textoAjuda = '''\nComandos:\n
	\n    /listar -> lista os usuários presentes na sala
	\n    /remover <nome> -> remove um usuário da sala. Só pode ser usado pelo admin
	\n    /sair -> sai da sala atual
	\n    /ajuda -> mostra o menu de ajuda\n\n'''
#textoAjuda

main()




