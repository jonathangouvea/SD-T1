import threading

class TupleSpace():
	def __init__(self):
		self._tuplas = []
		self._lock = threading.Lock()
		
	def put(self, *tupla):
		print("\t>> PUT {0}".format(tupla))
		with self._lock:
			self._tuplas.append(tupla)
		
	def get(self, *tupla):
		print("\t>> GET {0}".format(tupla))
		with self._lock:
			try:
				print(tupla[1])
				self._tuplas.remove(tupla[1])
				return tupla[1]
			except:
				return None
		
	def query(self, *tupla):
		print("\t>> QUERY {0}".format(tupla))
		resposta = []
		for t in self._tuplas:
			if self._match(t[1], tupla[1]):
				resposta.append(t)
			print(" ")
		return resposta
		
	def _match(self, t, tupla):
		print("\t\t>> MATCH {0} -> {1}".format(t, tupla), end = '\t')
		if t == tupla:
			return True
		if len(t) != len(tupla):
			return False
		for i in range(len(t)):
			if t[i] != tupla[i] and tupla[i] != None:
				return False
		print("[MATCHED]", end = '')
		return True
				 
		
