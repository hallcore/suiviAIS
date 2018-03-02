from aismessage import AISMessage
from grille import Grille
from case import Case
from navcase import NavCase

class Mesure :
	"""
		Cette classe modélise les données sur lesquelles on travaille. Elle comprend les messages et la grille.
	"""
	
	def __init__(self) :	#constructeur
		self.balise = "inconnu"	#le nom de la balise réceptrice
		
		self.tabNavMsg = dict()	#le dictionnaire regroupant les messages par navire
		self.grille = None
		self.tabNavCase = dict()
		
	def ajoutMsg(self,m) :	#Cette méthode permet d'ajouter un message au dictionnaire pour le navire correspondant. Si celui-ci n'existe pas déjà, il est créé.
		if(m.mmsi not in self.tabNavMsg) :
			self.tabNavMsg[m.mmsi] = list()
		self.tabNavMsg[m.mmsi].append(m)
	
	def triHoraireNavMsg(self) : #Cette méthode permet de s'assurer que les messages sont triés par ordre chronologique
		for cle in self.tabNavMsg :	#pour chaque navire du dictionnaire
			sorted(self.tabNavMsg[cle], key=lambda aismessage: aismessage.horaire)

	def getListNav(self) :
		tab = list()
		for key in self.tabNavMsg :
			tab.append(key)
		
		return tab
	
	def getNbMsgNav(self) :
		tab = dict()
		for key in self.tabNavMsg :
			tab[key] = len(self.tabNavMsg[key])
		
		return tab

	def createGrid(self,param) :
		self.grille = Grille(param)
	
	def sortByCase(self) :
		for n in self.tabNavMsg :
			cpt=0
			bool = False
			oldMsg=None
			oldId=-1
			for m in self.tabNavMsg[n] :
				bool = False
				for c in self.grille.tabCases :
					if((m.longitude >= c.ouest) and (m.longitude < c.est) and (m.latitude <= c.nord) and (m.latitude > c.sud)) :
						if (oldId == -1) :#pour le premier tour de boucle, on met l'id de la case
							oldId = c.id
						if (c.id,n) not in self.tabNavCase :
							self.tabNavCase[(c.id,n)] = NavCase(c.id, n)
						if (c.id != oldId) and (oldMsg != None) :#si changement de case, on met le nouveau message dans l'ancienne case et l'ancien message dans la nouvelle
							self.tabNavCase[(c.id,n)].tabMsg.append(oldMsg)
							self.tabNavCase[(oldId,n)].tabMsg.append(m)
							msg = m
							msg.intercalaire = True
							self.tabNavCase[(oldId,n)].tabMsg.append(msg)
							oldId = c.id
						self.tabNavCase[(c.id,n)].tabMsg.append(m)
						bool = True
						break
				if bool == False :#compteur messages hors-zone
					cpt+=1
				oldMsg=m
			#print(str(cpt))
			if (oldId != -1):
				msg = m
				msg.intercalaire = True
				self.tabNavCase[(oldId,n)].tabMsg.append(msg)


	def applyAlgo(self) :
	
		for i in self.tabNavCase :
			if len(self.tabNavCase[i].tabMsg) > 4 :
				rep = self.tabNavCase[i].calculRecep()
				print(rep)
				self.grille.tabCases[self.tabNavCase[i].id].msgTheo = self.grille.tabCases[self.tabNavCase[i].id].msgTheo + rep['nbMsgTheos']
				self.grille.tabCases[self.tabNavCase[i].id].msgRecu = self.grille.tabCases[self.tabNavCase[i].id].msgRecu	+ rep['nbMsgRecus']
				self.grille.tabCases[self.tabNavCase[i].id].nbSequence = self.grille.tabCases[self.tabNavCase[i].id].nbSequence	+ rep['nbSequence']




