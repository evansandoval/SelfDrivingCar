import numpy as np
from Brain import Brain

# DEFAULT PARAMETERS
# 
DEFAULT_START_X = 123
DEFAULT_START_Y = 300
DEFAULT_SPEED = 60.0
DEFAULT_TURN_RADIUS = 100.0
# DEFAULT_EYES = 3 # maybe even make this an input
DEFAULT_EYE_PARAMS = [(100,-45), (100, 45)]

DEFAULT_CAR_PARAMS = np.array([DEFAULT_SPEED, DEFAULT_TURN_RADIUS])
TOP_BRAIN_LAYERS = [np.loadtxt("BestBrain/layer-0.csv"), np.loadtxt("BestBrain/layer-1.csv"), np.loadtxt("BestBrain/layer-2.csv")]

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
    def __init__(self, CarConstructor, numCars, carParams=DEFAULT_CAR_PARAMS, eyeParams=DEFAULT_EYE_PARAMS, showEyes=True):
        self.number = 1
        self.showEyes = showEyes
        self.numCars = numCars
        self.Car = CarConstructor
        self.cars = []
        for i in range(numCars):
            speed = carParams[0]
            turnRadius = carParams[1]
            if i < 20: #inject 20 ideal cars
                brain = Brain(TOP_BRAIN_LAYERS)
            else:
                brain = Brain(self.initBrainMatrices(len(eyeParams)))   
            self.cars.append(self.Car(speed, turnRadius, eyeParams, brain, x=DEFAULT_START_X, y=DEFAULT_START_Y, batch=None))




    def populateGeneration(self, carParams, eyeParams, brainParams=None):
        self.number += 1
        self.cars = []
        for i in range(self.numCars):
            speed = carParams[0]
            turnRadius = carParams[1]
            brain = Brain(brainParams[i])     
            self.cars.append(self.Car(speed, turnRadius, eyeParams, brain, x=DEFAULT_START_X, y=DEFAULT_START_Y, batch=None))


        
    def initBrainMatrices(self, numInputs):
        # Brain needs at least three matrices in order to compute
        #     8 x numEyes || 8 x 8 || 4 x 8
        # to add more hidden layers, simply add more 8x8 matrices in the middle

        # initialize random matrices using a UNIFORM distribution
        inputMatrix = np.random.uniform(-1, 1, (8, numInputs))
        hiddenMatrix = np.random.uniform(-1, 1, (8, 8))
        outputMatrix = np.random.uniform(-1, 1, (4, 8))
        return [inputMatrix, hiddenMatrix, outputMatrix]
    
    def createNextGeneration(self):
        self.sortByFitness()
        print(f"Generation {self.number}'s top 10 fitness scores:")
        for i in range(10):
            print(i, self.cars[i].getFitness())
        self.saveBrain(self.cars[0], "")
        top20 = self.cars[0:self.numCars//5]
        newParams = self.mixMutate([car.carParams       for car in top20])
        newEyes   = self.newEyes  ([car.eyeParams    for car in top20])
        # eyes need their own mix function to randomly mutate new eyes
        newBrains = self.newBrain(top20)
        self.populateGeneration(DEFAULT_CAR_PARAMS, DEFAULT_EYE_PARAMS, newBrains)
        
    def saveBrain(self, car, titleString):
        for i in range(len(car.brain.layers)):
            np.savetxt("Saved-Brains/" + titleString + "layer-" + str(i) + ".csv", self.cars[0].brain.layers[i])

    
    def newBrain(self, top20):
        numberOfLayers = len(top20[0].brain.layers)
        #collects new generation of newly mutated weights matrices (organized in order)
        separateLayers = []
        for layerIndex in range(numberOfLayers):
            separateLayers.append(self.mixMutate([car.brain.layers[layerIndex] for car in top20]))
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
            child = self.crossOver(lst[i], lst[i+1]) # replace this with a genetic crossover function instead
            for _ in range(4): # need four more children
                shape = np.shape(child)
                mutatedChild = child + np.random.normal(0, .12, size=shape)
                lst.append(mutatedChild)
        return lst
    
    def crossOver(self, lst1, lst2):
        child = []
        # Favors parent with higher fitness
        for i in range(len(lst1)):
            sample = np.random.uniform()
            if sample < 0.8:
                child.append(lst1[i])
            else: child.append(lst2[i])
        return np.array(child)



    def isDead(self):
        lifeStatus = [car.dead for car in self.cars]
        return all(lifeStatus)

    def sortByFitness(self):
        self.cars.sort(key=lambda car: car.getFitness(), reverse=True)
        

