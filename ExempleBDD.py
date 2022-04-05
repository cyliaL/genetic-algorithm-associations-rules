import numpy as np
class ExempleBDD :
    def __init__(self): 
        self.bdd = [[1,4],[2,4], [1, 3, 5], [2,4,5,6], [1,2,4,5,6], [1,4,6], [2,4,6], [1,3,4,5,6], [2,3,5,6], [1,3,4,6]]

    def getBDD(self):
        return self.bdd
    
    def setBDD(self, bdd):
        self.bdd= bdd

test = ExempleBDD()
print(len(test.getBDD()))
