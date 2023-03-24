import numpy as np
import random

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
            speed = params[0] + random.randint(-10, 10)
            turnRadius = params[1] + random.randint(-10,10)
            eyeDist = params[2]
            eyeAngles = params[3]
            self.cars.append(CarConstructor(speed, turnRadius, eyeDist, eyeAngles, x=defaultStartX, y=defaultStartY, batch=None))

    def firstGeneration(CarConstructor, numCars, showEye=True):
        return Generation(CarConstructor, numCars, showEyes=showEye)

    def sortByFitness(self):
        self.cars.sort(lambda car: car.getFitness(), reverse=True)
        

