import numpy as np
import random

# DEFAULT PARAMETERS
defaultStartX = 150
defaultStartY = 415
defaultSpeed = 100
defaultTurnRadius = 100
defaultEyes = 3 # maybe even make this an input
defaultEyeDistance = 20 #number of pixels 

defaultParams = np.array([defaultSpeed, defaultTurnRadius, defaultEyes, defaultEyeDistance])

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
    def __init__(self, CarConstructor, numCars, params=defaultParams):
        self.cars = []
        for _ in range(numCars):
            speed = params[0] + random.randint(-10, 10)
            turnRadius = params[1] + random.randint(-10,10)
            numEyes = params[2]
            eyeDist = params[3]
            self.cars.append(CarConstructor(speed, turnRadius, x=150, y=415, batch=None))

    def sortByFitness(self):
        self.cars.sort(lambda car: car.getFitness(), reverse=True)
        
