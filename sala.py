#encoding: utf-8
KEYCONTROLLER = '<ctrl>'
from datetime import datetime
class sala:
	def __init__(self, nome="", ID=0):
		self.nome = nome
		self.id = ID
		self.s = {}
		
	def criaSala(self, user, nome, ip):
		if not nome in self.s:
			aux = [[user],user]
			self.s[nome] = aux
			print 'Sala Criada: ',self.s
			return True
		return False

	def adicionaUsuario(self, user, nome):
			self.s[nome][0].append(user)
			out = '"'+user.nome+'"'
			self.enviaMsg(nome,out,'Entrou na sala')

	def enviaMsg(self, nomeSala, msg, nome):
		timeStamp = self.getHoraFormatada()
		msg = timeStamp + nome + ': ' + msg
		for i in self.s[nomeSala][0]:
			i.conn.send(msg)

	def getHoraFormatada(self):
		now = datetime.now()

		if now.hour < 10:
			horaString = '0' + str(now.hour)
		else:
			horaString = str(now.hour)

		if now.minute < 10:
			minutoString = '0' + str(now.minute)
		else:
			minutoString = str(now.minute)

		timeStamp = '['+horaString+':'+minutoString+'] '

		return timeStamp

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

	def isAdmin(self, ip, nome,nomeSala):
		if self.s[nomeSala][1].ip == ip and nome == self.s[nomeSala][1].nome:
			return True
		return False

	def removeUsuario(self, nome, nomeSala,conn):
		for i in range(len(self.s[nomeSala][0])):
			if self.s[nomeSala][0][i].nome == nome:
				self.s[nomeSala][0][i].conn.send(KEYCONTROLLER+"sair"+KEYCONTROLLER)
				self.s[nomeSala][0].pop(i)
				nome = '"'+nome+'"'
				self.enviaMsg(nomeSala, nome, 'Saiu da sala')

			conn.send('ok')

	def nomeSalaByAdim(self, ip):
		for i in self.s:
			if self.s[i][1].ip == ip:
				return i
		return None

	def nomeSalaByUser(self, ip, nome):
		for i in self.s:
			for j in self.s[i][0]:
				if j.ip == ip and j.nome == nome:
					return i
		return None

	def getNumSalas(self):
		return len(self.s)

	def usuarioInSala(self, nome, nomeSala):
		for i in self.s[nomeSala][0]:
			if nome == i.nome:
				return 1
		return 0

	def removeTodos(self,nomeSala):
		print self.s[nomeSala][0]
		for i in self.s[nomeSala][0]:
			i.conn.send(KEYCONTROLLER+"sair"+KEYCONTROLLER)

		self.s[nomeSala][0] = []
		self.s.pop(nomeSala)
