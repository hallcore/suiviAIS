from mesure import Mesure
from bitstring import BitArray
from aismessage import AISMessage

class AISIO :
	"""
		Cette classe utilitaire permet de mettre en mémoire un fichier AIS encodé, d'enregistrer les messages décodés dans des fichiers et de les recharger
	"""
	
	def __init__(self, balise) :	#constructeur
		self.balise = balise

	def createFromFile(self, fileNameIn, mes) :	#Cette méthode décode et met en mémoire un fichier AIS encodé
		with open(fileNameIn,"r") as fi :
			for line in fi :
				if line[3:10] == self.balise :
				
					part1 = line[:27]	#première partie du message
					beacon = part1.split(",")[0][3:10]	#nom de la balise réceptrice
					timeRecv = part1.split(",")[1][2:-4]	#heure de réception
					
					if(mes.balise == "inconnu") :
						mes.balise = beacon
					
					part2 = line[27:]	#deuxième partie du message : données
					part2 = part2[:-1]
					trame = part2.split(",")
					
					#décodage de la trame
					dataDec = []
					for c in trame[5] :	#convertit les caractères ascii
						dataDec.append(ord(c))
					dataBin = []
					for d in dataDec :	#convertit l'ascii 8-bit en ascii 6-bit et les transforme en binaire
						tmp = d - 48
						if tmp > 40 :
							tmp = tmp - 8
						dataBin.append(bin(tmp))
					dataBin6= []
					for b in dataBin :	#ajoute des zéros si nécessaire pour avoir des chaînes de 6 bits
						dataBin6.append(b[2:].zfill(6))
					msgBin = ""
					for p in dataBin6 :	#crée la chaîne globale en collant toutes les parties
						msgBin += p
					
					#on ne garde que les types de messages désirés
					if int(msgBin[0:6],2) == 1 or int(msgBin[0:6],2) == 2 or int(msgBin[0:6],2) == 3 :#if type 1, 2 or 3
						mes.ajoutMsg(AISMessage(int(timeRecv),int(msgBin[0:6],2),int(msgBin[8:38],2),BitArray(bin=msgBin[89:116]).int/600000,BitArray(bin=msgBin[61:89]).int/600000,int(msgBin[50:60],2),int(msgBin[128:137],2),int(msgBin[38:42],2),BitArray(bin=msgBin[42:50]).int))
					elif int(msgBin[0:6],2) == 18 :#if type 18
						mes.ajoutMsg(AISMessage(int(timeRecv),int(msgBin[0:6],2),int(msgBin[8:38],2),BitArray(bin=msgBin[85:112]).int/600000,BitArray(bin=msgBin[57:85]).int/600000,int(msgBin[46:56],2),int(msgBin[124:133],2),-1,-1))
			mes.triHoraireNavMsg() #on s'assure que les messages sont triés chronologiquement
			
	def saveAll(self, fileNameOut, mes) :	#sauvegarde tous les messages de tous les navires
		with open(fileNameOut,"w") as fo :
			for key in mes.tabNavMsg :
				fo.write("MMSI : "+str(key)+'\n')
				for m in mes.tabNavMsg[key] :
					fo.write(str(m))
					
	def saveNav(self, fileNameOut, mes, mmsi) :	#sauvegarde tous les messages du navire passé en paramètre
		with open(fileNameOut,"w") as fo :
			fo.write("MMSI : "+str(mmsi)+'\n')
			for m in mes.tabNavMsg[mmsi] :
				fo.write(str(m))
	
	def loadAll(self, fileNameIn, mes) :	#charge tous les messages de tous les navires
		with open(fileNameIn,"r") as fi :
			for line in fi :
				if(line[0:4] != "MMSI") :
					msg = line.split(",")
					mes.ajoutMsg(AISMessage(int(msg[2]),int(msg[1]),int(msg[0]),float(msg[3]),float(msg[4]),int(msg[5]),int(msg[6]),int(msg[7]),int(msg[8])))

	def loadNav(self, fileNameIn, mes, mmsi) :	#charge tous les messages du navire passé en paramètre
		with open(fileNameIn,"r") as fi :
			trouve = False
			while True :
				line = fo.readline()
				if not line :	#c'est la fin du fichier
					break
				if line == "MMSI : "+str(mmsi) :	 #le navire est trouvé
					trouve = True
					break
			
			if trouve == True :
				while True :
					line = fo.readline()
					if not line :	#c'est la fin du fichier
						break
					if line[0:4] == "MMSI" :	#le navire est fini
						break
					
					msg = line.split(",")
					mes.ajoutMsg(AISMessage(int(msg[2]),int(msg[1]),int(msg[0]),float(msg[3]),float(msg[4]),int(msg[5]),int(msg[6]),int(msg[7]),int(msg[8])))

