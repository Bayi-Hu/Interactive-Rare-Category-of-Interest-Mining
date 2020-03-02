# -*- coding:utf-8 -*-
import numpy as np
import time
from Code.Configuration import Args
import os
import pickle
import bisect

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
    '''
    Find k-nearest neighbors for a certain data sample.
    '''
    K_index = NNindex[index][:k]
    return K_index

def RCD_auto(NNindex, Abs_idx, k, y):
    '''
    For convience of rare category detection, we set up an automatic RCD function, i.e.,
    assume that the category user interested in is one of the category of the dataset.
    This function select top data samples according to their candidate scores,
    and applied kNN rules automatically to eliminate data samples from discovered categories.
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

def RCD_interact(NNindex, Abs_idx, Abs_scr, k):
    '''
    To align with the settings in the paper, we set up an interactive RCD function.
    The input is an query triple <k,s_low, s_up>,
    where k represents the expected number of data examples in the rare category to be detected,
    s_low and s_up denote the lower and upper bounds of the rare category candidate score.
    '''
    label_time = 0

    Index_list = list(Abs_idx[k - args.KMIN])
    Index_list = list(map(lambda x: AbsIdx2Idx[x], Index_list))
    Found_class = set()

    Score_list = list(Abs_scr[k - args.KMIN])
    print('The range of candidate score scales from', Score_list[0],'to',Score_list[-1])
    print('please enter the parameter <s_low, s_up> for this query'),
    print('s_low = '),
    s_low = float(input())
    print('s_up = '),
    s_up = float(input())

    idx_low = bisect.bisect_left(Score_list, s_low)
    idx_up = bisect.bisect_right(Score_list, s_up)

    Query_list = Index_list[idx_low:idx_up]
    Query_list.reverse()

    #一个切片list
    print('There are',len(Query_list),'data samples included in this query and will be labeled sequentially according to the candidate score (From big to small)')
    print('1 for intereseted, 0 for not intereseted.')
    pick_num = 0
    Label_dict = {}

    while True:

        if len(Query_list) == 0:
            print('Mining finishing..')
            break

        Top_index = Query_list[0]
        pick_num += 1
        print('please label this sample, 1 for interested in , 0 for uninterested in.')
        label = (input())
        # record user's interest
        Label_dict[Top_index] = label
        print('Applied kNN rule for this sample? (y/[n])?')
        yes = str(input())
        if yes in ('y', 'yes'):
            # applied kNN rule to eluminate similar data samples
            K_index = KNN(NNindex, Top_index, k)
            Delete_index = set(K_index) & set(Query_list)

            for i in Delete_index:
                Query_list.remove(i)

    return Label_dict

def main():

    # while True:
    #     print('please enter the parameter k, enter any negative number to exit..')
    #     k = int(input())
    #     if k < 0:
    #         print('finishing..')
    #         break
    #     RCD_auto(NNindex, Abs_idx, k, y)

    while True:
        print('please enter the parameter k, enter any negative number to exit..')
        k = int(input())
        if k < 0:
            print('finishing..')
            break
        RCD_interact(NNindex, Abs_idx, Abs_scr, k)


if __name__ == '__main__':
    main()



