from case import Case
import numpy as np

class Grille :
	"""
		Cette classe permet de simuler la grille geographique.
	"""
	
	def __init__(self, param) :#constructeur
		self.param = param
		
		self.tabCases = list()
		self.matrice = np.zeros((16,22),float)
		
		#crée le nombre de cases nécessaire en fonction des paramètres passés
		ind = 0
		for i in range(0,self.param['lines']) :
			for j in range(0,self.param['rows']) :
				self.tabCases.append(Case(ind,j,i,self.param['lat']+self.param['pasV']*i,self.param['long']+self.param['pasH']*j,self.param['lat']+self.param['pasV']*(i+1),self.param['long']+self.param['pasH']*(j+1)))
				ind += 1
	
	def paramSTR(self) :#permet d'écrire les paramètres sous la forme d'un string
		return str(self.param['long'])+","+str(self.param['lat'])+","+str(self.param['rows'])+","+str(self.param['lines'])+","+str(self.param['pasH'])+","+str(self.param['pasV'])
	
	def printGrid(self, fileName) :#génère un fichier avec toutes les cases de la grille
		with open(fileName,"w") as fo :
			fo.write(self.paramSTR()+'\n')
			for c in self.tabCases :
				fo.write(str(c))


	def fillMatrice(self) :#rempli la matrice résultat en fonction des valeurs enregistrées dans toutes les cases.
		x = 0
		y = -1
		for i in range(0,len(self.tabCases)):
			if i%self.param['rows'] == 0 :
				x = 0
				y += 1
			else :
				x += 1
			
			if (self.tabCases[i].msgTheo > 0.0):
				self.matrice[y,x] = self.tabCases[i].msgRecu / self.tabCases[i].msgTheo
			else :
				self.matrice[y,x] = 0.0
			
	def writeMatrice(self,fileNameOut):#exporte la matrice dans un fichier csv
		with open(fileNameOut,"w") as fo :
			x = 0
			y = -1
			strg=''
			for i in range(0,len(self.tabCases)):
				if i%self.param['rows'] == 0 :
					strg = strg +'\n'
					fo.write(strg)
					x = 0
					y += 1
					strg=''
				else :
					x += 1
					strg=strg+','
			
					strg = strg + str(self.matrice[y,x])
					