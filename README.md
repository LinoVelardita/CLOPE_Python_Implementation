# CLOPE_Python_Implementation
Python Implementation of CLOPE (Clustering with SLOPE), a transactional clustering algorithm proposed in 2002.

Traditional clustering algorithms are inefficient and often unsuitable for datasets with categorical features due to their large size and volume. Algorithms relying on pairwise distance calculations, like k-means, are primarily effective for numerical data but perform poorly when dealing with numerous non-numeric factors. The main limitation is not the complexity of defining a distance metric for categorical attributes, but rather the requirement of pairwise comparisons between objects in each iteration. This approach becomes impractical for tables with millions of records and thousands of fields.
CLOPE was proposed in 2002 by a group of Chinese scientists. It provides higher performance and better clustering quality compared to other hierarchical algorithms proposed fro working with categorical data.

Briefly, the CLOPE clustering algorithm is based on the idea of maximization of the global cost function, which increases the proximity of transactions inside the clusters due to an increase in the cluster histogram parameter.

Below is the pseudocode I relied on for the implementation...

first pass through the transaction table to perform the initial split

![phase 1](https://github.com/LinoVelardita/CLOPE_Python_Implementation/assets/102514924/8fdf30d1-851c-4f1c-83cf-02e2612628ea)

After that, there are additional table scans required to improve the clustering quality and optimize the cost function. If there are no changes in the current pass through the table, the algorithm stop

![phase 2](https://github.com/LinoVelardita/CLOPE_Python_Implementation/assets/102514924/979afb03-da58-4923-921f-904bad491d7c)

Instead of the classic Profit function, it was used the DeltaAdd function, that returns the difference (in terms of Profit) of the clusters with and without the transaction t. This is possible thanks to the following theorem: If DeltaAdd(Ci,t) is the maximum, then movement t to the cluster maximizes Profit(C,r).

![deltaAdd](https://github.com/LinoVelardita/CLOPE_Python_Implementation/assets/102514924/086db9a5-30df-4c2a-afab-2d8d6da52d53)





ref. Yang, Y., Guan, H., You. J. CLOPE: A fast and Effective Clustering Algorithm for Transactional Data In Proc. of SIGKDD’02, July 23-26, 2002, Edmonton, Alberta, Canada.
