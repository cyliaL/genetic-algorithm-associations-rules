from xmlrpc.client import boolean

from numpy import append
import Chromosome
import random


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

        for i in range(self.taillePop):
            nouveau=True
            while(nouveau):
                nouveau=True
                t=random.randrange(2, self.tailleMaxChromosome+1)
                c=Chromosome(t,0,0,0,0,alpha,beta,None)
                ind=random.randrange(1, t)
                if(michigan):
                    c.setIndice(t-1)
                else:
                    c.setIndice(ind)
                
                c.chromosomeAlea()

                if i==0:
                    self.population.append(c)
                else:
                    for x in self.population:
                        if x.equals(c)==True:
                            nouveau=False
                            break
                        else:
                            self.population.append(c)




    