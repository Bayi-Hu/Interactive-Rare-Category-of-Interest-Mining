# -*- coding:utf-8 -*-
import numpy as np
import time
from Code.Configuration import Args
import os
import pickle

args = Args('Abalone')

# Load Abstraction
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

X = np.load(os.path.join(args.dir, 'X.npy'), allow_pickle=True)
y = np.load(os.path.join(args.dir, 'y.npy'), allow_pickle=True)
Dist = np.load(os.path.join(args.dir, 'Dist.npy'))
NNindex = np.load(os.path.join(args.dir, 'NNindex.npy'))

def Sample_Construct(NNindex, Abs_idx, k, X, y, string2index=None):
    '''
    :param NNindex:
    :param Abs_idx:
    :param k:
    :param y:
    :param string2index:
    :return:
    '''
    pick_num = 0
    Index_list = list(Abs_idx[k - args.KMIN])
    Index_list.reverse()
    Index_list = map(lambda x: AbsIdx2Idx[x], Index_list)
    Pos_sample_set = set()
    Neg_sample_set = set()
    # construct_num = max(100, 2*k)
    construct_num = 1000
    check_list = [1]

    for i in range(150):
        print(Index_list[i], y[Index_list[i]])

    print('Mining ？ (y/[n])?')
    yes = int(input())
    if yes != 'y' or 'yes':
        print('finishing..')
        return
    else:
        print('resuming operation...')

    print('Please enter the index of sample you are interested in.'),
    first_sample = int(input())
    arg_first_sample = np.where(np.array(Index_list) == first_sample)[0][0]

    Interesting_set = set(Index_list[arg_first_sample + 1:arg_first_sample + construct_num + 1])
    target_class = y[first_sample]
    Pos_sample_set.add(first_sample)

    start = time.time()

    for iter in range(k - 1):

        candidate = list(Interesting_set)
        similarity = dict()
        Info = dict()

        for c in candidate:
            sample_pos = X[[first_sample]]

            for i in Pos_sample_set:
                if i != first_sample:
                    sample_pos = np.concatenate([sample_pos, X[[i]]], axis=0)

            D = np.concatenate([sample_pos, -X[[c]]], axis=0).T
            e = np.ones(D.shape[1] - 1)
            # e = np.zeros(D.shape[1]-1)
            gamma1 = 10000  # Penalty
            gamma2 = 1
            gamma = 1

            B = np.eye(D.shape[1])
            # B *= gamma
            B[:-1] *= gamma1
            B[-1] *= gamma2
            u = np.expand_dims(np.concatenate([e, np.zeros(1)], axis=0), axis=1)
            # u = np.expand_dims(np.concatenate([e, np.ones(1)], axis= 0), axis=1)
            P = np.matmul(D.T, D) + B
            P_I = np.linalg.inv(P)
            x = np.matmul(P_I, u) / (np.matmul(np.matmul(u.T, P_I), u))
            a = x[0:-1].T
            # a = np.abs(a)
            b = x[-1]
            # print(b)
            # print(a)
            # b = np.abs(b)
            # similarity[c] = -1 * (np.linalg.norm(np.matmul(a,sample_pos) - X[c])**2)
            similarity[c] = -1 * (np.linalg.norm(np.matmul(a, sample_pos) - b * X[c]) ** 2)
            Info[c] = []
            Info[c].append(('pos_a', a))
            Info[c].append(('pos_b', b))
            # print('similarity:',similarity[c])
            # print(y[c])
            # print('------')

            if len(Neg_sample_set):
                Neg_sample = list(Neg_sample_set)
                sample_neg = X[[Neg_sample[0]]]
                for i in Neg_sample:
                    if i != Neg_sample[0]:
                        sample_neg = np.concatenate([sample_neg, X[[i]]], axis=0)

                D = np.concatenate([sample_neg, -X[[c]]], axis=0).T
                e = np.ones(D.shape[1] - 1)
                # e = np.zeros(D.shape[1] - 1)

                B = np.eye(D.shape[1])
                # B *= gamma
                B[:-1] *= gamma1
                B[-1] *= gamma2
                u = np.expand_dims(np.concatenate([e, np.zeros(1)], axis=0), axis=1)
                # u = np.expand_dims(np.concatenate([e, np.ones(1)], axis=0), axis=1)
                P = np.matmul(D.T, D) + B
                P_I = np.linalg.inv(P)
                x = np.matmul(P_I, u) / (np.matmul(np.matmul(u.T, P_I), u))
                a = x[0:-1].T
                # a = np.abs(a)
                b = x[-1]
                # print(a)
                # print(b)
                # b = np.abs(b)
                # similarity[c] +=  (np.linalg.norm(np.matmul(a, sample_neg) - X[c]) ** 2)
                similarity[c] += 1 * (np.linalg.norm(np.matmul(a, sample_neg) - b * X[c]) ** 2)
                Info[c].append(('neg_a', a))
                Info[c].append(('neg_b', b))

        Sorted = np.array(sorted(similarity.items(), key=lambda similarity: similarity[1], reverse=True)).astype(int)
        check = Sorted[0][0]

        m = k - 1 - iter
        top_m = Sorted[:m, 0]

        # top_m precision
        fenzi = 0
        for i in top_m:
            if y[i] == target_class:
                fenzi += 1

        # print(Info[check])
        if y[check] == target_class:
            Pos_sample_set.add(check)
            check_list.append(1)
            print(iter + 1, 'gocha!', check, y[check])
        else:
            Neg_sample_set.add(check)
            print(iter + 1, 'T.T', check, y[check])
            check_list.append(0)

        Interesting_set.remove(check)
    end = time.time()
    print((end - start) * 1.0 / (k - 1))

    return check_list, target_class


