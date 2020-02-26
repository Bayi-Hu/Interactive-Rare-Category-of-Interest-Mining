# -*- coding:utf-8 -*-
import numpy as np
import time
from Code.Configuration import Args
import os
import pickle

args = Args('Abalone')

# Load Abastraction
with open(os.path.join(args.abs_dir, 'Abs_scr'), 'rb') as f:
    Abs_scr = pickle.load(f)
with open(os.path.join(args.abs_dir, 'Abs_idx'), 'rb') as f:
    Abs_idx = pickle.load(f)
with open(os.path.join(args.abs_dir, 'Abs_idx_lst'), 'rb') as f:
    Abs_idx_lst = pickle.load(f)
with open(os.path.join(args.abs_dir, 'Idx2AbsIdx'), 'rb') as f:
    Idx2AbsIdx = pickle.load(f)
with open(os.path.join(args.abs_dir, 'AbsIdx2Idx'), 'rb') as f:
    AbsIdx2Idx = pickle.load(f)

X = np.load(os.path.join(args.dir, 'X.npy'))
y = np.load(os.path.join(args.dir, 'y.npy'))
Dist = np.load(os.path.join(args.dir, 'Dist.npy'))
NNindex = np.load(os.path.join(args.dir, 'NNindex.npy'))

def KNN(NNindex,index,k):
    K_index = NNindex[index][:k]
    return K_index

def RCD_auto(NNindex, Abs_idx, k, y):
    '''
    For convience of rare category detection, we set up an automatic RCD function, i.e.,
    assume that the category user interested in is one of the category of the dataset.
    This function works on Abalone, Bird, Shuttle and Kddcup datasets(have class labels themselves).
    '''

    pick_num = 0
    Index_list = list(Abs_idx[k-args.KMIN])
    Index_list.reverse()
    Index_list = list(map(lambda x: AbsIdx2Idx[x], Index_list))
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
            print('Find class:', class_name, 'index:', Top_index, 'pick_num =', pick_num)

        for i in Delete_index:
            Index_list.remove(i)

    end = time.time()
    return end - start

def RCD_interact(NNindex, Abs_idx, k, y):
    '''

    '''
    return

def main():
    while True:
        print('please enter the parameter k, enter any negative number to exit..')
        k = int(input())
        if k < 0:
            break
        RCD_auto(NNindex, Abs_idx, k, y)

if __name__ == '__main__':
    main()



