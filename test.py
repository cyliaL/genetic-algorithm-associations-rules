from Cout import cout
from TraitementDeDonnees import TraitementDeDonnees
from AGetMLHorsLigne import AGetMLHorsLigne
from AG import AG
import pandas as pd
import numpy as np

TraitementDeDonnees.lireDonneesBinaires("data\DataSet1.txt")
#ag=AG(100,100,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
#ag.lancerAlgoGen()
TraitementDeDonnees.generateModelHorsLigne(0)
agHorsLigne=AGetMLHorsLigne(100,100,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
agHorsLigne.lancerAlgoGen()
