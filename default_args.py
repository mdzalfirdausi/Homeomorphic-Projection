def config():
    defaults = {}
    defaults['predType'] = ['NN', 'NN_Eq'][1]
    defaults['projType'] = ['WS', 'Proj', 'D_Proj', 'H_Bis'][3]
    defaults['probType'] = ['qp', 'socp', 'convex_qcqp', 'sdp', 'acopf'][4]
    defaults['probSize'] = [[100, 50, 50, 10000], 
                            [200, 100, 100, 20000]][1]
    defaults['opfSize'] = [30,  10] # Adjust this as needed
    defaults['testSize'] = 1
    defaults['saveAllStats'] = False
    defaults['resultsSaveFreq'] = 5
    defaults['seed'] = 2026
  
    defaults['mapping_para'] = \
        {'training': False, 'testing': True,
        'n_samples': 500,
        't_samples': 10,
        'bound': [0, 1],
        'scale_ratio': 1,
        'shape': 'square',
        'total_iteration': 300, 
        'batch_size': 32,
        'num_layer': 3,
        'lr': 1e-4,
        'lr_decay': 0.9,
        'lr_decay_step': 50,
        'penalty_coefficient': 50, 
        'distortion_coefficient': 1,
        'transport_coefficient': 0,
        'testing_samples': 5,
        'resultsSaveFreq': defaults['resultsSaveFreq']}

    defaults['nn_para'] = \
        {'training': False, 'testing': False,
         'approach': 'unsupervise',
        'total_iteration': 500,
        'batch_size': 32, 
        'lr': 1e-3,
        'lr_decay': 0.9,
        'lr_decay_step': 100,
        'num_layer': 3,
        'objWeight': 0.01,
        'softWeightInEqFrac': 100,
        'softWeightEqFrac': 100}

    defaults['proj_para'] = \
        {'useTestCorr': False,    
        'corrMode': 'partial',      
        'corrTestMaxSteps': 100,  
        'corrBis': 0.9,           
        'corrEps': 1e-5,          
        'corrLr': 1e-5,           
        'corrMomentum': 0.1, }    

    return defaults