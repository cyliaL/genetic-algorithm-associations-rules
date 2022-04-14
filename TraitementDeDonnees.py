from Cout import cout
import time
from ExempleBDD import ExempleBDD

class TraitementDeDonnees:
    time=0
    nbTransactions=0
    nbItems=0
    totalItems=0
    bdd=[]

    @staticmethod
    def lireDonneesBinaires(path):
        with open(path, 'r') as file:
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
            TraitementDeDonnees.bdd.append(transaction)

    @staticmethod
    def lireDonnees():
        TraitementDeDonnees.bdd = ExempleBDD().getBDD()
        TraitementDeDonnees.nbTransactions = len(TraitementDeDonnees.bdd)
        TraitementDeDonnees.nbItems = 9

    @staticmethod
    def calculFitnessCPU(regle, alpha, beta) :
        AetB = 0 #nombre d'appaition de A et B
        A = 0    #nombbre d'appaition de d'un item antécédent 
        B=0      #nombre d'appaition de d'un item conclusion
        cpt=0
        startTime = int(round(time.time() * 1000)) #le temps en ms
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
        stopTime = int(round(time.time() * 1000))
        elapsedTime = (stopTime - startTime)
        TraitementDeDonnees.incTime(elapsedTime)
        return cout((alpha*support+beta*confiance)/(alpha+beta),support,confiance)

    @staticmethod
    def incTime(ti):
        TraitementDeDonnees.time += ti