class sala:
	def __init__(self, nome="", ID=0):
		self.nome = nome
		self.id = ID
		self.s = []
		
	def adicionaConexao(self, s, nome):
		self.s.append([s,nome])
		print 'conectou',self.s

	def enviaMsg(self, nomeSala, msg, nome):
		msg = nome+': '+msg
		for i in self.s:
			if i[1]==nomeSala:
				i[0].send(msg)

	def verificaSala(self, nomeSala):
		for i in self.s:
			if i[1]==nomeSala:
				return True
		return False

	def listaSalas(self):
		nomes = []
		for i in self.s:
			nomes.append(i[1])
		return list(set(nomes))