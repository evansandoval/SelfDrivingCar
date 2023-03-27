import numpy as np
from Brain import Brain

# DEFAULT PARAMETERS
defaultStartX = 150
defaultStartY = 415
defaultSpeed = 100.0
defaultTurnRadius = 100.0
# defaultEyes = 3 # maybe even make this an input
defaultEyeParams = [(50, -90),(40,-45), (130,0), (40, 45), (50, 90)]

defaultParams = np.array([defaultSpeed, defaultTurnRadius])

# INPUTS
# leftEye = 0 or 1 (inbounds or not inbounds)
# frontEye = 0 or 1 (inbounds or not inbounds)
# rightEye = 0 or 1 (inbounds or not inbounds)

# find ideal connections between eyes and output values

# OUTPUTS
# forward = 0 or 1
# backward = 0 or 1
# left = 0 or 1
# right = 0 or 1

class Generation:
    def __init__(self, CarConstructor, numCars, params=defaultParams, eyeParams=defaultEyeParams, showEyes=True):
        self.number = 1
        self.showEyes = showEyes
        self.numCars = numCars
        self.Car = CarConstructor
        self.cars = []
        for _ in range(numCars):
            speed = params[0]
            turnRadius = params[1]
            brain = Brain(self.initBrainMatrices(len(eyeParams)))        
            self.cars.append(self.Car(speed, turnRadius, eyeParams, brain, x=defaultStartX, y=defaultStartY, batch=None))



    def createGeneration(self, params, eyeParams, brainParams=None):
        self.number += 1
        self.cars = []
        for i in range(self.numCars):
            speed = params[i][0]
            turnRadius = params[i][1]
            brain = Brain(brainParams[i])     
            self.cars.append(self.Car(speed, turnRadius, eyeParams, brain, x=defaultStartX, y=defaultStartY, batch=None))


        
    def initBrainMatrices(self, numInputs):
        # Brain needs at least three matrices in order to compute
        #     8 x numEyes || 8 x 8 || 4 x 8
        # to add more hidden layers, simply add more 8x8 matrices in the middle

        # initialize random matrices using a UNIFORM distribution
        inputMatrix = np.random.uniform(-1, 1, (8, numInputs))
        hiddenMatrix = np.random.uniform(-1, 1, (8, 8))
        outputMatrix = np.random.uniform(-1, 1, (4, 8))
        return [inputMatrix, hiddenMatrix, outputMatrix]
    
    def nextGeneration(self):
        self.sortByFitness()
        print(f"Generation {self.number}'s top 10 fitness scores:")
        for i in range(10):
            print(i, self.cars[i].getFitness())
        topHalf = self.cars[0:self.numCars//2]
        newParams = self.mixMutate([car.params       for car in topHalf])
        newEyes   = self.newEyes  ([car.eyeParams    for car in topHalf])
        # eyes need their own mix function to randomly mutate new eyes
        newBrains = self.newBrain(topHalf)
        self.createGeneration(newParams, defaultEyeParams, newBrains)
        

    def newBrain(self, topHalf):
        numberOfLayers = len(topHalf[0].brain.layers)
        #collects new generation of newly mutated weights matrices (organized in order)
        separateLayers = []
        for layerIndex in range(numberOfLayers):
            separateLayers.append(self.mixMutate([car.brain.layers[layerIndex] for car in topHalf]))
        #reorganize the new matrices into where they're supposed to be in the brains
        brainList = []
        numCars = len(separateLayers[0])
        for carIndex in range(numCars):
            brainList.append([separateLayers[layerIndex][carIndex] for layerIndex in range(numberOfLayers)])
        return brainList

    def newEyes(self, lst):
        return

    def mixMutate(self, lst):
        for i in range(len(lst)):
                average = (lst[i] + lst[i+1]) / 2
                lst.append(average)
        for item in lst:
            shape = np.shape(item)
            item += np.random.normal(size=shape)
        return lst


    def isDead(self):
        lifeStatus = [car.dead for car in self.cars]
        return all(lifeStatus)

    def sortByFitness(self):
        self.cars.sort(key=lambda car: car.getFitness(), reverse=True)
        

