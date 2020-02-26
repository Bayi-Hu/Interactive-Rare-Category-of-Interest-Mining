# -*- coding:utf-8 -*-
import numpy as np
import time
from Code.Configuration import Args
from sklearn.neighbors import KDTree
import pickle
import os

args = Args('Abalone')
Dist = np.zeros([100, 2])
RSC = set()

AbsIdx2Idx = {}
Idx2AbsIdx = {}

def mapping():
    '''
    Generate index mapping function between data abstraction and raw features
    '''
    count = 0
    global Idx2AbsIdx, AbsIdx2Idx
    for i in RSC:
        Idx2AbsIdx[i] = count
        AbsIdx2Idx[count] = i
        count += 1

def Abstraction_Construct(X, Dist):
    '''
    Construct offline data abstraction for the follow-up rare category mining.
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
    Abs_idx_lst = np.array(list(RSC))
    Dist = Dist[Abs_idx_lst]
    Abs_scr = []
    Abs_idx = []

    start = time.time()
    for k in range(args.KMIN, args.KMAX + 1):
        D_k = Dist[:, k] / (np.average(Dist[:, :k], axis=1) + 0.01)
        Abs_scr.append(np.sort(D_k))
        Abs_idx.append(np.argsort(D_k))

    end = time.time()
    print('''Calculating candidates' score costs''', end - start, 's')
    Abs_scr = np.array(Abs_scr)
    Abs_idx = np.array(Abs_idx)
    time_1 = time.time()
    print('Establishment of OSpace and PSpace costs', time_1 - time_start, 's')

    return Abs_scr, Abs_idx, Abs_idx_lst

def main():
    X = np.load(os.path.join(args.dir,'X.npy'))
    y = np.load(os.path.join(args.dir,'y.npy'))

    kdtree = KDTree(X, leaf_size=40, metric='euclidean')
    Dist, NNindex = kdtree.query(X, args.KMAX + 1)
    np.save(os.path.join(args.dir, 'Dist.npy'), Dist)
    np.save(os.path.join(args.dir, 'NNindex.npy'), NNindex)

    (Abs_scr, Abs_idx, Abs_idx_lst) = Abstraction_Construct(X, Dist)

    with open(os.path.join(args.abs_dir, 'Abs_scr'),'wb') as f:
        pickle.dump(Abs_scr, f)
    with open(os.path.join(args.abs_dir, 'Abs_idx'),'wb') as f:
        pickle.dump(Abs_idx, f)
    with open(os.path.join(args.abs_dir, 'Abs_idx_lst'),'wb') as f:
        pickle.dump(Abs_idx_lst, f)
    with open(os.path.join(args.abs_dir, 'Idx2AbsIdx'),'wb') as f:
        pickle.dump(Idx2AbsIdx, f)
    with open(os.path.join(args.abs_dir, 'AbsIdx2Idx'),'wb') as f:
        pickle.dump(AbsIdx2Idx, f)

    print('Offline abstraction construction has finished..')

if __name__ == '__main__':
    main()


