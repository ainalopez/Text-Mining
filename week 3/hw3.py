# -*- coding: utf-8 -*-
"""
Created on Thu May  5 14:05:41 2016

@author: yaroslav
"""

import numpy as np
import random

# Parameters
K=3
alpha=1
eta=1
D=15
V=10
Vd=[6]*D # number of words in document d

#random.seed(666) 
# Draw beta
seed(111)
beta = np.random.dirichlet([eta]*V, K)


# Draw rho
seed(222)
rho = np.random.dirichlet([alpha]*K, 1)
rho=rho[0] # to avoid error in next step
rho

# Draw z
z=[argmax(np.random.multinomial(1, rho, size=1)) for i in range(D)] 

# Draw words
docs=[]
for d in range(D):
    docs.append([argmax(np.random.multinomial(1, beta[z[d]], size=1)) for i in range(Vd[d])] )
