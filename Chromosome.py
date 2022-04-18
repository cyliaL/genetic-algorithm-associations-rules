from itertools import count
from operator import truediv
from tokenize import String
from ExempleBDD import ExempleBDD
from TraitementDeDonnees import TraitementDeDonnees
#from cv2 import repeat
import random
from Cout import cout


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
        self.binary =[]

    def setItems(self, items):
        self.items=items

    def getTaille(self):
        return self.taille
    
    def getBinary(self):
        return self.binary

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
    
    def setItem(self, item,indice):
        self.items[indice]=item

    def copyChromosome(self,c):
        self.taille=c.taille
        self.cout=c.cout
        self.support=c.support
        self.confiance=c.confiance
        self.indice=c.indice
        self.alpha=c.alpha
        self.beta=c.beta
        self.valide=c.valide

        for i in range(c.taille):
            self.items.append(c.getItems()[i])


    def calculerCoutRegleCPU(self):
        c= TraitementDeDonnees.calculFitnessCPU(self, self.alpha, self.beta)
        self.confiance=c.confiance
        self.support=c.support
        self.cout=c.fitness

    def afficherRegle(self):
        print(" Items :  ",self.items,"/ indice",self.indice)
        print("fitness = ",self.cout, " support =",self.support," confiance =",self.confiance)


    def chromosomeAlea(self): #err
        for i in range(self.taille):
            while True:
                nouveau=True
                #print(TraitementDeDonnees.nbItems)
                x=random.randrange(0, TraitementDeDonnees.nbItems,1)
                self.items.append(TraitementDeDonnees.totalItems[x])
                
                j=0
                while j<i:
                    if(self.items[j]==self.items[i]):
                        nouveau=False
                        self.items.pop()
                        break
                    j+=1
                if(nouveau==True):
                    break

    def contient(self, item):#err
        for i in range(self.taille):
            if self.items[i]==item:
                return True
        return False


    def contientAntecedants(self, item):
        for i in range(self.indice):
            if self.items[i]==item:
                return True
        return False

        
    def contientConclusion(self, item):
        for i in range(self.indice, self.taille):
            if self.items[i]==item:
                return True
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
        for i in range(self.indice):
            if not self.contientAntecedants(c.getItems()[i]):
                return False

        for i in range(self.indice,self.taille):
            if not self.contientConclusion(c.getItems()[i]):
                return False

        return True
    
    def encoder(self):
        for it in TraitementDeDonnees.totalItems:
            i=0
            while(i<self.taille):
                if i >= self.indice:
                    if self.items[i]==it:
                        self.binary.append(2)
                        break
                elif self.items[i]==it:
                        self.binary.append(1)
                        break  
                i += 1
            if i==self.taille:
                self.binary.append(0)
        self.binary.append(self.indice)
        self.binary.append(self.cout)


#test
#tab=[]
#TraitementDeDonnees.lireDonneesBinaires("data\DataSet1.txt")
TraitementDeDonnees.lireDonnees()
print("total items = ",TraitementDeDonnees.totalItems)
print("--------------------------------------")
regle1 = Chromosome(4,0,0,0,2,0.1,0.1,False)
regle1.chromosomeAlea() 
f=TraitementDeDonnees.calculFitnessCPU(regle1,0.1,0.1)
regle1.setCout(f.fitness)
regle1.setSupport(f.support)
regle1.setConfiance(f.confiance)
print("--------------------------------------")
regle1.afficherRegle()
print("--------------------------------------")
regle1.encoder()
print("binaire [item1,item2...,indice,fitness ] = ",regle1.binary)