class cout: 
    def __init__(self, fitness, support, confiance): 
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


  
#test = cout() # constructeur vide

#test.setFitness(10) 
#test.setSupport(0.5)
#test.setConfiance(1)
#print(test.getFitness(),test.getSupport(),test.getConfiance()) # les getters marchents
#print(test.fitness,test.support,test.confiance) # les attributs marchent
###


t1 = cout(10,20,30) # constructeur avec valeurs

print(t1.fitness,t1.support,t1.confiance) #les valeurs marchent 
print(t1.getFitness,t1.getSupport,t1.getConfiance)#les getters marchent pas erreur





  
