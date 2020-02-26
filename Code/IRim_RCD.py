# -*- coding:utf-8 -*-
import numpy as np
import time
from Code.Configuration import Args
import os
import pickle

args = Args('Abalone')

# Load Abastraction
with open(os.path.join(args.abs_dir, 'PSpace_score'), 'rb') as f:
    PSpace_score = pickle.load(f)
with open(os.path.join(args.abs_dir, 'PSpace_index'), 'rb') as f:
    PSpace_index = pickle.load(f)
with open(os.path.join(args.abs_dir, 'RSC_index_array'), 'rb') as f:
    RSC_index_array = pickle.load(f)
with open(os.path.join(args.abs_dir, 'index2RSCindex'), 'rb') as f:
    index2RSCindex = pickle.load(f)
with open(os.path.join(args.abs_dir, 'RSCindex2index'), 'rb') as f:
    RSCindex2index = pickle.load(f)

X = np.load(os.path.join(args.dir, 'X.npy'))
y = np.load(os.path.join(args.dir, 'y.npy'))
Dist = np.load(os.path.join(args.dir, 'Dist.npy'))
NNindex = np.load(os.path.join(args.dir, 'NNindex.npy'))

def KNN(NNindex,index,k):
    K_index = NNindex[index][:k]
    return K_index

def RCD_auto(NNindex, PSpace_index, k, y):

    pick_num = 0
    Index_list = list(PSpace_index[k-args.KMIN])
    Index_list.reverse()
    Index_list = list(map(lambda x: RSCindex2index[x], Index_list))
    Found_class = set()
    start = time.time()
    while pick_num < 50:
        Top_index = Index_list[0]
        pick_num += 1
        K_index = KNN(NNindex, Top_index, k)
        Delete_index = set(K_index) & set(Index_list)

        if y[Top_index] not in Found_class:
            Found_class.add(y[Top_index])
            class_name = y[Top_index]
            print('Find class:', y[Top_index], 'index:', class_name, 'pick_num =', pick_num, 'Index:', Top_index)

        for i in Delete_index:
            Index_list.remove(i)

    end = time.time()
    return end - start

def RCD_interact(NNindex, PSpace_index, k, y):
    return

def main():
    while True:
        print('please enter the parameter k, enter any negative number to exit..')
        k = int(input())
        if k < 0:
            break
        RCD_auto(NNindex, PSpace_index, k, y)

if __name__ == '__main__':
    main()



