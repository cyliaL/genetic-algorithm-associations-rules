from itertools import count
from operator import truediv
from tokenize import String
from ExempleBDD import ExempleBDD
from TraitementDeDonnees import TraitementDeDonnees
#from cv2 import repeat
import random
import Cout


class Chromosome:
    def __init__(self, taille, cout, support, confiance, indice, alpha, beta, valide):
        self.taille=taille
        self.items = []
        self.cout=cout
        self.support=support
        self.confiance=confiance
        self.indice=indice
        self.alpha=alpha
        self.beta=beta
        self.valide=valide

    def getTaille(self):
        return self.taille

    def getCout(self):
        return self.cout

    def getSupport(self):
        return self.support

    def getConfiance(self):
        return self.confiance

    def getIndice(self):
        return self.indice

    def getAlpha(self):
        return self.alpha

    def getBeta(self):
        return self.beta   

    def getValide(self):
        return self.valide

    def getItems(self):
        return self.items

    def setTaille(self, taille):
        self.taille=taille
        
    def setCout(self, cout):
        self.cout=cout

    def setSupport(self, support):
        self.support=support

    def setConfiance(self, confiance):
        self.confiance=confiance

    def setIndice(self, indice):
        self.indice=indice

    def setAlpha(self, alpha):
        self.alpha=alpha

    def setBeta(self, beta):
        self.beta=beta

    def setValide(self, valide):
        self.valide=valide

    def copyChromosome(self,c):
        self.taille=c.taille
        self.cout=c.cout
        self.support=c.support
        self.confiance=c.confiance
        self.indice=c.indice
        self.alpha=c.alpha
        self.beta=c.beta
        self.valide=c.valide
        i=0
        while(True):
            self.items[i]=c.getItems()[i]
            if(i==self.taille):
                break
            i+=1


    def calculerCoutRegle(self):
        c= Cout(TraitementDeDonnees.calculFitnessCPU(self, self.alpha, self.beta))
        self.confiane=c.confiance
        self.support=c.support
        self.cout=c.cout

    def afficherRegle(self, k):
        if(self.cout != 0):
            print(" R�gle "+(int)(k+1)+" : ")
            for item in self.items:
                print("  " + item)
            print("cout: "+self.cout, " indice: "+self.indice)


    def cheromosomeAlea(self): #err
        for i in range(self.taille):
            while True:
                nouveau=True
                x=TraitementDeDonnees.nbItems +1
                self.items.append(str(random.randrange(1, x)))
                j=0
                while j<i:
                    if(self.items[j]==self.items[i]):
                        nouveau=False
                        self.items.pop()
                        break
                    j+=1
                if(nouveau==True):
                    break

    def contient(self, item):
        index=0
        while(True):
            if self.items[index]==item:
                return True
            if index==self.taille:
                break
        return False

    def contientAntecedants(self, item):
        index=0
        while(True):
            if self.items[index]==item:
                return True
            if index==self.indice:
                break
            index+=1
        return False

        
    def contientConclusion(self, item):
        index=self.indice
        while(True):
            if self.items[index]==item:
                return True
            if index==self.taille:
                break
            index+=1
        return False

    def redondante(self,c):
        if((self.taille-self.indice) != (c.getTaille()-c.getIndice())):
            return False
        index=self.indice
        while(True):
            if not c.contientConclusion(self.items[index]):
                return False
            if index==self.taille:
                break
            index+=1
        index=0
        while(True):
            if not self.contientAntecedents(c.getItems()[index]):
                return False
            if index==self.indice:
                break
            index+=1
        return True

    def equals(self,c):
        if(self.indice!= c.getIndice()):
            return False
        index=0
        while(True):
            if not self.contientAntecedents(c.getItems()[index]):
                return False
            if index==self.indice:
                break
            index+=1

        while(True):
            if not self.contientConclusion(c.getItems()[index]):
                return False
            if index==self.taille:
                break
            index+=1
        return True


#test
TraitementDeDonnees.lireDonnees()
regle = Chromosome(3,0,0,0,2,0.1,0.1,False)
regle.cheromosomeAlea() 
print("items : ",regle.getItems())
print("fitness : ",TraitementDeDonnees().calculFitnessCPU(regle,1,2).getFitness) #mazal
