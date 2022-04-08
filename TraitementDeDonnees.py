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
            print(TraitementDeDonnees.nb_transactions)
            print(TraitementDeDonnees.total_items)
            print(TraitementDeDonnees.nb_items)
            print(transactions)
        inter=list(transactions)

        for i in range(0, len(inter)):
            transaction=inter[i].split(',')
            print(transaction) 
            TraitementDeDonnees.bdd.append(transaction)