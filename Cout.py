class cout: 
    def __init__(self, fitness = 0, support = 0, confiance = 0): 
         self.fitness = fitness
         self.support = support
         self.confiance = confiance
      
    
    def getFitness(self): 
        return self.fitness 
    
    def setFitness(self, f): 
        self.fitness = f

    def getSupport(self): 
        return self.support

    def setSupport(self, s): 
        self.support = s

    def getConfiance(self): 
        return self.confiance
    
    def setConfiance(self, c): 
        self.confiance = c


  
test = cout() # constructeur vide
test.setFitness(10) #il faut utiliser les setters pour introduire les valeurs, les getters marchent
test.setSupport(0.5)
test.setConfiance(1)
print(test.getFitness(),test.getSupport(),test.getConfiance()) 
print(test.fitness,test.support,test.confiance)



t2 = cout(10,20,30) # constructeur avec valeurs, les getters ne marchent pas il faut appeler directement l'attribut
print(t2.fitness,t2.support,t2.confiance)





  
