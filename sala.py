class sala:
	def __init__(self, nome="", ID=0):
		self.nome = nome
		self.id = ID
		self.s = {}
		
	def adicionaConexao(self, s, nome,ip):
		if not nome in self.s:
			aux = ([s],ip)
			self.s[nome] = aux
		else:
			self.s[nome][0].append(s)
		print 'conectou',self.s

	def enviaMsg(self, nomeSala, msg, nome):
		msg = nome+': '+msg
		for i in self.s[nomeSala][0]:
			i.send(msg)

	def verificaSala(self, nomeSala):
		for nomeSala in self.s:
			return True
		return False

	def listaSalas(self):
		nomes = []
		for i in self.s:
			nomes.append(i)
		return list(set(nomes))