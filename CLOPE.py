# %%
import pandas as pd
import numpy as np
from sklearn.metrics import normalized_mutual_info_score
from collections import Counter
from collections import defaultdict

# df -> transactional dataset
# k -> number of clusters
# r -> repulsion coefficient
# real_label -> nome of the column in df that contains the class target (necessary to obtain the purity measure)
def CLOPE(df, k, r, real_label="missing!"):
    
    #whatever is passed the column of the class
    if real_label!="missing!":
        df_tmp = df.drop([real_label], axis=1, inplace=False)
    else: df_tmp = df
    
    #initialize the table (index in df | cluster label)
    table = pd.DataFrame(columns=['items', 'index', 'cluster_label', 'real_label'], index=range(df_tmp.shape[0]))
    table['index'] = np.arange(df_tmp.shape[0])
    table['cluster_label'] = -1
    table['items'] = df_tmp.apply(lambda row: row.tolist(), axis=1)
    if real_label!="missing!": table['real_label'] = df[real_label]
    
    #initialize the empty clusters
    # S -> number of items
    # W -> width
    # N -> number of transactions
    # Items -> list of items (eventually repeated)
    Clusters = pd.DataFrame(columns=['S', 'W', 'N', 'Items'], index=range(k))
    for index, c in Clusters.iterrows():
        c['S'] = 0
        c['W'] = 0
        c['N'] = 0
        c['Items'] = []
        
    
    #FIRST STEP
    for index, ts in table.iterrows():
        new_label = maximize(Clusters, ts, r)
        table.loc[index, 'cluster_label'] = new_label
        
        
    #SECOND STEP
    moved=False 
    while(not moved):
        moved=False
        for index, ts in table.iterrows():
            old_label = ts['cluster_label']
            new_label = maximize(Clusters, ts, r)
            if new_label!=old_label:
                table.loc[index, 'cluster_label'] = new_label
                moved = True
                
    #calculating metric for clustering evaluation
    if real_label != "missing!":
        real=table['real_label'].tolist()
        pred=table['cluster_label'].tolist()
        print("purity: ", Purity(real, pred))
        print("mutual info score: ", normalized_mutual_info_score(real, pred))   
    
    return table, Clusters

# %%
def maximize(Clusters, ts, r):
    
    label = ts['cluster_label']
    new_label = label #at starting point the new_label is the previous label
    indices_empty = Clusters.loc[Clusters['N'] == 0].index #list of empty cluster
    
    #CASE 0: There's at least one cluster with 0 elements
    if len(indices_empty)!=0:
        update_cluster(Clusters.loc[indices_empty[0]], ts)
        new_label = indices_empty[0]

#CASE 1: all the clusters have at least 1 element
    #remove ts from its Cluster (if ts belong to a cluster)
    else:
        #to avoid to remove the element from a cluster with a single element
        if label!=-1:
            if Clusters.loc[label]['N']==1:
                return label
        
        #REMOVE
        #if the element belong to a cluster...
        if label!=-1:
            #...remove the transaction from the cluster
            Clusters.loc[label]['S']-=len(ts['items'])
            Clusters.loc[label]['N']-=1
            Clusters.loc[label]['Items'] = remove_occ(Clusters.loc[label]['Items'], ts['items'])
            Clusters.loc[label]['W'] = len(set(Clusters.loc[label]['Items']))

        #UPDATE
        #update the cluster with the new transaction
        profits = Clusters.apply(lambda row: DeltaAdd(row, ts, r), axis=1).tolist()
        maxprofit = max(profits)
        new_label = profits.index(maxprofit)
        #update the corresponding cluster and ts.label
        update_cluster(Clusters.loc[new_label], ts)
        
    return new_label

# %%
#calculate the increment Profit considering a specific cluster C
def DeltaAdd(C, ts, r):

    S_new = C['S'] + len(ts['items'])
    W_new = C['W']

    for i in set(ts['items']):
        if not i in C['Items']:
            W_new+=1
            
    result = ( S_new*( (C['N']+1)/(W_new**r) ) ) - ( C['S']*( C['N']/(C['W']**r) ) )
    
    return result

# %%
def remove_occ(main_list, remove_list):
    
    main_counter = Counter(main_list)
    remove_counter = Counter(remove_list)

    result_counter = main_counter - remove_counter
        
    return list(result_counter.elements())

# %%
def update_cluster(C, ts):
    C['N']+=1
    C['S']+=len(ts['items'])
    C['Items']+=ts['items']
    C['W']=len(set(C['Items']))

# %%
def Purity(real, pred):
    
    mapping = {value: index for index, value in enumerate(set(real))}
    # Map the list of strings to numbers
    real_map = [mapping[item] for item in real]
    
    
    purity_val = 0
    cluster_count = defaultdict(lambda: [0] * len(set(real_map)))

    for p, r in zip(pred, real_map):
        cluster_count[p][r] += 1

    for label in cluster_count:
        purity_val += np.max(cluster_count[label])

    return 1.0 * purity_val / len(real)


