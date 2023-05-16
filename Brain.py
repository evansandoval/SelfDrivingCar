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

# layer1 = np.array([[3, 1, 4],
#                    [1, 5, 9],
#                    [2, 6, 2],
#                    [3, 5, 8],
#                    [9, 7, 2],
#                    [3, 2, 3],
#                    [8, 4, 6],
#                    [2, 6, 4]])


# hiddenLayer = np.array([[1,2,3,4,5,6,7,8],
#                        [9,0,9,8,7,6,5,4],
#                        [3,2,1,2,3,4,5,6],
#                        [1,2,3,4,5,6,7,8],
#                        [9,0,9,8,7,6,5,4],
#                        [3,2,1,2,3,4,5,6],
#                        [1,2,3,4,5,6,7,8],
#                        [3,2,1,2,3,4,5,6],])

# outputLayer = np.array([[2,7,1,8,2,8,1,8],
#                         [2,8,4,5,9,0,4,5],
#                         [2,3,5,3,6,0,2,8],
#                         [5,3,5,1,6,6,3,5]])

# b = Brain(layer1, hiddenLayer, outputLayer)

# input = np.array([1, 0, 0])

# b.process(input)