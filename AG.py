from xmlrpc.client import boolean

from numpy import append
from Chromosome import Chromosome
import random
from TraitementDeDonnees import TraitementDeDonnees


class AG:

    def __init__(self, nbIteration, taillePop, alpha, beta, pc, pm,  tailleMaxChromosome, minsup, minconf, 
    michigan ,typeCroisement, typeRemplacement, TypeExec) -> None:
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

        for i in range(self.taillePop):
            nouveau=False
            while(not nouveau):
                #print("hhh")
                nouveau=False
                t=random.randrange(2, self.tailleMaxChromosome+1)
                c=Chromosome(t,0,0,0,0,alpha,beta,False)
                ind=random.randrange(1, t)
                if(michigan):
                    c.setIndice(t-1)
                else:
                    c.setIndice(ind)
                c.chromosomeAlea()
                calcul = TraitementDeDonnees.calculFitnessCPU(c,self.alpha,self.beta)
                c.setCout(calcul.getFitness())
                c.setConfiance(calcul.getConfiance())
                c.setSupport(calcul.getSupport())

                if i==0:
                    self.population.append(c)
                    break
                else:
                    for x in self.population:
                        if x.equals(c)!=True:
                            self.population.append(c)
                            nouveau=True
                            break
                            

    def calculCoutPop(self):
        for i in range(self.taillePop):
            if(self.TypeExec==0) : self.population[i].calculerCoutRegle()
            #elif(self.TypeExec==2) : self.population[i].calculerCoutRegleGPUDist()
            #elif(self.TypeExec==4) : self.population[i].calculerCoutReglesurThreads()

    def lancerAlgoGen(self):
        if(self.TypeExec==0):
            print("etape 0 ")
            self.calculCoutPop()
            self.afficherPop() # population initiale
            for i in range(self.nbIteration):
                #croisement()
                #mutation()
                print("itération n° :",i)
        print("********************")
        self.afficherPop() #population finale
        self.AfficherReglesValide()
        self.stats()



    def croisement(self):
        #selection
        self.trierPop()

        

    def afficherPop(self):
        for i in range(self.taillePop):
            print("**************** régle ",i,"****************")
            self.population[i].afficherRegle()

    def AfficherReglesValide(self):
        print("----------Les Regles valides----------")
        for j in range(self.taillePop):
            if( self.population[j].getSupport() > self.minsup and self.population[j].getConfiance() > self.minconf):
                self.population[j].setValide(True)
                self.population[j].afficherRegle(self.population[j].getTaille())
            else : self.population[j].setValide(False)

    def stats(self):
        countRegles=0
        countItems=0
        nb2=0
        moyenne=0
        moyConf=0
        moySupp=0
        moyTaille=0
        items= []
        for j in range(self.taillePop):
            if(self.population[j].valide):
                countRegles += 1
                moyTaille += self.population[j].getTaille()
                if(self.population[j].getTaille()==2) : nb2 += 1
                moyenne += self.population[j].getCout()
                moyConf+=self.population[j].getConfiance()
                moySupp+= self.population[j].getSupport()
                for k in range(self.population[j].getTaille()):
                    if self.population[j].getItems()[k] not in items:
                        items.append(self.population[j].getItems()[k])
                        countItems += 1
                        
        moyTaille/= countRegles
        moyenne = moyenne/countRegles
        moySupp= moySupp/countRegles
        moyConf/=countRegles
        print("Le nombre de régles est : " ,countRegles)
        print("Le cout moyen est : " ,moyenne)
        print("Le support moyen est : " ,moySupp)
        print("La confiance moyenne est : " ,moyConf)
        print("Le nombre d'items utilisés : " ,countItems)
        print(" la taille moyenne est de : ",moyTaille,"  le nombre de regles de taille 2: ",nb2)



#petit probleme de constructeur dans Chromosome a régler aprés on peut mettre les valeur de init == o
    def trierPop(self):
        for i in range(1,self.taillePop):
            for j in range(self.taillePop-i):
                if( self.population[j].getCout()>self.population[j+1].getCout()):
                    save = Chromosome(self.population[j].getTaille(),self.population[j].getCout(),self.population[j].getSupport(),self.population[j].getConfiance(),self.population[j].getIndice(),self.population[j].getAlpha(),self.population[j].getBeta(),self.population[j].getValide())
                    self.population[j]=Chromosome(self.population[j+1].getTaille(),self.population[j+1].getCout(),self.population[j+1].getSupport(),self.population[j+1].getConfiance(),self.population[j+1].getIndice(),self.population[j+1].getAlpha(),self.population[j+1].getBeta(),self.population[j+1].getValide())
                    self.population[j+1]=save
		

    def mutation(self):
        for j in range(self.taillePop):
            d=random.uniform(0, 1)
            if(d<self.pm):
                while True:
                    mut = Chromosome(self.population[j].getTaille(),self.population[j].getCout(),self.population[j].getSupport(),self.population[j].getConfiance(),self.population[j].getIndice(),self.population[j].getAlpha(),self.population[j].getBeta(),self.population[j].getValide())
                    mut.items = self.population[j].getItems()
                    indice = random.randint(0,mut.getTaille()-1)
                    while True:
                        val = str(random.randint(1, TraitementDeDonnees.nbItems + 1))
                        if(mut.contient(val) is False):
                            break
                    mut.getItems()[indice] = val
                    if(mut not in self.population):
                        break
                self.population[j]=mut
                c=TraitementDeDonnees.calculFitnessCPU(self.population[j],self.alpha,self.beta)
                self.population[j].setCout(c.getFitness())
                self.population[j].setSupport(c.getSupport())
                self.population[j].setConfiance(c.getConfiance())



    def contientRegle(self,c):
        for i in range(self.taillePop):
            if(self.population[i].equals(c)): return True
        return False



TraitementDeDonnees.lireDonnees()
ag=AG(3,5,0.4,0.4,0.9,0.5,5,0.3,0.6,True,1,1,0)
ag.afficherPop()
ag.mutation()
print("----------------------------------------")
ag.afficherPop()





    