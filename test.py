import math
import csv
from xmlrpc.client import boolean
from cv2 import sort
import time
from numpy import append
from regex import P
from Chromosome import Chromosome
import random
from Cout import cout
from TraitementDeDonnees import TraitementDeDonnees
from AG import AG
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import svm
from sklearn.tree import DecisionTreeRegressor 
from sklearn.neural_network import MLPRegressor


TraitementDeDonnees.lireDonneesBinaires("data\DataSet1.txt")
ag=AG(100,100,0.4,0.6,0.5,0.5,5,0.3,0.6,True,0,0,0)
ag.lancerAlgoGen()
ag.saveDonnees()
print("le temps d'encodage des chromosomes = ",ag.temps_encod)
print("le temps d'execution de l'AG séquentiel = ",ag.temps_exec)
print("--------------------------------------------------------------------------------")

'''--------------------------------------------------------------------------------'''
# pré-traitement

dataset = pd.read_csv('results/results_AG_simple.csv')
co = TraitementDeDonnees.totalItems
one_hot_encoded_data = pd.get_dummies(dataset, columns = co)
limit_sup = TraitementDeDonnees.nbItems * 3 +1
x= one_hot_encoded_data.iloc[:,1:limit_sup].values #les colones de 1 limit_sup
y= one_hot_encoded_data.iloc[:,0].values # la colonne fitnesse 0
x_train, x_test, y_train, y_test =train_test_split(x, y,test_size=0.25, random_state=0)
'''--------------------------------------------------------------------------------'''
print("Random Forest Regressor")
temps_debut = time.time()
regressor_RF = RandomForestRegressor(n_estimators = 30, random_state = 0)
regressor_RF.fit(x_train,y_train)
temps_fin = time.time()
y_pred_RF = regressor_RF.predict(x_test)
print('temps d''entrainement = ',temps_fin-temps_debut)
print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_RF))
print("--------------------------------------------------------------------------------")
print("Support Vector Regressor")
temps_debut = time.time()
regressor_SVM = svm.SVR()
regressor_SVM.fit(x_train,y_train)
temps_fin = time.time()
y_pred_SVM=regressor_SVM.predict(x_test)
print('temps d''entrainement = ',temps_fin-temps_debut)
print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_SVM))
print("--------------------------------------------------------------------------------")
print("Decison Tree Regressor")
temps_debut = time.time()
regressor_DT = DecisionTreeRegressor(random_state = 0)
regressor_DT.fit(x_train,y_train)
temps_fin = time.time()
y_pred_DT=regressor_DT.predict(x_test)
print('temps d''entrainement = ',temps_fin-temps_debut)
print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_DT))

print("--------------------------------------------------------------------------------")
print("Neural Network Regressor")
temps_debut = time.time()
regressor_NN = MLPRegressor(max_iter=2000).fit(x_train,y_train)
regressor_NN.fit(x_train,y_train)
temps_fin = time.time()
y_pred_NN=regressor_NN.predict(x_test)
print('temps d''entrainement = ',temps_fin-temps_debut)
print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_NN))