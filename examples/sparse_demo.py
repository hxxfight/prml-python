import numpy as np
import matplotlib.pyplot as plt
from basic.regressor import *
# from bayesian.regressor import *
# from bayesian.pymc3 import *
from bayesian.pytorch import *
from sklearn.linear_model import ARDRegression

N = 256
P = 512 # feature dimension
X = np.random.randn(N,P).astype(np.float32)
# designed weights
NG = 32 # number of groups
PG = np.floor(P/NG).astype(int) # number of feature per-group
groups = np.floor(np.arange(P)/PG).astype(int) + 1
NSG = 10 # number of active groups
perm = np.random.permutation(NG)
actives = perm[:NSG] + 1
w0 = np.zeros(P)
for i in range(NSG):
    indices = np.squeeze(np.argwhere(groups == actives[i]))
    w0[indices] = np.random.randn(len(indices)) # gaussian signal
    # w0[indices] = np.ones(len(indices)) # uniform signal
# design matrix and class label
sigma = 0.1
y = np.dot(X, w0) + sigma*np.random.randn(N)

ardr = ARDRegression()
ardr.fit(X, y)
w1 = ardr.coef_

# w2, b2 = bayesreg(y, X)
# w2, b2 = bardreg(y, X)
w2, b2 = bgardreg(y, X, groups)

# visualize
plt.figure(1)

plt.subplot(3,1,1)
plt.plot(w0)
plt.axis('tight')
plt.ylim([-2, 2])
plt.title('raw')

plt.subplot(3,1,2)
plt.plot(w1)
plt.axis('tight')
plt.ylim([-2, 2])
plt.title('ardreg')

plt.subplot(3,1,3)
plt.plot(w2)
plt.axis('tight')
plt.title('bardreg')
plt.show()