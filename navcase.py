from math import ceil

class NavCase :

	def __init__(self,id,mmsi) :#constructeur
		self.mmsi = mmsi
		self.id = id
		self.tabMsg = list()
		
	def calculTI(self) :#calcule si le navire possède un indicateur développé d'angle de barre ou non (Turn Indicator)
		i = 0
		asTi=True
		while(i < len(self.tabMsg)) :
			if(self.tabMsg[i].tauxVirage == 127 or self.tabMsg[i].tauxVirage == -127) :
				asTi=False
				break
			i+=1
		return asTi
			
	def calculRecep(self) :#calcul le pourcentage de messages reçus
		rep=dict()
		rep['nbMsgRecus'] = 0
		rep['nbMsgTheos'] = 0
		rep['pourcentage'] = 0
		rep['nbSequence'] = 0
		
		if(len(self.tabMsg) < 3) :
			rep['nbMsgRecus'] = 0
			rep['nbMsgTheos'] = 0
			rep['pourcentage'] = 0
			rep['nbSequence'] = 0
		else :
			
			ind = 1
			
			if ((self.tabMsg[ind].typeMsg == 1 or self.tabMsg[ind].typeMsg == 2 or self.tabMsg[ind].typeMsg == 3) and (self.tabMsg[ind].tauxVirage != -128)) : #class A
				while (ind < len(self.tabMsg)) :
					cpt = 0
					vitesse = self.tabMsg[ind].vitesse
					cap = self.tabMsg[ind].cap
					navStatus = self.tabMsg[ind].statut
					heure1 = self.tabMsg[ind-1].horaire
					upperBorder = 1022
					lowerBorder = 0
					#print('debut'+str(ind))
					if (navStatus == 1 or navStatus == 5) :#détermine l'intervalle de vitesse suivant la vitesse du premier message de la séquence
						if (vitesse < 30) :
							upperBorder = 30
							lowerBorder = 0
						else :
							upperBorder = 1022
							lowerBorder = 30
					else :
						if(vitesse <= 140) :
							upperBorder = 140
							lowerBorder = 0
						elif (vitesse > 140 and vitesse <= 230) :
							upperBorder = 230
							lowerBorder = 140
						else :
							upperBorder = 1022
							lowerBorder = 230
					#cpt+=1
					
					asTi = self.calculTI()
					#print(asTi)
					tauxInit = self.tabMsg[ind].tauxVirage
					tourne = True
					if((asTi == False and tauxInit == 0) or (asTi == True and tauxInit < 15 and tauxInit > -15)):
						tourne = False
					#print(tourne)
					aChange = False
										
					
					while(((aChange == False) and (self.tabMsg[ind].statut == navStatus) and (self.tabMsg[ind].vitesse < upperBorder) and (self.tabMsg[ind].vitesse >= lowerBorder)) and self.tabMsg[ind].intercalaire == False) : #tant que la vitesse reste la même, on est sur la même séquence
						if(asTi == False) :
							if (tourne == True and self.tabMsg[ind-1].tauxVirage == 0) :
								aChange = True
							elif (tourne == False and self.tabMsg[ind-1].tauxVirage != 0) :
								aChange = True
							else : 
								aChange = False
						else :
							if (tourne == True and self.tabMsg[ind-1].tauxVirage < 15 and self.tabMsg[ind-1].tauxVirage > -15) :
								aChange = True
							elif (tourne == False and self.tabMsg[ind-1].tauxVirage >= 15 and self.tabMsg[ind-1].tauxVirage <= -15) :
								aChange = True
							else : 
								aChange = False
						
						ind+=1
						cpt+=1
						
					#print(ind)
					#print(cpt)
					#print(tourne)
					#print(aChange)
					#print('ind'+str(ind))
					#print('cpt'+str(cpt))					
					heure2 = self.tabMsg[ind-1].horaire
					if (self.tabMsg[ind].intercalaire == True) : #si le message est un intercalaire, on le passe
						heure2 = self.tabMsg[ind-2].horaire
						ind += 2
						cpt -= 1
					
					
					intervalle = 0
					if (navStatus == 1 or navStatus == 5) :
						if (vitesse <= 30)  :
							intervalle = 180
						else :
							intervalle = 10
					else :
						if(vitesse <= 140 and tourne == False) :
							intervalle = 10
						elif(vitesse <= 140 and tourne == True) :
							intervalle = 3.33
						elif (vitesse > 140 and vitesse <= 230 and tourne == False) :
							intervalle = 6
						elif (vitesse > 140 and vitesse <= 230 and tourne == True) :
							intervalle = 2
						else :
							intervalle = 2
		
					
					rep['nbMsgRecus'] = rep['nbMsgRecus'] + cpt
					rep['nbMsgTheos'] = rep['nbMsgTheos'] + ceil(((heure2 - heure1)/intervalle))
					rep['nbSequence'] += 1
						
			elif (self.tabMsg[ind].typeMsg == 18) : #class B
				while (ind < len(self.tabMsg)) :
					cpt = 0
					vitesse = self.tabMsg[ind].vitesse
					heure1 = self.tabMsg[ind-1].horaire
					upperBorder = 1022
					lowerBorder = 0
					#print('debut'+str(ind))
					if(vitesse <= 20) :#détermine l'intervalle de vitesse suivant la vitesse du premier message de la séquence
						upperBorder = 20
						lowerBorder = 0
					elif (vitesse > 20 and vitesse <= 140) :
						upperBorder = 140
						lowerBorder = 20
					elif (vitesse > 140 and vitesse <= 230) :
						upperBorder = 230
						lowerBorder = 140
					else :
						upperBorder = 1022
						lowerBorder = 230
					#cpt+=1
					while(((self.tabMsg[ind].vitesse < upperBorder) and  (self.tabMsg[ind].vitesse >= lowerBorder)) and self.tabMsg[ind].intercalaire == False) : #tant que la vitesse reste la même, on est sur la même séquence
						ind+=1
						cpt+=1
						
					#print('ind'+str(ind))
					#print('cpt'+str(cpt))					
					heure2 = self.tabMsg[ind-1].horaire
					if (self.tabMsg[ind].intercalaire == True) : #si le message est un intercalaire, on le passe
						heure2 = self.tabMsg[ind-2].horaire
						ind += 2
						cpt -= 1
						
					
					intervalle = 0
					if(vitesse <= 20) :
						intervalle = 180
					elif (vitesse > 20 and vitesse <= 140) :
						intervalle = 30
					elif (vitesse > 140 and vitesse <= 230) :
						intervalle = 15
					else :
						intervalle = 5
		
					
					rep['nbMsgRecus'] = rep['nbMsgRecus'] + cpt
					rep['nbMsgTheos'] = rep['nbMsgTheos'] + ((heure2 - heure1)/intervalle)
					rep['nbSequence'] += 1
	
		return rep