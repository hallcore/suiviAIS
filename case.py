class Case :

	"""
		Cette classe permet de représenter les cases géographiques.
	"""
	def __init__(self, id, x, y, nord, ouest, sud, est) :#constructeur
		self.id = id
		self.x = x
		self.y = y
		self.nord = nord
		self.ouest =  ouest
		self.sud = sud
		self.est = est
		self.msgTheo = 0 #nombre de messages théoriquement reçus pour tous les navires dans cette case.
		self.msgRecu = 0 #nombre de messages effectivement reçus pour tous les navires dans cette case.
		self.nbSequence = 0 #nombre de séquences différentes

	def __str__(self) :#méthode toString
		return "{},{},{},{},{},{},{},{},{}\n".format(self.id,self.x,self.y,self.nord,self.ouest,self.sud,self.est,self.msgTheo,self.msgRecu,self.nbSequence)
