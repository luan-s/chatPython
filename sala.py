#encoding: utf-8
KEYCONTROLLER = '<ctrl>'
class sala:
	def __init__(self, nome="", ID=0):
		self.nome = nome
		self.id = ID
		self.s = {}
		
	def criaSala(self, user, nome, ip):
		if not nome in self.s:
			aux = ([user],ip)
			self.s[nome] = aux
			print 'Sala Criada: ',self.s
			return True
		return False

	def adicionaUsuario(self, user, nome):
			self.s[nome][0].append(user)
			#out = '\n"'+user.nome+'"\n'
			#self.enviaMsg(nome,out,'Entrou na sala')


	def enviaMsg(self, nomeSala, msg, nome):
		msg = nome+': '+msg
		for i in self.s[nomeSala][0]:
			i.conn.send(msg)

	def verificaSala(self, nomeSala):
		for nomeSala in self.s:
			return True
		return False

	def listaSalas(self):
		nomes = []
		print "Aqui: ",self.s
		for i in self.s:
			nomes.append(i)
		return list(set(nomes))

	def listaUsuarios(self,ip):
		nomes = []
		nomeSala = ''
		for i in self.s:
			for j in self.s[i][0]:
				if j.ip == ip:
					nomeSala = i

		for i in self.s[nomeSala][0]:
			nomes.append(i.nome)
		
		return nomes				

	def isAdmin(self, ip, nomeSala):
		if self.s[nomeSala][1] == ip:
			return True
		return False

	def removeUsuario(self, nome, nomeSala,conn):
		for i in range(len(self.s[nomeSala][0])):
			if self.s[nomeSala][0][i].nome == nome:
				self.s[nomeSala][0][i].conn.send(KEYCONTROLLER+"sair"+KEYCONTROLLER)
				self.s[nomeSala][0].pop(i)
			conn.send('ok')


	def getNumSalas(self):
		return len(self.s)
