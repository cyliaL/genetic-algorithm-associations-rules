import math
import csv
from xmlrpc.client import boolean
from cv2 import sort
import time
from numpy import append
from regex import P
from Chromosome import Chromosome
import random
import copy
from Cout import cout
from TraitementDeDonnees import TraitementDeDonnees

from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn import svm
from sklearn.tree import DecisionTreeRegressor 
from sklearn.neural_network import MLPRegressor
import matplotlib.pyplot as plt


class AG_En_Ligne:

    def __init__(self, maxIterations, taillePop, alpha, beta, pc, pm,  tailleMaxChromosome, minsup, minconf, 
    michigan ,typeCroisement, typeRemplacement, typeExec,typeModel,typeMAJ):
        self.maxIterations=maxIterations
        self.taillePop=taillePop
        self.alpha=alpha
        self.beta=beta
        self.pc=pc
        self.pm=pm
        self.tailleMaxChromosome=tailleMaxChromosome
        self.minsup=minsup
        self.minconf=minconf
        self.michigan=michigan
        self.typeCroisement=typeCroisement
        self.typeRemplacement=typeRemplacement
        self.TypeExec = typeExec
        self.typeModel=typeModel
        self.typeMAJ=typeMAJ
        self.nbIterations=0
        self.population = []


        self.pop_train = []
        self.pop_train_val = []

        self.temps_entrainement=0
        self.temps_eval_reelle=0
        self.temps_prediction=0
        self.temps_exec = 0
        self.temps_encod=0

        self.indice=0
        self.x=[]
        self.y=[]
        self.z=[]
        
        
        for i in range(self.taillePop):
            while(True):
                #print("hhh")
                nouveau=True
                t=random.randrange(2, self.tailleMaxChromosome+1)
                c=Chromosome(t,0,0,0,0,self.alpha,self.beta,False)
                ind=random.randrange(1, t)
                if(self.michigan):
                    c.setIndice(t-1)
                else:
                    c.setIndice(ind)

                c.chromosomeAlea()
                #calcul = TraitementDeDonnees.calculFitnessCPU(c,self.alpha,self.beta)
                #c.setCout(calcul.getFitness())
                #c.setConfiance(calcul.getConfiance())
                #c.setSupport(calcul.getSupport())

                for x in self.population:
                    if x.equals(c):
                        nouveau=False
                        break

                if(nouveau==True):
                    debut_encod=time.time()
                    c.encoderBinaire()
                    fin_encod=time.time()
                    self.temps_encod+=fin_encod-debut_encod
                    self.population.append(c)
                    self.pop_train.append(c.binary)
                    break

        
        self.eval_function_pop()
        for r in self.population:
            self.pop_train_val.append(r.getCout())

        self.ind_best=self.population[0]
        self.ind_candidate=self.population[0]



    def train_model(self):
        if(self.typeModel==0):
            print("Random Forest Regressor")
            temps_debut = time.time()
            self.model = RandomForestRegressor(n_estimators = 30, random_state = 0)
            self.model.fit(self.pop_train,self.pop_train_val)
            temps_fin = time.time()
            self.temps_entrainement+=temps_debut-temps_fin
            #print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_RF))
        
        if(self.typeModel==1):
            print("Support Vector Regressor")
            temps_debut = time.time()
            self.model = svm.SVR()
            self.model.fit(self.pop_train,self.pop_train_val)
            temps_fin = time.time()
            self.temps_entrainement+=temps_fin-temps_debut
            #print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_SVM))
        if(self.typeModel==2):
            print("Decison Tree Regressor")
            temps_debut = time.time()
            self.model = DecisionTreeRegressor(random_state = 0)
            self.model.fit(self.pop_train,self.pop_train_val)
            temps_fin = time.time()
            self.temps_entrainement+=temps_fin-temps_debut
            #print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_DT))
        if(self.typeModel==3):
            print("Neural Network Regressor")
            temps_debut = time.time()
            self.model = MLPRegressor(max_iter=2000)
            self.model.fit(self.pop_train,self.pop_train_val)
            temps_fin = time.time()
            self.temps_entrainement+=temps_fin-temps_debut


    
    def model_predict(self,regle):
        data=[regle.binary]
        debut_pred=time.time()
        val = self.model.predict(data)
        fin_pred=time.time()
        self.temps_prediction+=fin_pred-debut_pred
        regle.setCout(val)
    

    def update_model(self):
        if(self.typeMAJ==0):
            pop_sort=self.trierPop()
            #for x in pop_sort:
                #x.afficherRegle()
            for i in range(len(self.population)):
                print(i)
                self.ind_candidate = self.population[i]
                if self.ind_candidate not in (self.pop_train):
                    #self.ind_candidate.encoderBinaire()
                    #self.ind_candidate.afficherRegle()
                    #print(self.pop_train)
                    #print(self.pop_train_val)
                    self.x.append(self.indice)
                    self.indice+=1
                    self.y.append(self.ind_candidate.getCout())
                    #self.eval_function(self.ind_candidate)
                    debut_eval=time.time()
                    calcul=TraitementDeDonnees.calculFitnessCPU(self.ind_candidate,self.alpha,self.beta)
                    fin_eval=time.time()
                    self.temps_eval_reelle+=fin_eval-debut_eval
                    self.ind_candidate.setCout(calcul.getFitness())
                    self.ind_candidate.setConfiance(calcul.getConfiance())
                    self.ind_candidate.setSupport(calcul.getSupport())
                    self.z.append(calcul.getFitness())

                    self.pop_train.append(self.ind_candidate.binary)
                    self.pop_train_val.append(self.ind_candidate.getCout())
                    print(self.pop_train)
                    print(self.pop_train_val)
                    debut_entrain=time.time()
                    self.model.fit(self.pop_train, self.pop_train_val)
                    fin_entrain=time.time()
                    self.temps_entrainement+=fin_entrain-debut_entrain
                    #debut_entrain=time.time()
                    #x_train, x_test, y_train, y_test =train_test_split(self.pop_train, self.pop_train_val,test_size=0.25, random_state=8)
                    #self.model.fit(x_train,y_train)
                    #fin_entrain=time.time()
                    #self.temps_entrainement+=fin_entrain-debut_entrain
                    #y_pred_RF = self.model.predict(x_test)
                    #print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_RF))

                    break
        else:
            if self.maxIterations%10==0:
                #print(len(self.pop_train))
                for r in self.population:
                    self.eval_function(r)
                    self.pop_train.append(r.binary)
                    self.pop_train_val.append(r.getCout())
                debut_entrain=time.time()
                #self.model.fit(self.pop_train,self.pop_train_val)
                x_train, x_test, y_train, y_test =train_test_split(self.pop_train, self.pop_train_val,test_size=0.25, random_state=8)
                self.model.fit(x_train,y_train)
                fin_entrain=time.time()
                self.temps_entrainement+=fin_entrain-debut_entrain
                y_pred_RF = self.model.predict(x_test)
                print('Erreur quadratique moyenne (Root Mean Squared Error):', mean_squared_error(y_test, y_pred_RF))

    def update_best(self):
        if self.ind_candidate.getCout() > self.ind_best.getCout():
            self.ind_best = self.ind_candidate

        
    def eval_function(self,c):
        if(self.TypeExec==0):
            #c.calculerCoutRegleCPU(self.alpha,self.beta)
            debut_eval=time.time()
            calcul=TraitementDeDonnees.calculFitnessCPU(c,self.alpha,self.beta)
            fin_eval=time.time()
            self.temps_eval_reelle+=fin_eval-debut_eval
            c.setCout(calcul.getFitness())
            c.setConfiance(calcul.getConfiance())
            c.setSupport(calcul.getSupport())


    def eval_function_pop(self):
        if(self.TypeExec==0): 
            for r in self.population:
                #r.calculerCoutRegleCPU(self.alpha,self.beta)
                debut_eval=time.time()
                calcul=TraitementDeDonnees.calculFitnessCPU(r,self.alpha,self.beta)
                fin_eval=time.time()
                self.temps_eval_reelle+=fin_eval-debut_eval
                r.setCout(calcul.getFitness())
                r.setConfiance(calcul.getConfiance())
                r.setSupport(calcul.getSupport())

        #elif(self.TypeExec==2) : self.population[i].calculerCoutRegleGPUDist()
        #elif(self.TypeExec==4) : self.population[i].calculerCoutReglesurThreads()

    def lancerAlgoGen(self):

        if(self.TypeExec==0):

            self.train_model()
            #self.calculCoutPop()   
            #self.afficherPop() # population initiale
            #print(self.nbIterations)
            for i in range(self.maxIterations):
                self.croisement()
                self.mutation()
                self.update_model()
                self.update_best()
        self.trierPop()

        # plotting the line 2 points
        #plt.scatter(self.x, self.y, label= 'AGsimple', color= "green", marker= "*", s=30)
        #plt.scatter(self.x, self.y, label= 'AG_EnLigne', color= "red", marker= "*", s=30)
        plt.plot(self.x, self.y, color='r', label='AGsimple')
        plt.plot(self.x, self.z, color='g', label='AG_EnLing')
        plt.xlabel('individu')
        plt.ylabel('fitness')
        plt.title('la fitness au cours des générations')
        plt.legend()
        plt.show()
        #fin_exec = time.time()
        #self.temps_exec += (fin_exec - debut_exec)
        #print("le temps d'execution de l'AG simple = ",self.temps_exec)
        print("le temps d'encodage binaire = ",self.temps_encod)
        print("le temps d'evaluation reelle = ",self.temps_eval_reelle)
        print("le temps d'entrainement = ",self.temps_entrainement)
        print("le temps de prediction = ",self.temps_prediction)





    def croisement(self): 
        #self.trierPop()
        #======> selection des paires
        paires=[]
        indice=0
        utilisees=set()
        for j in range(self.taillePop):
            while(True):
                rand=random.random()
                indice+=1
                if(indice==self.taillePop):
                    indice=0
                while (indice in utilisees):
                    indice+=1
                    if indice==self.taillePop:
                        indice=0
                if(rand<=0.5):
                    break
            paires.append(indice)
            utilisees.add(indice)
        if(len(paires)%2==1):
            fin=len(paires)-1
        else:
            fin=len(paires)
        #======> croisement
        for j in range(0, fin-1,2):
            if(random.random()<self.pc):
                ef1=Chromosome(self.population[paires[j]].getTaille(),0,0,0,self.population[paires[j]].getIndice(),self.alpha,self.beta,False)
                ef2=Chromosome(self.population[paires[j+1]].getTaille(),0,0,0,self.population[paires[j+1]].getIndice(),self.alpha,self.beta,False)
                minimum=min(ef1.getTaille(),ef2.getTaille())
                #======> croisement à un point
                if self.typeCroisement==0:
                    #======> recopier la premiere partie des parents vers les fils
                    point=random.randrange(1,minimum)
                    for k in range(point):
                        ef1.getItems().append(self.population[paires[j]].getItems()[k])
                        ef2.getItems().append(self.population[paires[j+1]].getItems()[k])
                     #======> echanger la deuxième partie das parents vers les fils
                    for k in range(point,minimum):
                        if (not self.population[paires[j]].contient(self.population[paires[j+1]].getItems()[k])) and (not self.population[paires[j+1]].contient(self.population[paires[j]].getItems()[k])):
                            ef1.getItems().append(self.population[paires[j+1]].getItems()[k])
                            ef2.getItems().append(self.population[paires[j]].getItems()[k])
                        else:
                            ef1.getItems() .append(self.population[paires[j]].getItems()[k])
                            ef2.getItems().append(self.population[paires[j+1]].getItems()[k])
                    #======> copier les items restants de la regle 1
                    for k in range(minimum,ef1.getTaille(),1):
                        ef1.getItems().append(self.population[paires[j]].getItems()[k])   
                    #======> copier les items restants de la regle 2
                    for k in range(minimum,ef2.getTaille(),1):
                        ef2.getItems().append(self.population[paires[j+1]].getItems()[k])   
                    #======> evaluation des individus fils
                    if self.TypeExec==0:
                        debut_encod=time.time()
                        ef1.encoderBinaire()
                        ef2.encoderBinaire()
                        fin_encod=time.time()
                        self.temps_encod+=fin_encod-debut_encod

                        self.model_predict(ef1)
                        self.model_predict(ef2)

                    
                    #======> remplacement des parents
                    remplace=0
                    #======> remplacement de la regle 1
                    if (not self.contientRegle(ef1)):
                        if ef1.getCout()> self.population[paires[j]].getCout():
                            self.population[paires[j]]= ef1
                            remplace=1
                        else: 
                            if ef1.getCout()> self.population[paires[j+1]].getCout():
                                self.population[paires[j+1]]= ef1
                                remplace=2
                    #======> remplacement de la regle 2 
                    if not self.contientRegle(ef2):
                        if remplace ==0  and ef2.cout> self.population[paires[j]].getCout():
                            self.population[paires[j]]= ef2
                        else: 
                            if remplace ==0  and ef2.cout> self.population[paires[j+1]].getCout():
                                self.population[paires[j+1]]= ef2
                            else: 
                                if remplace ==1  and ef2.cout> self.population[paires[j+1]].getCout():
                                    self.population[paires[j+1]]= ef2
                                else: 
                                    if remplace ==2  and ef2.cout> self.population[paires[j]].getCout():
                                        self.population[paires[j]]= ef2


    def contientRegle(self,c):
        for i in range(self.taillePop):
            if self.population[i].equals(c):
                return True
        return False
        

    def afficherPop(self):
        for x in self.population:
            x.afficherRegle()


    def AfficherReglesValide(self):
        print("----------Les Regles valides----------")
        for j in range(self.taillePop):
            if( self.population[j].getSupport() > self.minsup and self.population[j].getConfiance() > self.minconf):
                self.population[j].setValide(True)
                self.population[j].afficherRegle()
            else : self.population[j].setValide(False)

    def stats(self):
        countRegles=0
        countItems=0
        moyenne=0
        moyConf=0
        moySupp=0
        moyTaille=0
        items= []
        for c in self.population:
            if c.valide:
                countRegles += 1
                moyTaille += c.getTaille()
                moyenne += c.getCout()
                moyConf+=c.getConfiance()
                moySupp+= c.getSupport()
                for k in range(c.getTaille()):
                    if c.getItems()[k] not in items:
                        items.append(c.getItems()[k])
                        countItems += 1  
        if(countRegles!=0): 
            moyTaille/= countRegles
            moyenne/= countRegles
            moySupp/= countRegles
            moyConf/= countRegles
            print("Le nombre de régles est : " ,countRegles)
            print("Le cout moyen est : " ,moyenne)
            print("Le support moyen est : " ,moySupp)
            print("La confiance moyenne est : " ,moyConf)
            print("Le nombre d'items utilisés : " ,countItems)
            print(" la taille moyenne est de : ",moyTaille)
            print("le temps d'execution = ",self.temps_exec, "secondes")
            print("le temps d'encodage = ",self.temps_encod, "secondes")
            



    #petit probleme de constructeur dans Chromosome a régler aprés on peut mettre les valeur de init == o
    def trierPop(self):
        pop_sort = copy.deepcopy(self.population)
        for i in range(1,self.taillePop):
            for j in range(self.taillePop-i):
                if( pop_sort[j].getCout()>pop_sort[j+1].getCout()):
                    save = pop_sort[j]
                    pop_sort[j]=pop_sort[j+1]
                    pop_sort[j+1]=save
        return pop_sort
		

    def mutation(self):
        for j in range(self.taillePop):
            d=random.uniform(0, 1)
            if(d<self.pm):
                while True:
                    #print("gggg")
                    mut = Chromosome(self.population[j].getTaille(),self.population[j].getCout(),self.population[j].getSupport(),self.population[j].getConfiance(),self.population[j].getIndice(),self.population[j].getAlpha(),self.population[j].getBeta(),self.population[j].getValide())
                    for k in range(mut.getTaille()):
                        mut.getItems().append(self.population[j].getItems()[k])
                    #mut.items = self.population[j].getItems()
                    indice = random.randint(0,mut.getTaille()-1)
                    while True:
                        val = TraitementDeDonnees.totalItems[random.randrange(0, TraitementDeDonnees.nbItems,1)]
                        if(not mut.contient(val)):
                            break
                    mut.getItems()[indice] = val
                    if(not self.contientRegle(mut)):
                        break
                debut_encod=time.time()
                mut.encoderBinaire()
                fin_encod=time.time()
                self.temps_encod+=fin_encod-debut_encod

                self.model_predict(mut)
                self.population[j]=mut


TraitementDeDonnees.lireDonneesSynthetiques('data\mushroom.txt')
debut_exec=time.time()
ag=AG_En_Ligne(50,200,0.4,0.6,0.9,0.1,7,0.3,0.6,True,0,0,0,0,0)
ag.lancerAlgoGen()
fin_exec = time.time()
temps_exec = (fin_exec - debut_exec)
print("le temps d'execution de l'AG simple = ",temps_exec)