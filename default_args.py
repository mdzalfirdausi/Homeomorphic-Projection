# def config():
#     defaults = {}
#     defaults['predType'] = ['NN', 'NN_Eq'][1]
#     defaults['projType'] = ['WS', 'Proj', 'D_Proj', 'H_Bis'][3]
#     defaults['probType'] = ['qp', 'socp', 'convex_qcqp', 'sdp', 'acopf'][4]
#     defaults['probSize'] = [[100, 50, 50, 10000], 
#                             [200, 100, 100, 20000]][1]
    
#     # 1. SMALLER DATASET: Use 500 samples for a quick local test
#     defaults['opfSize'] = [60,  10] 
#     defaults['testSize'] = 10
#     defaults['saveAllStats'] = False
#     defaults['resultsSaveFreq'] = 10
#     defaults['seed'] = 2026
  
#     defaults['mapping_para'] = \
#         {'training': True, 'testing': True,
#         'n_samples': 10,             # Match opfSize
#         't_samples': 32,              # Reduced for CPU speed
#         'bound': [0, 1],
#         'scale_ratio': 1,
#         'shape': 'square',
#         'total_iteration': 200,       # 2. REDUCED ITERATIONS: Enough to see convergence
#         'batch_size': 32,             # 3. SMALLER BATCH: Friendlier for CPU RAM
#         'num_layer': 4,
#         'lr': 1e-4,
#         'lr_decay': 0.9,
#         'lr_decay_step': 50,          # Adjusted for 200 total iterations
#         'penalty_coefficient': 100, 
#         'distortion_coefficient': 1,
#         'transport_coefficient': 0,
#         'testing_samples': 2,         # Fewer test samples for speed
#         'resultsSaveFreq': 100}

#     defaults['nn_para'] = \
#         {'training': True, 'testing': True,
#          'approach': 'supervise',     # Keep supervise to test your data logic
#         'total_iteration': 200,       # Match mapping iterations
#         'batch_size': 32,             
#         'lr': 1e-3,
#         'lr_decay': 0.9,
#         'lr_decay_step': 50,
#         'num_layer': 4,
#         'objWeight': 0.05,
#         'softWeightInEqFrac': 100,
#         'softWeightEqFrac': 100}

#     defaults['proj_para'] = \
#         {'useTestCorr': True,    
#         'corrMode': 'partial',      
#         'corrTestMaxSteps': 20,       # 4. FEWER BISECTION STEPS: Local CPU is slow here
#         'corrBis': 0.5,           
#         'corrEps': 1e-5,          
#         'corrLr': 1e-5,           
#         'corrMomentum': 0.1, }    

#     return defaults

################################################################################ zzz run this for cuda/hpc
# def config():
#     defaults = {}
#     defaults['predType'] = ['NN', 'NN_Eq'][1]
#     defaults['projType'] = ['WS', 'Proj', 'D_Proj', 'H_Bis'][3]
#     defaults['probType'] = ['qp', 'socp', 'convex_qcqp', 'sdp', 'acopf'][4]
#     defaults['probSize'] = [[100, 50, 50, 10000], 
#                             [200, 100, 100, 20000]][1]
#     defaults['opfSize'] = [60,  15000]
#     defaults['testSize'] = 1500       # CHANGED: 10% holdout for proper evaluation
#     defaults['saveAllStats'] = False
#     defaults['resultsSaveFreq'] = 500 # CHANGED: Scaled up to avoid I/O bottlenecks
#     defaults['seed'] = 2026
  
#     defaults['mapping_para'] = \
#         {'training': True, 'testing': True,
#         'n_samples': 15000,
#         't_samples': 256,             # CHANGED: Larger parameter sampling for better gradients
#         'bound': [0, 1],
#         'scale_ratio': 1,
#         'shape': 'square',
#         'total_iteration': 5000,      # CHANGED: Give the model time to converge
#         'batch_size': 256,            # CHANGED: Maximizing GPU parallelization
#         'num_layer': 4,
#         'lr': 1e-4,
#         'lr_decay': 0.9,
#         'lr_decay_step': 1000,        # CHANGED: Scaled to match the new total_iteration
#         'penalty_coefficient': 100, 
#         'distortion_coefficient': 1,
#         'transport_coefficient': 0,
#         'testing_samples': 5,
#         'resultsSaveFreq': 500}       # CHANGED: Match the global save frequency

#     defaults['nn_para'] = \
#         {'training': True, 'testing': True,
#          'approach': 'supervise',     # CHANGED: Crucial for utilizing your dataset labels
#         'total_iteration': 5000,      # CHANGED: ~100 epochs over the training set
#         'batch_size': 256,            # CHANGED: Maximizing GPU parallelization
#         'lr': 1e-3,
#         'lr_decay': 0.9,
#         'lr_decay_step': 1000,        # CHANGED: Scaled to match the new total_iteration
#         'num_layer': 4,
#         'objWeight': 0.05,
#         'softWeightInEqFrac': 100,
#         'softWeightEqFrac': 100}

#     defaults['proj_para'] = \
#         {'useTestCorr': True,    
#         'corrMode': 'partial',      
#         'corrTestMaxSteps': 100,  
#         'corrBis': 0.5,           
#         'corrEps': 1e-5,          
#         'corrLr': 1e-5,           
#         'corrMomentum': 0.1, }    

#     return defaults

def config():
    defaults = {}
    defaults['predType'] = ['NN', 'NN_Eq'][1]
    defaults['projType'] = ['WS', 'Proj', 'D_Proj', 'H_Bis'][3]
    defaults['probType'] = ['qp', 'socp', 'convex_qcqp', 'sdp', 'acopf'][4]
    defaults['probSize'] = [[100, 50, 50, 10000],
                            [200, 100, 100, 20000]][1]
    defaults['opfSize'] = [[30,  10000],
                           [118, 20000]][0]
    defaults['testSize'] = 1024
    defaults['saveAllStats'] = False
    defaults['resultsSaveFreq'] = 1000
    defaults['seed'] = 2023

    defaults['mapping_para'] = \
        {'training': True, 'testing': False,
        'n_samples': 1024,
        't_samples': 10000,
        'bound': [0, 1],
        'scale_ratio': 1,
        'shape': 'square',
        'total_iteration': 10000,
        'batch_size': 512,
        'num_layer': 3,
        'lr': 1e-4,
        'lr_decay': 0.9,
        'lr_decay_step': 1000,
        'penalty_coefficient': 10,
        'distortion_coefficient': 1,
        'transport_coefficient': 0,
        'testing_samples': 1024,
        'resultsSaveFreq': 500}


    defaults['nn_para'] = \
        {'training': False, 'testing': True,
         'approach': 'unsupervise',
        'total_iteration': 10000,
        'batch_size': 512,
        'lr': 1e-3,
        'lr_decay': 0.9,
        'lr_decay_step': 1000,
        'num_layer': 3,
        'objWeight': 0.1,
        'softWeightInEqFrac': 10,
        'softWeightEqFrac': 10}


    defaults['proj_para'] = \
        {'useTestCorr': False,    # post-process for infeasible solutions
        'corrMode': 'partial',    # equality completion
        'corrTestMaxSteps': 100,  # steps for D-Proj
        'corrBis': 0.9,           # steps for bisection
        'corrEps': 1e-5,          # tolerance for constraint violation
        'corrLr': 1e-5,           # stepsize for gradient descent in D-Proj
        'corrMomentum': 0.1, }    # momentum parameter in D-Proj

    return defaults
