from grille import Grille

param = dict()	#paramètres de la grille
param['long'] = -4.83
param['lat'] = 48.42
param['rows'] = 2
param['lines'] = 2
param['pasH'] = 0.04
param['pasV'] = -0.04

g = Grille(param)

g.printGrid('testGridOut.log')
