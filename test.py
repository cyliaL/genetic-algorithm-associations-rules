from Cout import cout
from TraitementDeDonnees import TraitementDeDonnees
from AG import AG
import pandas as pd
import numpy as np
from AG_Hors_Ligne import AG_Hors_Ligne


TraitementDeDonnees.lireDonneesSynthetiques('data\data.txt')
print(TraitementDeDonnees.totalItems)
print(TraitementDeDonnees.nbItems)
print(TraitementDeDonnees.nbTransactions)
print(TraitementDeDonnees.bdd)
'''TraitementDeDonnees.lireDonneesBinaires("data\data_test.txt")
ag=AG(30,30,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
ag.lancerAlgoGen()
print("le temps de calcul de la fitness réelle durant l'optimisation = ", TraitementDeDonnees.time)
print("==========================================================================================")
TraitementDeDonnees.generateModelHorsLigne(0)
agHorsLigne=AG_Hors_Ligne(30,30,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
agHorsLigne.lancerAlgoGen()
print("le temps de prédiction = ", TraitementDeDonnees.temps_prediction)
print("le temps d'encodage = ", TraitementDeDonnees.temps_encod)
print("==========================================================================================")
TraitementDeDonnees.generateModelHorsLigne(1)
agHorsLigne=AG_Hors_Ligne(30,30,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
agHorsLigne.lancerAlgoGen()
print("le temps de prédiction = ", TraitementDeDonnees.temps_prediction)
print("le temps d'encodage = ", TraitementDeDonnees.temps_encod)
print("==========================================================================================")
TraitementDeDonnees.generateModelHorsLigne(2)
agHorsLigne=AG_Hors_Ligne(30,30,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
agHorsLigne.lancerAlgoGen()
print("le temps de prédiction = ", TraitementDeDonnees.temps_prediction)
print("le temps d'encodage = ", TraitementDeDonnees.temps_encod)
print("==========================================================================================")
TraitementDeDonnees.generateModelHorsLigne(3)
agHorsLigne=AG_Hors_Ligne(30,30,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
agHorsLigne.lancerAlgoGen()
print("le temps de prédiction = ", TraitementDeDonnees.temps_prediction)
print("le temps d'encodage = ", TraitementDeDonnees.temps_encod)'''