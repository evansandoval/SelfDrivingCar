# Neural Network functionality 

import numpy as np

class Brain:
   
    # Initialized with Python List of ndArrays representing weights in layers of neural network
    def __init__(self, listOfLayers):
        self.layers = listOfLayers
           
    # Input:  Vector of length NUM_EYES
    # Output: Vector of length 4 (Left, Up, Right, Down)
    def processNeuralNet(self, inputs):
        processedVector = inputs
        for layer in self.layers:
            processedVector = self.processLayer(processedVector, layer)
        return [processedVector[0] > .5, processedVector[1] > .5, processedVector[2] > .5, processedVector[3] > .5]
    
    # Helper function to process one layer of Neural Network
    def processLayer(self, inputVector, weightsMatrix):
        outputVector = weightsMatrix @ inputVector
        return self.sigmoid(outputVector)

    # Utility function ensuring all outputs are between 0 and 1
    def sigmoid(self, vector):
        return 1 / (1 + np.exp(-vector)) 



#TESTING
# Test_Layers = [np.loadtxt("InjectedBrain/layer-0.csv"), np.loadtxt("InjectedBrain/layer-1.csv"), np.loadtxt("InjectedBrain/layer-2.csv")]
# b = Brain(Test_Layers)

# for i in range(2):
#     for j in range(2):
#         print("===========")
#         print("LeftEye: ", i)
#         print("RightEye:", j)
#         output = b.processNeuralNet(np.array([i,j]))
#         print("Left ", output[0])
#         print("Up   ", output[1])
#         print("Right", output[2])
#         print("Down ", output[3])
