import numpy as np
from Brain import Brain

# DEFAULT PARAMETERS
defaultStartX = 150
defaultStartY = 415
defaultSpeed = 100
defaultTurnRadius = 100
# defaultEyes = 3 # maybe even make this an input
defaultEyeDistance = 40 #number of pixels
defaultEyeAngles = [-45, 0, 45] #NUMBER OF EYES WILL BE LENGTH OF THIS ARRAY

defaultParams = [defaultSpeed, defaultTurnRadius, defaultEyeDistance, defaultEyeAngles]

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
    def __init__(self, CarConstructor, numCars, params=defaultParams, showEyes=True):
        self.cars = []
        self.number = 1
        self.showEyes = showEyes
        for _ in range(numCars):
            speed = params[0]
            turnRadius = params[1]
            eyeDist = params[2]
            eyeAngles = params[3]
            brain = Brain(self.initBrainMatrices(len(eyeAngles)))
            self.cars.append(CarConstructor(speed, turnRadius, eyeDist, eyeAngles, brain, x=defaultStartX, y=defaultStartY, batch=None))

    def initBrainMatrices(self, numInputs):
        # Brain needs at least three matrices in order to compute
        #     8 x numEyes || 8 x 8 || 4 x 8
        # if adding more hidden layers, simply add more 8x8 matrices in the middle

        # initialize random matrices using a UNIFORM distribution
        inputMatrix = np.random.uniform(-1, 1, (8, numInputs))
        hiddenMatrix = np.random.uniform(-1, 1, (8, 8))
        outputMatrix = np.random.uniform(-1, 1, (4, 8))
        return [inputMatrix, hiddenMatrix, outputMatrix]
    
    def endGeneration(self):
        self.sortByFitness()
        print("The top 20 fitness scores were:")
        for i in range(20):
            print(i, self.cars[i].getFitness())
        exit()

    def isDead(self):
        lifeStatus = [car.dead for car in self.cars]
        return all(lifeStatus)

    def firstGeneration(CarConstructor, numCars, showEye=True):
        return Generation(CarConstructor, numCars, showEyes=showEye)

    def sortByFitness(self):
        self.cars.sort(key=lambda car: car.getFitness(), reverse=True)
        

