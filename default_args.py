def config():
    defaults = {}
    defaults['predType'] = ['NN', 'NN_Eq'][1]
    defaults['projType'] = ['WS', 'Proj', 'D_Proj', 'H_Bis'][3]
    defaults['probType'] = ['qp', 'socp', 'convex_qcqp', 'sdp', 'acopf'][4]
    defaults['probSize'] = [[100, 50, 50, 10000], 
                            [200, 100, 100, 20000]][1]
    defaults['opfSize'] = [300,  1000] # Adjust this as needed
    defaults['testSize'] = 1024
    defaults['saveAllStats'] = False
    defaults['resultsSaveFreq'] = 500
    defaults['seed'] = 2026
 
    defaults['mapping_para'] = \
        {'training': True, 'testing': True,
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
        'testing_samples': 1024}

    defaults['nn_para'] = \
        {'training': True, 'testing': True,
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
        {'useTestCorr': False,    
        'corrMode': 'partial',      
        'corrTestMaxSteps': 100,  
        'corrBis': 0.9,           
        'corrEps': 1e-5,          
        'corrLr': 1e-5,           
        'corrMomentum': 0.1, }    

    return defaults