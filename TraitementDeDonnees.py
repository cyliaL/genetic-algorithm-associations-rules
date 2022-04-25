from doctest import debug
from tkinter.tix import PopupMenu
from Cout import cout
import time
from datetime import datetime
from ExempleBDD import ExempleBDD
import pandas as pd
import csv
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import svm
from sklearn.tree import DecisionTreeRegressor 
from sklearn.neural_network import MLPRegressor
from sklearn.compose import make_column_transformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import make_pipeline
import numpy as np



class TraitementDeDonnees:
    time=0
    temps_encod=0
    temps_prediction=0
    nbTransactions=0
    nbItems=0
    totalItems=[]
    bdd=[]


    @staticmethod
    def lireDonnees1(path):
        '''with open(path, 'r') as file:
            data = file.read().splitlines()
            TraitementDeDonnees.nb_transactions, TraitementDeDonnees.total_items, TraitementDeDonnees.nb_items, transactions= int(data[0]), int(data[1]),int(data[2]), data[3:]
            #print(TraitementDeDonnees.nb_transactions)
            #print(TraitementDeDonnees.total_items)
            #print(TraitementDeDonnees.nb_items)
            #print(transactions)
        inter=list(transactions)
        for i in range(0, len(inter)):
            transaction=inter[i].split(',')
            #print(transaction) 
            TraitementDeDonnees.bdd.append(transaction)'''
        with open(path, "r") as file:
            for line in file:
                transaction = []
                TraitementDeDonnees.nbTransactions += 1
                for word in line.split():
                    transaction.append(word)
                    if word not in TraitementDeDonnees.totalItems:
                        TraitementDeDonnees.totalItems.append(word)
                TraitementDeDonnees.bdd.append(transaction)
            TraitementDeDonnees.nbItems=len(TraitementDeDonnees.totalItems)  
        print("okkkkk")  



    @staticmethod
    def lireDonnees2(path):
        '''with open(path, 'r') as file:
            data = file.read().splitlines()
            TraitementDeDonnees.nb_transactions, TraitementDeDonnees.total_items, TraitementDeDonnees.nb_items, transactions= int(data[0]), int(data[1]),int(data[2]), data[3:]
            #print(TraitementDeDonnees.nb_transactions)
            #print(TraitementDeDonnees.total_items)
            #print(TraitementDeDonnees.nb_items)
            #print(transactions)
        inter=list(transactions)
        for i in range(0, len(inter)):
            transaction=inter[i].split(',')
            #print(transaction) 
            TraitementDeDonnees.bdd.append(transaction)'''
        with open(path, "r") as file:
            for line in file:
                transaction = []
                TraitementDeDonnees.nbTransactions += 1
                for word in line.split():
                    transaction.append(word)
                    if word not in TraitementDeDonnees.totalItems:
                        TraitementDeDonnees.totalItems.append(word)
                TraitementDeDonnees.bdd.append(transaction)
            TraitementDeDonnees.nbItems=len(TraitementDeDonnees.totalItems)  
        print("okkkkk")  


    @staticmethod
    def lireDonneesSynthetiques(path):
        with open(path, 'r') as file:
            data = file.read().splitlines()
            TraitementDeDonnees.nbTransactions=int(data[0])
            index=2
            while True:
                item=str(data[index])
                if item=="BEGIN_DATA":
                    index+=1
                    break
                else:
                    TraitementDeDonnees.totalItems.append(item)
                    temp=item
                    index+=1
            tokens=temp.split()
            TraitementDeDonnees.nbItems=int(tokens[0])
            while(True):
                transaction=str(data[index])
                if(transaction=="END_DATA"):
                    break
                temp=transaction.split()
                TraitementDeDonnees.bdd.append(temp)
                index+=1
	            


    @staticmethod
    def lireDonnees():
        TraitementDeDonnees.bdd = ExempleBDD().getBDD()
        TraitementDeDonnees.nbTransactions = len(TraitementDeDonnees.bdd)
        TraitementDeDonnees.nbItems = 9
        TraitementDeDonnees.totalItems=["1","2","3","4","5","6","7","8","9"]


    @staticmethod
    def calculFitnessCPU(regle, alpha, beta) :
        AetB = 0 #nombre d'appaition de A et B
        A = 0    #nombbre d'appaition de d'un item antécédent 
        B=0      #nombre d'appaition de d'un item conclusion
        cpt=0
        startTime = time.time() #le temps en ms
        for i in range(TraitementDeDonnees.nbTransactions): #parcourir les transactions
            k = 0
            trouve = 0
            for j in range(regle.getIndice()): #parcourir les antécédents
                k=0
                while(k < len(TraitementDeDonnees.bdd[i]) ): #calculer le nombre d'items de la regle trouvés dans la transaction
                    if TraitementDeDonnees.bdd[i][k] == regle.getItems()[j]:
                        trouve += 1
                        break
                    k += 1
            if (trouve == regle.getIndice()) : A += 1 #tout les items antécédents sont trouvés
            cpt=0
            for j in range(regle.getIndice(),regle.getTaille()):
                k = 0
                while (k < len(TraitementDeDonnees.bdd[i])) :#rechercher la partie conséquence de la régle dans la transaction
                    if (TraitementDeDonnees.bdd[i][k]==regle.getItems()[j]) :
                        trouve += 1
                        cpt += 1 
                        break
                    k += 1
            if(trouve == regle.getTaille()) : AetB += 1 #tout les items antécédents et conclusion sont trouvés
            if(cpt== (regle.getTaille()-regle.getIndice())): B += 1 #nombre d'apparition de la conclusion
            #print(A,B,AetB)

        if(A==0 or AetB==0) : return cout(0,0,0)
        support = AetB / TraitementDeDonnees.nbTransactions
        confiance = AetB / A
        #if (B==0):lift=0
        #else :
        # lift= (AetB * self.nbTransactions)/ (A* B)
        # if(lift <1): lift=1
        stopTime = time.time()
        elapsedTime = (stopTime - startTime)
        TraitementDeDonnees.incTime(elapsedTime)
        return cout((alpha*support+beta*confiance)/(alpha+beta),support,confiance)

    #temps de calcul de la la fitness durant l'optimisation
    @staticmethod
    def incTime(ti):
        TraitementDeDonnees.time += ti


    @staticmethod
    def saveDonnees(totalData):
        l=TraitementDeDonnees.totalItems+['fitness']
        with open("./results/results_AG_simple.csv", 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(l)
            for r in totalData:
                debut_encod = time.time()
                r.encoder()
                r.binary.append(r.cout)
                fin_encod = time.time()
                TraitementDeDonnees.temps_encod += (fin_encod - debut_encod) 
                writer.writerow(r.binary) 
            l1,l2,l3=TraitementDeDonnees.generate_hasard()
            l1.append(0)
            l2.append(0)
            l3.append(0)
            writer.writerows([l1,l2,l3])
            

    @staticmethod
    def generate_hasard():
        l1=[]
        l2=[]
        l3=[]
        for i in range(TraitementDeDonnees.nbItems):
            l1.append('n')
            l2.append('a')
            l3.append('c')
        return [l1,l2,l3]


    @staticmethod
    def generateModelHorsLigne(numModel):        
        dataset = pd.read_csv('results/results_AG_simple.csv')
        co = TraitementDeDonnees.totalItems
        #print(dataset)
        one_hot_encoded_data = pd.get_dummies(dataset, columns = co)
        one_hot_encoded_data = one_hot_encoded_data.iloc[:-1 , :]
        one_hot_encoded_data = one_hot_encoded_data.iloc[:-1 , :]
        one_hot_encoded_data = one_hot_encoded_data.iloc[:-1 , :]
        #print(one_hot_encoded_data)
        limit_sup = TraitementDeDonnees.nbItems * 3 +1
        x= one_hot_encoded_data.iloc[:,1:limit_sup].values #les colones de 1 limit_sup
        y= one_hot_encoded_data.iloc[:,0].values # la colonne fitnesse 0
        x_train, x_test, y_train, y_test =train_test_split(x, y,test_size=0.25, random_state=0)
        '''--------------------------------------------------------------------------------'''
        if(numModel==0):
            print("Random Forest Regressor")
            temps_debut = time.time()
            TraitementDeDonnees.model = RandomForestRegressor(n_estimators = 30, random_state = 0)
            TraitementDeDonnees.model.fit(x_train,y_train)
            temps_fin = time.time()
            y_pred_RF = TraitementDeDonnees.model.predict(x_test)
            print('temps d''entrainement = ',temps_fin-temps_debut)
            print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_RF))
        if(numModel==1):
            print("Support Vector Regressor")
            temps_debut = time.time()
            TraitementDeDonnees.model = svm.SVR()
            TraitementDeDonnees.model.fit(x_train,y_train)
            temps_fin = time.time()
            y_pred_SVM=TraitementDeDonnees.model.predict(x_test)
            print('temps d''entrainement = ',temps_fin-temps_debut)
            print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_SVM))
        if(numModel==2):
            print("Decison Tree Regressor")
            temps_debut = time.time()
            TraitementDeDonnees.model = DecisionTreeRegressor(random_state = 0)
            TraitementDeDonnees.model.fit(x_train,y_train)
            temps_fin = time.time()
            y_pred_DT=TraitementDeDonnees.model.predict(x_test)
            print('temps d''entrainement = ',temps_fin-temps_debut)
            print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_DT))
        if(numModel==3):
            print("Neural Network Regressor")
            temps_debut = time.time()
            TraitementDeDonnees.model = MLPRegressor(max_iter=2000).fit(x_train,y_train)
            TraitementDeDonnees.model.fit(x_train,y_train)
            temps_fin = time.time()
            y_pred_NN=TraitementDeDonnees.model.predict(x_test)
            print('temps d''entrainement = ',temps_fin-temps_debut)
            print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_NN))




    @staticmethod
    def calculFitnessModelHorsLigne(regle):
        debut_encodage = time.time()
        l1,l2,l3=TraitementDeDonnees.generate_hasard()
        population=[l1,l2,l3]
        population.append(regle)
        #print(regle)
        co=TraitementDeDonnees.totalItems
        df= pd.DataFrame(population,columns = co)
        one_hot_encoded_data = pd.get_dummies(df, columns = co)
        fin_encodage = time.time()
        TraitementDeDonnees.temps_encod+= (fin_encodage-debut_encodage)
        #print(df)
        debut_prediction = time.time()
        val=TraitementDeDonnees.model.predict(one_hot_encoded_data)
        fin_prediction = time.time()
        TraitementDeDonnees.temps_prediction += (fin_prediction - debut_prediction)
        #print(val)
        return val[3:]

        


#TraitementDeDonnees.lireDonneesBinaires("data\DataSet1.txt")
#print(TraitementDeDonnees.bdd)

#print(TraitementDeDonnees.totalItems)