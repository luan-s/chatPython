#encoding: utf-8
class usuario:
	def __init__(self, nome, ip, s):
		self.ip = ip
		self.nome = nome
		self.conn = s
