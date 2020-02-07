# -*- coding:utf-8 -*-
import numpy as np
import time
from Configuration import Args
from numpy.linalg import cholesky
from sklearn.neighbors import KDTree
import bisect
import pickle
import os

args = Args('Shuttle')
Dist = np.zeros([100, 2])
RSC = set()
index2RSCindex = {}
RSCindex2index = {}

def mapping():
    count = 0
    global index2RSCindex, RSCindex2index
    for i in RSC:
        index2RSCindex[i] = count
        RSCindex2index[count] = i
        count += 1

def Abstraction_Construct(X, Dist):
    '''
    :param args:
    :param X:
    :param kdtree:
    :return:
    '''
    time_start = time.time()
    reserve = int(args.rp * X.shape[0])
    # take sample a for example, rare-category-score of sample a is d(k+1)/d(avg_k)
    # d(k+1) is distance from sample a to its k+1-th nearest neighbor;
    # d(avg_k) is average distance from sample a to its top-k nearest neighbors.

    start = time.time()
    for k in range(args.KMIN, args.KMAX + 1):
        temp = np.argsort(-Dist[:, k] / (np.average(Dist[:, :k], axis=1) + 0.01), axis=0)
        for i in temp[:reserve]:
            RSC.add(i)

    end = time.time()
    print('Picking candidates costs', end-start, 's')
    print('The number of candidates is', len(RSC))

    mapping()
    RSC_index_array = np.array(list(RSC))
    Dist = Dist[RSC_index_array]

    PSpace_score = []
    PSpace_index = []

    start = time.time()

    for k in range(args.KMIN, args.KMAX + 1):
        D_k = Dist[:, k] / (np.average(Dist[:, :k], axis=1) + 0.01)

        PSpace_score.append(np.sort(D_k))
        PSpace_index.append(np.argsort(D_k))

    end = time.time()
    print('''Calculating candidates' score costs''', end - start, 's')

    PSpace_score = np.array(PSpace_score)
    PSpace_index = np.array(PSpace_index)

    time_1 = time.time()
    print('Establishment of OSpace and PSpace costs', time_1 - time_start, 's')

    return PSpace_score, PSpace_index, RSC_index_array

def main():
    X = np.load(os.path.join(args.dir,'X.npy'))
    y = np.load(os.path.join(args.dir,'y.npy'))

    kdtree = KDTree(X, leaf_size=40, metric='euclidean')
    Dist, NNindex = kdtree.query(X, args.KMAX + 1)
    np.save(os.path.join(args.dir, 'Dist.npy'), Dist)
    np.save(os.path.join(args.dir, 'NNindex.npy'), NNindex)

    (PSpace_score, PSpace_index, RSC_index_array) = Abstraction_Construct(X, Dist)

    with open(os.path.join(args.abs_dir, 'PSpace_score'),'wb') as f:
        pickle.dump(PSpace_score, f)
    with open(os.path.join(args.abs_dir, 'PSpace_index'),'wb') as f:
        pickle.dump(PSpace_index, f)
    with open(os.path.join(args.abs_dir, 'RSC_index_array'),'wb') as f:
        pickle.dump(RSC_index_array, f)
    with open(os.path.join(args.abs_dir, 'index2RSCindex'),'wb') as f:
        pickle.dump(index2RSCindex, f)
    with open(os.path.join(args.abs_dir, 'RSCindex2index'),'wb') as f:
        pickle.dump(RSCindex2index, f)

    print('pause')

if __name__ == '__main__':
    main()


