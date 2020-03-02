# -*- coding:utf-8 -*-
import os

# Parameter Settings
class Args(object):
    def __init__(self, dataset):
        self.dataset = dataset
        if self.dataset == 'Abalone':
            self.KMIN = 2
            self.KMAX = 200

        elif self.dataset == 'Shuttle':
            self.KMIN = 2
            self.KMAX = 200

        elif self.dataset == 'Kddcup':
            self.KMIN = 2
            self.KMAX = 500

        elif self.dataset == 'Bird':
            self.KMIN = 2
            self.KMAX = 200

        elif self.dataset == 'Game':
            self.KMIN = 2
            self.KMAX = 1000

        else:
            raise Exception('No Dataset named', self.dataset, '.')

        self.INFINITESIMAL = -99999
        self.rp = 0.1
        self.dir = os.path.join('../Dataset', self.dataset,'Features') # directory of data.
        self.abs_dir = os.path.join('../Interval_abstraction', self.dataset) # directory of abstraction.


