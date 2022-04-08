import Cout
import time
from ExempleBDD import ExempleBDD

#bdd.append(["1","2"])

#bdd.append(["D"])

class TraitementDeDonnees:
   def __init__(self):
      self.time=0
      self.nbTransactions=0
      self.nbItems=0
      self.totalItems=0
      self.bdd=[]

   def lireDonnees(self):
      self.bdd = ExempleBDD().getBDD()
      self.nbTransactions = len(self.bdd)
      self.nbItems = 5

   @staticmethod
   def calculFitnessCPU(self,regle, a, b) :
      AetB = 0 #nombre d'appaition de A et B
      A = 0    #nombbre d'appaition de d'un item antécédent 
      B=0      #nombre d'appaition de d'un item conclusion
      startTime = int(round(time.time() * 1000)) #le temps en ms
      for i in range(self.nbTransactions): #parcourir les transactions
         k = 0
         trouve = 0
         for j in range(regle.getIndice()): #parcourir les antécédents
            k=0
            while(k < len(self.bdd[i]) ): #calculer le nombre d'items de la regle trouvés dans la transaction
               if self.bdd[i][k] == regle.getItems()[j]:
                  trouve += 1
                  break
               k += 1
         if (trouve == regle.getIndice()) : #tout les items de la partie antécédent sont trouvés
            A += 1
         cpt=0
         j=regle.getIndice()
         for j in range(regle.getTaille()):
            k = 0
            while (k < len(self.bdd[i])) :#rechercher la partie conséquence de la régle dans la transaction
               if (self.bdd[i][k]==regle.getItems()[j]) :
                  trouve += 1
                  cpt += 1
                  break
            k += 1
         if(trouve == regle.getTaille()) : AetB += 1
         if(cpt== (regle.getTaille()-regle.getIndice())): B += 1
      if(A==0 or AetB==0) : return Cout(0,0,0)
      support = AetB / self.nbTransactions
   # print("support : ",support)
      confiance = AetB / A
      #if (B==0):lift=0
      #else :
      # lift= (AetB * self.nbTransactions)/ (A* B)
      # if(lift <1): lift=1
      # print("--> Lift : " ,lift)
      # #print("confiance : " ,confiance);
      stopTime = int(round(time.time() * 1000))
      elapsedTime = (stopTime - startTime)
      self.time = elapsedTime
      return Cout(support,confiance, (a*support+b*confiance)/(a+b))


