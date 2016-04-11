class sala:
	def __init__(self, nome="", ID=0):
		self.nome = nome
		self.id = ID
		self.s = {}
		
	def adicionaConexao(self, user, nome, ip):
		if not nome in self.s:
			aux = ([user],ip)
			self.s[nome] = aux
		else:
			self.s[nome][0].append(user)
		print 'conectou',self.s

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



	def isAdmin(seld, ip, nomeSala):
		if self.s[nomeSala][1] == ip:
			return True
		return False
