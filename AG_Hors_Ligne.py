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
import pandas as pd

class hii:
    def __init__(self, nbIteration, taillePop, alpha, beta, pc, pm,  tailleMaxChromosome, minsup, minconf, 
    michigan ,typeCroisement, typeRemplacement, TypeExec):
        self.nbIterations=nbIteration
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
        self.population=[]
        self.TypeExec = TypeExec
        self.temps_exec = 0

        for i in range(self.taillePop):
            while(True):
                #print("hhh")
                nouveau=True
                t=random.randrange(2, self.tailleMaxChromosome+1)
                c=Chromosome(t,0,0,0,0,alpha,beta,False)
                ind=random.randrange(1, t)
                if(michigan):
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
                    self.population.append(c)
                    break
                
                            

    def calculCoutPop(self):
        if(self.TypeExec==0):
            for r in self.population:
                debut_encod = time.time()
                r.encoder()
                fin_encod = time.time()
                TraitementDeDonnees.temps_encod+=(fin_encod-debut_encod)
            fitness=TraitementDeDonnees.calculFitnessModelHorsLigne(self.population)
                #r.setCout(fitness)
            for i,r in enumerate(self.population):
                r.setCout(fitness[i])


                

                #calcul=TraitementDeDonnees.calculFitnessCPU(r,self.alpha,self.beta)
                #r.setCout(calcul.getFitness())
                #r.setConfiance(calcul.getConfiance())
                #r.setSupport(calcul.getSupport())

        #elif(self.TypeExec==2) : self.population[i].calculerCoutRegleGPUDist()
        #elif(self.TypeExec==4) : self.population[i].calculerCoutReglesurThreads()

    def lancerAlgoGen(self):
        debut_exec = time.time()
       
        if(self.TypeExec==0):
            #self.afficherPop() # population initiale
            for i in range(self.nbIterations):
                self.croisement()
                self.mutation()
        fin_exec = time.time()
        self.temps_exec += (fin_exec - debut_exec)
        print("le temps d'execution de l'AG avec modèle hors-ligne = ", self.temps_exec)
        #self.AfficherReglesValide()
        #self.stats()



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
                        debut_encod = time.time()
                        ef1.encoder()
                        ef2.encoder()
                        fin_encod = time.time()
                        TraitementDeDonnees.temps_encod+=fin_encod-debut_encod            
                        c1=TraitementDeDonnees.calculFitnessModelHorsLigne(ef1.binary)
                        ef1.setCout(c1)
                        c2=TraitementDeDonnees.calculFitnessModelHorsLigne(ef2.binary)
                        ef1.setCout(c2)

                    
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
            print("le temps d'encodage = ",TraitementDeDonnees.temps_encod, "secondes")
            



    #petit probleme de constructeur dans Chromosome a régler aprés on peut mettre les valeur de init == o
    def trierPop(self):
        for i in range(1,self.taillePop):
            for j in range(self.taillePop-i):
                if( self.population[j].getCout()>self.population[j+1].getCout()):
                    save = self.population[j]
                    self.population[j]=self.population[j+1]
                    self.population[j+1]=save
		

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
                debut_encod = time.time()
                mut.encoder()
                fin_encod = time.time()
                TraitementDeDonnees.temps_encod+=fin_encod-debut_encod 
                c=TraitementDeDonnees.calculFitnessModelHorsLigne(mut.binary)
                mut.setCout(c)
                self.population[j]=mut

                



