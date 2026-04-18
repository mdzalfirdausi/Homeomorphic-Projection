import os
import pickle
import numpy as np
import sys
import scipy.io
sys.path.insert(1, os.path.join(sys.path[0], os.pardir, os.pardir))
# from utils import ACOPFProblem
# [3,5,24,30,73, 118, 200, 300, 500, 1354, 2000
nbus = 118
num = 8

data = scipy.io.loadmat('./matlab_datasets/data/ACOPF_01_variation/FeasiblePairs_case{}.mat'.format(nbus))
ppc_mat = scipy.io.loadmat('./matlab_datasets/data/ACOPF_01_variation/case{}.mat'.format(nbus))
# ... (Top part of your script remains the same)

# FIX: Use .item() to avoid NumPy DeprecationWarnings
ppc = {
    'version': int(ppc_mat['my_model']['version'][0, 0].item()),
    'baseMVA': float(ppc_mat['my_model']['baseMVA'][0, 0].item()),
    'bus': ppc_mat['my_model']['bus'][0, 0],
    'gen': ppc_mat['my_model']['gen'][0, 0],
    'branch': ppc_mat['my_model']['branch'][0, 0],
    'gencost': ppc_mat['my_model']['gencost'][0, 0]
}
data['ppc'] = ppc

np.random.seed(2023)
sample_index = np.random.choice([i for i in range(data['Dem'].T.shape[0])], num, replace=False)
data['Dem'] = data['Dem'].T[sample_index, :]
data['Gen'] = data['Gen'].T[sample_index, :]
data['Vol'] = data['Vol'].T[sample_index, :]

# FIX: Save to the current directory instead of a nested path
filename = "acopf_{}_{}_dataset".format(nbus, num)
with open(filename, 'wb') as f:
    pickle.dump(data, f)

print(f"Successfully saved: {filename}")