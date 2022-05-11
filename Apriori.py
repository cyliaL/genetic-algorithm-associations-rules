import numpy as np
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori


from TraitementDeDonnees import TraitementDeDonnees

TraitementDeDonnees.lireDonneesTransactions("data\data_test.txt")

te = TransactionEncoder()
te_ary = te.fit(TraitementDeDonnees.bdd).transform(TraitementDeDonnees.bdd)
te_ary.astype(int)
print(te.columns_)

df=pd.DataFrame(te_ary, columns=te.columns_)
df1 = apriori(df,min_support=0.4,use_colnames=True,verbose =1)
print(df1)

output= association_rules(df1, metric = "confidence", min_threshold = 0.5)

print(output)



