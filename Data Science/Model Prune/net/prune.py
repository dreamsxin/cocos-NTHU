import numpy as np
from torch.nn.modules.module import Module
from torch import from_numpy


class PruningModule(Module):
    DEFAULT_PRUNE_RATE = {
        'conv1': 84,
        'conv2': 38,
        'conv3': 35,
        'conv4': 37,
        'conv5': 37,
        'fc1': 9,
        'fc2': 9,
        'fc3': 25
    }

    def _prune(self, module, threshold):

        #################################
        # TODO:
        #    1. Use "module.weight.data" to get the weights of a certain layer of the model
        #    2. Set weights whose absolute value is less than threshold to 0, and keep the rest unchanged
        #    3. Save the results of the step 2 back to "module.weight.data"
        #    --------------------------------------------------------
        #    In addition, there is no need to return in this function ("module" can be considered as call by
        #    reference)
        #################################
        weight_dev = module.weight.device
        weights = module.weight.data.cpu().numpy()
        new_mask = np.where(abs(weights) < threshold, 0, weights)
        module.weight.data = from_numpy(weights * new_mask).to(weight_dev)
        #pass

    def prune_by_percentile(self, q=DEFAULT_PRUNE_RATE):

        ########################
        # TODO
        # 	For each layer of weights W (including fc and conv layers) in the model, obtain the (100 - q)th percentile
        # 	of absolute W as the threshold, and then set the absolute weights less than threshold to 0 , and the rest
        # 	remain unchanged.
        ########################
        
        for name, module in self.named_modules():
            if name == '':
                pass
            else:
                q_value = q.get(name)
                weights = module.weight.data.cpu().numpy()
                alive = []
                alive = weights[np.nonzero(weights)]
                threshold = np.percentile(abs(alive), (100 - q_value))
                print(f'Pruning with threshold : {threshold:.6f} for layer {name}')
                # Calculate percentile value
                #pass
                self._prune(module, threshold)
                # Prune the weights and ma
                #pass
    def prune_by_std(self, s=0.25):
        for name, module in self.named_modules():

            #################################
            # TODO:
            #    Only fully connected layers were considered, but convolution layers also needed
            #################################

            if name in ['fc1', 'fc2', 'fc3']:
                threshold = np.std(module.weight.data.cpu().numpy()) * s
                print(f'Pruning with threshold : {threshold:.4f} for layer {name}')
                self._prune(module, threshold)




