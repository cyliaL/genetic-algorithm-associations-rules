from Cout import cout
from TraitementDeDonnees import TraitementDeDonnees
from AG import AG
import pandas as pd
import numpy as np
from AG_Hors_Ligne import AG_Hors_Ligne


TraitementDeDonnees.lireDonneesSynthetiques('data\DataSet5.txt')
print("hello")
ag=AG(100,30,0.4,0.6,0.5,0.5,4,0.3,0.6,True,0,0,0)
ag.lancerAlgoGen()
TraitementDeDonnees.generateModelHorsLigneBinaire(0)
val=TraitementDeDonnees.model.predict([[0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
print(val)
#print(TraitementDeDonnees.totalItems)
#print(TraitementDeDonnees.nbItems)
#print(TraitementDeDonnees.nbTransactions)
#print(TraitementDeDonnees.bdd)
#TraitementDeDonnees.lireDonneesBinaires("data\data_test.txt")
'''ag=AG(100,30,0.4,0.6,0.5,0.5,3,0.3,0.6,True,0,0,0)
ag.lancerAlgoGen()
print("le temps de calcul de la fitness réelle durant l'optimisation = ", TraitementDeDonnees.temps_calc_fitness)
print("le temps de l'encodage = ", TraitementDeDonnees.temps_encod)
print("==========================================================================================")
TraitementDeDonnees.temps_calc_fitness=0
TraitementDeDonnees.temps_encod=0
TraitementDeDonnees.temps_prediction=0
TraitementDeDonnees.generateModelHorsLigneBinaire(0)
#x=pd.DataFrame()
agHorsLigne=AG_Hors_Ligne(100,30,0.4,0.6,0.5,0.5,3,0.3,0.6,True,0,0,0)
agHorsLigne.lancerAlgoGen()
print("le temps de prédiction = ", TraitementDeDonnees.temps_prediction)
print("le temps d'encodage = ", TraitementDeDonnees.temps_encod)



print("==========================================================================================")
TraitementDeDonnees.temps_calc_fitness=0
TraitementDeDonnees.temps_encod=0
TraitementDeDonnees.temps_prediction=0
TraitementDeDonnees.generateModelHorsLigneBinaire(1)
agHorsLigne=AG_Hors_Ligne(30,30,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
agHorsLigne.lancerAlgoGen()
print("le temps de prédiction = ", TraitementDeDonnees.temps_prediction)
print("le temps d'encodage = ", TraitementDeDonnees.temps_encod)
print("==========================================================================================")
TraitementDeDonnees.temps_calc_fitness=0
TraitementDeDonnees.temps_encod=0
TraitementDeDonnees.temps_prediction=0
TraitementDeDonnees.generateModelHorsLigneBinaire(2)
agHorsLigne=AG_Hors_Ligne(30,30,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
agHorsLigne.lancerAlgoGen()
print("le temps de prédiction = ", TraitementDeDonnees.temps_prediction)
print("le temps d'encodage = ", TraitementDeDonnees.temps_encod)
print("==========================================================================================")
TraitementDeDonnees.temps_calc_fitness=0
TraitementDeDonnees.temps_encod=0
TraitementDeDonnees.temps_prediction=0
TraitementDeDonnees.generateModelHorsLigneBinaire(3)
agHorsLigne=AG_Hors_Ligne(30,30,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
agHorsLigne.lancerAlgoGen()
print("le temps de prédiction = ", TraitementDeDonnees.temps_prediction)
print("le temps d'encodage = ", TraitementDeDonnees.temps_encod)'''