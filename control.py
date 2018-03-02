from mesure import Mesure
from aisio import AISIO
import time

class Control :
	
	def __init__(self, balise) :
		self.aisio = AISIO(balise)
		self.mesure = Mesure()


#main
param = dict()	#paramètres de la grille
param['long'] = -4.60
param['lat'] = 48.44
param['rows'] = 22
param['lines'] = 16
param['pasH'] = 0.02
param['pasV'] = -0.01

c = Control("BSPLOUZ")

#t=time.time()

#c.aisio.createFromFile('ais.log',c.mesure)
#c.aisio.createFromFile('../test_20180112.nmea',c.mesure)

#print(int(time.time()-t))

#c.aisio.saveAll("all.log",c.mesure)
#c.aisio.saveNav("nav.log",c.mesure, 227008170)

c.aisio.loadAll('nav.log',c.mesure)
#c.aisio.saveAll("all.log",c.mesure)

c.mesure.createGrid(param)
#c.mesure.grille.printGrid('grid.log')

c.mesure.sortByCase()

c.mesure.applyAlgo()

c.mesure.grille.printGrid('grid.log')

c.mesure.grille.fillMatrice()

c.mesure.grille.writeMatrice('mat.csv')


#for i in c.mesure.tabNavCase :
        #-print(str(c.mesure.tabNavCase[i].mmsi)+' '+str(c.mesure.tabNavCase[i].id)+' '+str(len(c.mesure.tabNavCase[i].tabMsg)))

#for i in c.mesure.tabNavCase[(269,636018035)].tabMsg :
#        print(str(i))

#print(str(c.mesure.grille.tabCases[313]))

