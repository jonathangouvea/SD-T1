from TupleSpace import *
from time import localtime, strftime

def tempo():
	return strftime('%m/%d - %H:%M', localtime())

class TSUser(TupleSpace):
	def __init__(self):
		TupleSpace.__init__(self)
		self.id = 1
		
	def addUser(self, username, nome):
		self.put(self, (self.id, username, nome))
		self.id += 1
		return self.id - 1
		
	def addUserId(self, id, username, nome):
		self.put(self, (id, username, nome))
		
	def getUser(self, username):
		T = self.queryUser(username)[0]
		return self.get(self, T)
		
	def queryUser(self, username):
		return self.query(self, (None, username, None))
		
class TSTopico(TupleSpace):
	def __init__(self):
		TupleSpace.__init__(self)
		self.id = 1
		
	def addTopico(self, titulo, autor, descricao):
		self.put(self, (self.id, titulo, autor, descricao, tempo()))
		self.id += 1
		return self.id - 1
		
	def addTopicoId(self, id, titulo, autor, descricao):
		self.put(self, (id, titulo, autor, descricao, tempo()))
		
	def getTopico(self, id):
		try:
			T = self.queryTopico(id)[0]
			return self.get(self, T)
		except:
			return
		
	def queryTopico(self, id):
		return self.query(self, (id, None, None, None, None))
		
	def queryTopicoAutor(self, nome):
		return self.query(self, (None, None, nome, None, None))
		
class TSComentario(TupleSpace):
	def __init__(self):
		TupleSpace.__init__(self)
		self.id = 1
		
	def addComentario(self, idTopico, autor, comentario):
		self.put(self, (idTopico, self.id, autor, comentario, tempo()))
		self.id += 1
		return self.id - 1
		
	def getComentario(self, id):
		try:
			T = self.queryComentarioTopico(id)[0]
			return self.get(self, T)
		except:
			return
			
	def getComentarioEspecifico(self, id):
		try:
			T = self.query(self, (None, id, None, None, None))[0]
			return self.get(self, T)
		except:
			return
		
	def queryComentarioTopico(self, idTopico):
		return self.query(self, (idTopico, None, None, None, None))
