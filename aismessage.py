class AISMessage :
	"""
		Cette classe permet de représenter un message AIS. On ne garde que les informations utiles.
	"""
	
	def __init__(self, horaire, typeMsg, mmsi, latitude, longitude, vitesse, cap, statut, tauxVirage) :	#constructeur
		self.horaire = horaire	#heure de réception du message
		self.typeMsg = typeMsg	#type de message AIS
		self.mmsi = mmsi	#identifiant MMSI du navire ayant émis ce message
		self.latitude = latitude	#la latitude à laquelle le message a été émis
		self.longitude = longitude #la longitude à laquelle le message a été émis
		self.vitesse = vitesse #la vitesse du navire (speedOverGround) au moment de l'émission
		self.cap = cap #le cap (trueHeading) du navire au moment de l'émission
		self.statut = statut #le statut de navigation du navire à l'émission (-1 si classe B car non présent dans le message)
		self.tauxVirage = tauxVirage #le taux du virage du navire (0 si classe B car non présent dans le message)
		self.intercalaire = False
		
	def __str__(self) : #méthode toString
		return  "{},{},{},{},{},{},{},{},{}\n".format(self.mmsi,self.typeMsg,self.horaire,self.latitude,self.longitude,self.vitesse,self.cap,self.statut,self.tauxVirage)