def Sample_Construct_constrainb(NNindex, Abs_idx, k, X, y, string2index=None):
    '''
        :param NNindex:
        :param Abs_idx:
        :param k:
        :param y:
        :param string2index:
        :return:
        '''
    pick_num = 0
    Index_list = list(Abs_idx[k - args.KMIN])
    Index_list.reverse()
    Index_list = map(lambda x: AbsIdx2Idx[x], Index_list)
    start = time.time()
    Pos_sample_set = set()
    Neg_sample_set = set()
    # construct_num = max(100, 2*k)
    construct_num = 1000
    check_list = [1]

    for i in range(150):
        print(Index_list[i], y[Index_list[i]])

    print('Mining ？ (y/[n])?')
    yes = int(input())
    if yes != 'y' or 'yes':
        print('finishing..')
        return
    else:
        print('resuming operation...')

    print('Please enter the index of sample you are interested in.'),
    first_sample = int(input())
    arg_first_sample = np.where(np.array(Index_list) == first_sample)[0][0]

    Interesting_set = set(Index_list[arg_first_sample + 1:arg_first_sample + construct_num + 1])
    target_class = y[first_sample]
    Pos_sample_set.add(first_sample)

    for iter in range(k - 1):

        candidate = list(Interesting_set)
        similarity = dict()
        Info = dict()

        for c in candidate:
            sample_pos = X[[first_sample]]

            for i in Pos_sample_set:
                if i != first_sample:
                    sample_pos = np.concatenate([sample_pos, X[[i]]], axis=0)

            D = (sample_pos - X[[c]]).T
            e = np.ones(D.shape[1])
            # e = np.zeros(D.shape[1]-1)
            # gamma1 = 1000  # Penalty
            # gamma2 = 1
            gamma1 = 100

            B = np.eye(D.shape[1])
            B *= gamma1
            u = np.expand_dims(e, axis=1)
            # u = np.expand_dims(np.concatenate([e, np.ones(1)], axis= 0), axis=1)
            P = np.matmul(D.T, D) + B
            P_I = np.linalg.inv(P)
            a = np.matmul(P_I, u) / (np.matmul(np.matmul(u.T, P_I), u))
            # a = np.abs(a)
            # print(a)
            similarity[c] = -1 * (np.linalg.norm(np.matmul(a.T, sample_pos) - X[[c]]) ** 2)
            Info[c] = []
            Info[c].append(('pos_a', a))
            # Info[c].append(('pos_b', b))
            # print('similarity:',similarity[c])
            # print(y[c])
            # print('------')

            if len(Neg_sample_set):
                Neg_sample = list(Neg_sample_set)
                sample_neg = X[[Neg_sample[0]]]
                for i in Neg_sample:
                    if i != Neg_sample[0]:
                        sample_neg = np.concatenate([sample_neg, X[[i]]], axis=0)

                D = (sample_neg - X[[c]]).T
                e = np.ones(D.shape[1])
                # e = np.zeros(D.shape[1] - 1)
                gamma2 = 1000
                B = np.eye(D.shape[1])
                # B *= gamma
                B *= gamma2
                u = np.expand_dims(e, axis=1)
                # u = np.expand_dims(np.concatenate([e, np.ones(1)], axis=0), axis=1)
                P = np.matmul(D.T, D) + B
                P_I = np.linalg.inv(P)
                a = np.matmul(P_I, u) / (np.matmul(np.matmul(u.T, P_I), u))
                # a = np.abs(a)
                # print(a)
                # print(b)
                # b = np.abs(b)
                similarity[c] += 0.3 * (np.linalg.norm(np.matmul(a.T, sample_neg) - X[[c]]) ** 2)
                Info[c].append(('neg_a', a))

        Sorted = np.array(sorted(similarity.items(), key=lambda similarity: similarity[1], reverse=True)).astype(int)
        check = Sorted[0][0]

        m = k - 1 - iter
        top_m = Sorted[:m, 0]

        # 计算precision
        fenzi = 0
        for i in top_m:
            if y[i] == target_class:
                fenzi += 1

        # print(Info[check])
        if y[check] == target_class:
            Pos_sample_set.add(check)
            check_list.append(1)
            print(iter + 1, 'gocha!', check, y[check])
        else:
            Neg_sample_set.add(check)
            print(iter + 1, 'T.T', check, y[check])
            check_list.append(0)

        Interesting_set.remove(check)

    print(sum(check_list) * 1.0 / len(check_list))
    return check_list, target_class

def main():

    count = dict()
    for i in y:
        try:
            count[i] += 1
        except:
            count[i] = 1

    while 1:
        print('please enter the parameter k, enter any negative number to exit..')
        k = int(input())
        if k < 0:
            break

        (check_list, category) = Sample_Construct(NNindex, Abs_idx, k, X, y)
        #(check_list, category) = Sample_Construct_constrainb(NNindex, Abs_idx, k, X, y)
        accuracy_k = sum(check_list)*1.0/len(check_list)
        print('accuracy = ', accuracy_k)
        recall = sum(check_list)*1.0/count[category]

if __name__ == '__main__':
    main()

