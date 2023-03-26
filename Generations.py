import numpy as np
from Brain import Brain

# DEFAULT PARAMETERS
defaultStartX = 150
defaultStartY = 415
defaultSpeed = 100
defaultTurnRadius = 100
# defaultEyes = 3 # maybe even make this an input
defaultEyeParams = [(40,-45), (40,0), (40, 45)]

defaultParams = [defaultSpeed, defaultTurnRadius]

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
        for i in range(numCars):
            speed = params[0]
            turnRadius = params[1]
            brain = Brain(self.initBrainMatrices(len(eyeParams)))        
            self.cars.append(self.Car(speed, turnRadius, eyeParams, brain, x=defaultStartX, y=defaultStartY, batch=None))



    def createGeneration(self, params, brainParams=None):
        self.number += 1
        
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
        print("The top 10 fitness scores were:")
        for i in range(10):
            print(i, self.cars[i].getFitness())
        topHalf = self.cars[0:self.numCars//2]
        newParams = self.mixMutate([car.params       for car in topHalf])
        newEyes   = self.newEyes  ([car.eyeParams    for car in topHalf])
        # eyes need their own mix function to randomly mutate new eyes
        newBrains = self.mixMutate([car.brain.layers for car in topHalf])
        self.createGeneration(newParams, newBrains)



    def isDead(self):
        lifeStatus = [car.dead for car in self.cars]
        return all(lifeStatus)

    def sortByFitness(self):
        self.cars.sort(key=lambda car: car.getFitness(), reverse=True)
        

