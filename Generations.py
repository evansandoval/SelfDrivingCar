# Genetic Algorithm Functionality

import numpy as np
import os
from Brain import Brain

# Genetic Algorithm Controls
CROSSOVER_RATE = .2 # Percent chance of genetic crossover
MUTATION_STD_DEV = .12 # Std Dev of random number added during genetic mutation
NUM_HIDDEN_LAYERS = 8

# Default Parameters
# Note: These are currently constant but can also be used as parameters for optimization
DEFAULT_SPEED = 80.0
DEFAULT_TURN_RADIUS = 100.0
DEFAULT_EYE_PARAMS = [(100,-45), (100, 45)]
DEFAULT_CAR_PARAMS = np.array([DEFAULT_SPEED, DEFAULT_TURN_RADIUS])
INJECTED_BRAIN_LAYERS = [np.loadtxt("InjectedBrain/layer-0.csv"), np.loadtxt("InjectedBrain/layer-1.csv"),
                         np.loadtxt("InjectedBrain/layer-2.csv")]

class Generation:
    def __init__(self, CarConstructor, numCars, currTrack, numInjectedBrains, carParams=DEFAULT_CAR_PARAMS, eyeParams=DEFAULT_EYE_PARAMS):
        self.number = 0
        self.numCars = numCars
        self.Car = CarConstructor
        self.cars = []
        brainParams = self.initBrains(len(eyeParams), numInjectedBrains)
        self.populateGeneration(carParams, eyeParams, brainParams, currTrack)

    # Constructs and stores car objects for each generation
    def populateGeneration(self, carParams, eyeParams, brainParams, currTrack):
        self.number += 1
        self.cars = []
        startX, startY = currTrack.DEFAULT_START_X, currTrack.DEFAULT_START_Y
        for i in range(self.numCars):
            speed = carParams[0]
            turnRadius = carParams[1]
            brain = Brain(brainParams[i])     
            self.cars.append(self.Car(speed, turnRadius, eyeParams, brain, x=startX, y=startY, batch=None))
    
    # Analyzes fitness scores and creates next generation
    def geneticAlgorthm(self, currTrack):
        self.sortByFitness()
        self.printTopTen()
        self.saveBrain(self.cars[0])
        top20 = self.cars[0:self.numCars//5]
        newParams = DEFAULT_CAR_PARAMS
        newEyes   = DEFAULT_EYE_PARAMS
        newBrains = self.generateNewBrains(top20)
        self.populateGeneration(newParams, newEyes, newBrains, currTrack)

    # Brain needs at least three matrices in order to compute
    # NUM_HIDDEN_LAYERS x numEyes || NUM_HIDDEN_LAYERS x NUM_HIDDEN_LAYERS || 4 x NUM_HIDDEN_LAYERS
    def initBrains(self, numInputs, numInjectedBrains):
        listOfBrainLayers = []
        for i in range(self.numCars):
            if i < numInjectedBrains:
                brainLayers = INJECTED_BRAIN_LAYERS
            else:
                # initialize random matrices using a UNIFORM distribution
                inputMatrix = np.random.uniform(-1, 1, (NUM_HIDDEN_LAYERS, numInputs))
                hiddenMatrix = np.random.uniform(-1, 1, (NUM_HIDDEN_LAYERS, NUM_HIDDEN_LAYERS))
                outputMatrix = np.random.uniform(-1, 1, (4, NUM_HIDDEN_LAYERS))
                brainLayers = [inputMatrix, hiddenMatrix, outputMatrix]
            listOfBrainLayers.append(brainLayers)
        return listOfBrainLayers
    
    # Takes top brains and generates new brains for children
    def generateNewBrains(self, top20):
        numberOfLayers = len(top20[0].brain.layers)
        unzippedLayers = [] # unzippedLayers[i] holds every brain's ith layer

        # Generate new brains and reorganize them by layer
        for layerIndex in range(numberOfLayers):
            parentLayers = []
            for car in top20:
                parentLayers.append(car.brain.layers[layerIndex])
            childLayers = self.generateChildren(parentLayers)
            unzippedLayers.append(childLayers)

        # Reconstruct unzipped brain layers
        brainList = []
        numCars = len(unzippedLayers[0])
        for carIndex in range(numCars):
            thisBrain = []
            for layerIndex in range(numberOfLayers):
                thisBrain.append(unzippedLayers[layerIndex][carIndex])
            brainList.append(thisBrain)

        return brainList

    # Creates 4 new children from each parent using genetic crossover and mutation 
    def generateChildren(self, lst):
        for i in range(len(lst)):
            child = self.crossOver(lst[i], lst[i+1]) # replace this with a genetic crossover function instead
            
            for _ in range(4): # need four more children
                shape = np.shape(child)
                mutatedChild = child + np.random.normal(0, MUTATION_STD_DEV, size=shape)
                lst.append(mutatedChild)
        return lst
    
    # Performs genetic crossover based on constant CROSSOVER_RATE
    def crossOver(self, parent1, parent2):
        child = []
        # Favors parent with higher fitness
        for i in range(len(parent1)):
            sample = np.random.uniform()
            if sample > CROSSOVER_RATE:
                child.append(parent1[i])
            else: child.append(parent2[i])
        return np.array(child)

    # Denotes end of a generation
    def isDead(self):
        lifeStatus = [car.dead for car in self.cars]
        return all(lifeStatus)

    def sortByFitness(self):
        self.cars.sort(key=lambda car: car.getFitness(), reverse=True)
        
    def printTopTen(self):
        print(f"Generation {self.number}'s top 10 fitness scores:")
        for i in range(10):
            print(f"{i}. {self.cars[i].getFitness()}")

    def saveBrain(self, car):
        if not os.path.exists(f"Saved-Brains/F{car.getFitness() // 1}-G{self.number}/"):
            os.makedirs(f"Saved-Brains/F{int(car.getFitness())}-G{self.number}/")
        for i in range(len(car.brain.layers)):
            np.savetxt(f"Saved-Brains/F{int(car.getFitness())}-G{self.number}/layer-{i}.csv", car.brain.layers[i])


