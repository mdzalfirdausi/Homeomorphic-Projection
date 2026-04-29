# def config():
#     defaults = {}
#     defaults['predType'] = ['NN', 'NN_Eq'][1]
#     defaults['projType'] = ['WS', 'Proj', 'D_Proj', 'H_Bis'][3]
#     defaults['probType'] = ['qp', 'socp', 'convex_qcqp', 'sdp', 'acopf'][4]
#     defaults['probSize'] = [[100, 50, 50, 10000], 
#                             [200, 100, 100, 20000]][1]
#     defaults['opfSize'] = [30,  10] # Adjust this as needed
#     defaults['testSize'] = 1
#     defaults['saveAllStats'] = False
#     defaults['resultsSaveFreq'] = 50
#     defaults['seed'] = 2026
  
#     defaults['mapping_para'] = \
#         {'training': True, 'testing': True,
#         'n_samples': 1000,
#         't_samples': 64,
#         'bound': [0, 1],
#         'scale_ratio': 1,
#         'shape': 'square',
#         'total_iteration': 1000, 
#         'batch_size': 64,
#         'num_layer': 4,
#         'lr': 1e-4,
#         'lr_decay': 0.9,
#         'lr_decay_step': 200,
#         'penalty_coefficient': 100, 
#         'distortion_coefficient': 1,
#         'transport_coefficient': 0,
#         'testing_samples': 5,
#         'resultsSaveFreq': defaults['resultsSaveFreq']}

#     defaults['nn_para'] = \
#         {'training': True, 'testing': True,
#          'approach': 'unsupervise',
#         'total_iteration': 1000,
#         'batch_size': 64, 
#         'lr': 1e-3,
#         'lr_decay': 0.9,
#         'lr_decay_step': 200,
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

################################################################################ run this for cuda/hpc
def config():
    defaults = {}
    defaults['predType'] = ['NN', 'NN_Eq'][1]
    defaults['projType'] = ['WS', 'Proj', 'D_Proj', 'H_Bis'][3]
    defaults['probType'] = ['qp', 'socp', 'convex_qcqp', 'sdp', 'acopf'][4]
    defaults['probSize'] = [[100, 50, 50, 10000], 
                            [200, 100, 100, 20000]][1]
    defaults['opfSize'] = [60,  10] # Adjust this as needed
    defaults['testSize'] = 1
    defaults['saveAllStats'] = False
    defaults['resultsSaveFreq'] = 50
    defaults['seed'] = 2026
  
    defaults['mapping_para'] = \
        {'training': True, 'testing': True,
        'n_samples': 1000,
        't_samples': 64,
        'bound': [0, 1],
        'scale_ratio': 1,
        'shape': 'square',
        'total_iteration': 1000, 
        'batch_size': 64,
        'num_layer': 4,
        'lr': 1e-4,
        'lr_decay': 0.9,
        'lr_decay_step': 200,
        'penalty_coefficient': 100, 
        'distortion_coefficient': 1,
        'transport_coefficient': 0,
        'testing_samples': 5,
        'resultsSaveFreq': defaults['resultsSaveFreq']}

    defaults['nn_para'] = \
        {'training': True, 'testing': True,
         'approach': 'unsupervise',
        'total_iteration': 1000,
        'batch_size': 64, 
        'lr': 1e-3,
        'lr_decay': 0.9,
        'lr_decay_step': 200,
        'num_layer': 4,
        'objWeight': 0.05,
        'softWeightInEqFrac': 100,
        'softWeightEqFrac': 100}

    defaults['proj_para'] = \
        {'useTestCorr': True,    
        'corrMode': 'partial',      
        'corrTestMaxSteps': 100,  
        'corrBis': 0.5,           
        'corrEps': 1e-5,          
        'corrLr': 1e-5,           
        'corrMomentum': 0.1, }    

    return defaults
