import numpy as np

# AI for a car with len(inputVector) eyes, a hidden layer of length 8, and outputs a list of length 3
class Brain:

    # LAYER 1 IS 8 X NUM_EYES, OUTPUTLAYER IS NUM_EYES X 8
    def __init__(self, layer1Weights, outputWeights):
        self.layers = [layer1Weights, outputWeights] ## layers is essentially a tensor
        
    def processLayer(self, inputVector, weightsMatrix):
        outputVector = weightsMatrix @ inputVector
        return self.sigmoid(outputVector)
           

    def process(self, inputs):
        processedVector = inputs
        for layer in self.layers:
            processedVector = self.processLayer(processedVector, layer)
            print(processedVector)
        
        

        return [processedVector[0] > .5, processedVector[1] > .5, processedVector[2] > .5]

    def sigmoid(self, vector):
        return 1 / (1 + np.exp(-vector)) 



##TESTING

# layer1 = np.array([[3, 1, 4],
#                    [1, 5, 9],
#                    [2, 6, 2],
#                    [3, 5, 8],
#                    [9, 7, 2],
#                    [3, 2, 3],
#                    [8, 4, 6],
#                    [2, 6, 4]])


# outputLayer = np.array([[2,7,1,8,2,8,1,8],
#                         [2,8,4,5,9,0,4,5],
#                         [2,3,5,3,6,0,2,8]])

# b = Brain(layer1, outputLayer)

# input = np.array([1, 0, 0])

# b.process(input)