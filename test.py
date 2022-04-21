import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestRegressor
from TraitementDeDonnees import TraitementDeDonnees
from sklearn.model_selection import train_test_split
from sklearn import metrics
from sklearn.metrics import mean_squared_error
 
dataset = pd.read_csv('results/results_AG_simple.csv')
print(dataset)
TraitementDeDonnees.lireDonneesBinaires("data\DataSet5.txt")
co = TraitementDeDonnees.totalItems
one_hot_encoded_data = pd.get_dummies(dataset, columns = co)
#print(one_hot_encoded_data)
limit_sup = TraitementDeDonnees.nbItems * 3 +1
x= one_hot_encoded_data.iloc[:,1:limit_sup].values #les colones de 1 limit_sup
y= one_hot_encoded_data.iloc[:,0].values # la colonne fitnesse 0


X_train,X_test,Y_train,Y_test=train_test_split(x,y,test_size=0.25,random_state=0)


regressor = RandomForestRegressor(n_estimators = 30, random_state = 0)
regressor.fit(X_train,Y_train)
#print("yel7aaaaa c bn")


Y_pred = regressor.predict(X_test)
print(Y_pred[1])

errors = mean_squared_error(Y_test, Y_pred)
#print(Y_test)
print("======================")
#print(Y_pred.head())
print(errors.head())