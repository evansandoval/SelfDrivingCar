import numpy as np

# AI for a car with len(inputVector) eyes, two hidden layers of length 8, and outputs a list of length 4
class Brain:

    #INPUT LAYER IS 8 X (NUM_EYES), HIDDEN LAYER IS 8X8,  OUTPUTLAYER IS 4 X 8
    def __init__(self, listOfLayers):
        self.layers = listOfLayers ## layers is essentially a tensor
    
    def processLayer(self, inputVector, weightsMatrix):
        outputVector = weightsMatrix @ inputVector
        return self.sigmoid(outputVector)
           

    def process(self, inputs):
        processedVector = inputs
        for layer in self.layers:
            processedVector = self.processLayer(processedVector, layer)
        return [processedVector[0] > .5, processedVector[1] > .5, processedVector[2] > .5, processedVector[3] > .5]
    
    def sigmoid(self, vector):
        return 1 / (1 + np.exp(-vector)) 



##TESTING

# Test_Layers = [np.loadtxt("InjectedBrain/Track2-F1554-G50/layer-0.csv"), np.loadtxt("InjectedBrain/Track2-F1554-G50/layer-1.csv"), np.loadtxt("InjectedBrain/Track2-F1554-G50/layer-2.csv")]
# b = Brain(Test_Layers)

# for i in range(2):
#     for j in range(2):
#         print("===========")
#         print("LeftEye: ", i)
#         print("RightEye:", j)
#         output = b.process(np.array([i,j]))
#         print("Left ", output[0])
#         print("Up   ", output[1])
#         print("Right", output[2])
#         print("Down ", output[3])
