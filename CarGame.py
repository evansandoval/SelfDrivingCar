# Main Driver for Simulation

import pyglet, math, numpy as np
import Tracks
from pyglet import shapes
from pyglet.window import key
from Generations import Generation

# SIMULATION CONTROLS
NUM_CARS = 20
NUM_INJECTED_BRAINS = 20
FRICTION_CONSTANT = .015
TESTED_TRACKS = [3]
CYCLE_TRACKS = False
DRIVE_MANUALLY = False
PIXEL_DEBUGGING_MODE = False

# GRAPHICS CONTROLS
SHOW_EYES = False
SHOW_GATES = True

# STOP CONDITION CONTROLS
TIMEOUT = 80
ZERO_GATE_TIMEOUT = 8

## PYGLET WINDOW SETUP
WINDOW_X, WINDOW_Y = 1080, 920 # track images should be 1080x920
window = pyglet.window.Window(WINDOW_X, WINDOW_Y)


# PYGLET IMAGE SETUP
pyglet.resource.path = ['images']
pyglet.resource.reindex()
carFile = pyglet.resource.image("car.png")
carFile.anchor_x, carFile.anchor_y  = carFile.width // 2, carFile.height // 2 
lineFile = pyglet.resource.image("line.png")
lineFile.anchor_x, lineFile.anchor_y  = 0 , lineFile.height // 2

# PYGLET OBJECTS
class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.velocity_x, self.velocity_y = 0.0, 0.0
    
    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
# Batch for rendering eyes
eyeBatch = pyglet.graphics.Batch()

# TRACK OBJECT SETUP
TRACK_OBJECTS = {}
for trackNumber in TESTED_TRACKS:
    TRACK_OBJECTS[trackNumber] = Tracks.createTrackObj(trackNumber, SHOW_GATES)
currTrack = TRACK_OBJECTS[TESTED_TRACKS[0]]
def incrementTrack(currGen):
    if not CYCLE_TRACKS:
        return
    global currTrack
    currTrack = TRACK_OBJECTS[1 + currGen % len(TESTED_TRACKS)]

# CAR CLASS
class Car(PhysicalObject):
    class Eye(PhysicalObject):
        def __init__(self, length, angle, car, *args, **kwargs):
            super().__init__(img=lineFile, *args, **kwargs)
            self.length = length
            self.angle = angle
            self.rotation = car.rotation + angle
            self.x = car.x
            self.y = car.y
            self.line = shapes.Line(self.x, self.y, self.targetXY()[0][0], self.targetXY()[0][1], width=2, batch=eyeBatch)
        
        # Returns whether this eye detects wall (1) or track (0)
        def read(self):
            for x, y in self.targetXY():
                if (0 <= x < 1080 and 0 <= y < 920 and currTrack.BOUNDS[x][y]):
                    return 1
            return 0

        # Moves graphic of line associated with eye
        def updateLine(self):
            self.line.x = self.x
            self.line.y = self.y
            self.line.x2 = self.targetXY()[0][0]
            self.line.y2 = self.targetXY()[0][1]

        # Calculates coordinate of this eye's target location using car's rotation
        def targetXY(self):
            angle_radians = math.radians(self.rotation + 90)
            testPoints = []
            # test end of eye
            x = round(self.x + self.length * math.sin(angle_radians))
            y = round(self.y + self.length * math.cos(angle_radians))
            testPoints.append((x,y))
            # test midway through eye (to avoid seeing through walls)
            x = round(self.x + self.length / 2 * math.sin(angle_radians))
            y = round(self.y + self.length / 2 * math.cos(angle_radians))
            testPoints.append((x,y))
            return testPoints
        
    def __init__(self, setSpeed, setRotateSpeed, eyeParams, brain, *args, **kwargs):
        super().__init__(img=carFile, *args, **kwargs)
        self.speed = setSpeed
        self.rotate_speed = setRotateSpeed
        self.dead = False
        self.timeAlive = 0
        self.rotation = -90
        self.initEyes(eyeParams)
        self.carParams = np.array([setSpeed, setRotateSpeed])
        self.eyeParams = eyeParams
        self.control = dict(left=False, right=False, up=False, down=False)
        self.gatesVisited = set()
        self.savedGateTimes = []
        self.control = {'up': 0, 'left': 0, 'down': 0, 'right': 0, 'endsim': 0}
        self.brain = brain

    def initEyes(self, eyeParams):
        self.eyes = []
        for eye in eyeParams:
            self.eyes.append(self.Eye(eye[0], eye[1], self))
    
    # Set control map based on arrow keys
    def on_key_press(self, symbol, modifiers):
        if DRIVE_MANUALLY:
            if symbol == key.UP:
                self.control['up'] = 1
            elif symbol == key.LEFT:
                self.control['left'] = 1
            elif symbol == key.RIGHT:
                self.control['right'] = 1
            elif symbol == key.DOWN:
                self.control['down'] = 1
    
    # Set control map based on arrow keys
    def on_key_release(self, symbol, modifiers):
        if DRIVE_MANUALLY:
            if symbol == key.UP:
                self.control['up'] = 0
            elif symbol == key.LEFT:
                self.control['left'] = 0
            elif symbol == key.RIGHT:
                self.control['right'] = 0
            elif symbol == key.DOWN:
                self.control['down'] = 0

    # Calculate the speed of the car using its velocity components
    def magnitudeVelocity(self):
        return np.linalg.norm(np.array([self.velocity_x, self.velocity_y])) 

    # Reduce speed of car to model friction
    def friction(self):
        xLosses = self.velocity_x * FRICTION_CONSTANT
        yLosses = self.velocity_y * FRICTION_CONSTANT
        if self.control['up']: # reduce effect of friction if driving
            xLosses *= .75
            yLosses *= .75
        self.velocity_x -= xLosses
        self.velocity_y -= yLosses
        # Car reaches stop if slow enough and no commands are present
        if all([not v for v in self.control.values()]) and self.magnitudeVelocity() < 45:
            self.velocity_x = 0
            self.velocity_y = 0
    
    # Marks car as dead and erases from screen
    def kill(self):
        self.dead = True
        self.visible = False
        if SHOW_EYES:
            for eye in self.eyes:
                eye.line.visible = False
        
    # Kill car if out of bounds
    def checkBounds(self):
        if not (0 < self.x < 1080) or not (0 < self.y < 920) or currTrack.BOUNDS[int(self.x)][int(self.y)]:
            self.kill()

    # Match eye location with car location
    def moveEyes(self):
        for eye in self.eyes:
            eye.x = self.x
            eye.y = self.y
            eye.updateLine()

    # Match eye rotation with car rotation
    def rotateEyes(self, theta):
        for eye in self.eyes:
            eye.rotation += theta
            eye.updateLine()
    
    # direction = -1 if left, 1 if right
    def turn(self, dt, direction):
        def rotateByTheta(vx, vy, theta):
            x = np.array([vx,vy])
            R = np.array([[math.cos(theta), -math.sin(theta)], 
                          [math.sin(theta), math.cos(theta)]])
            return np.matmul(R, x)
        theta_0 = -math.radians(self.rotation)
        self.rotation += direction * self.rotate_speed * dt
        self.rotateEyes(direction * self.rotate_speed * dt)
        theta_f = -math.radians(self.rotation)
        dTheta = theta_f-theta_0
        newRotatedVector = rotateByTheta(self.velocity_x, self.velocity_y, dTheta)
        self.velocity_x, self.velocity_y = newRotatedVector[0], newRotatedVector[1]

    # direction = 1 if forward, -1 if backward 
    def drive(self, dt, direction):
        angle_radians = -math.radians(self.rotation)
        accel_x = math.cos(angle_radians) * self.speed * dt
        accel_y = math.sin(angle_radians) * self.speed * dt
        self.velocity_x += direction * accel_x
        self.velocity_y += direction * accel_y
        
    # Return vector containing eye outputs
    def readEyes(self):
        vector = []
        for eye in self.eyes:
            vector.append(eye.read())
        return vector
    
    # Detect if Car has passed a gate and prevent duplicate gate counting
    def checkGates(self):
        x, y = int(self.x), int(self.y)
        if currTrack.GATE_TRACKER.isGate(x, y):
            if len(self.gatesVisited) < 20:
                for gate in self.gatesVisited:
                    if currTrack.GATE_TRACKER.isSameGate(gate[0], gate[1], x, y):
                        return
                self.gatesVisited.add((x,y))
                if len(self.savedGateTimes) == 0:
                    self.savedGateTimes.append(self.timeAlive)  
                else:
                    currentGateTime = self.timeAlive - self.savedGateTimes[-1] 
                    self.savedGateTimes.append(currentGateTime)
            # If lap completed, reset visited gates
            if len(self.gatesVisited) == 20:
                self.gatesVisited = set()

    # Fitness is independent of time before completing a lap
    # This prevents cars speeding into walls with low fitness
    def getFitness(self):
        numGates = len(self.savedGateTimes)
        # Phase I Fitness Function, dependent on numGates
        if numGates < 20: 
            return numGates
        # Phase II Fitness Function, dependent on numGates & time
        else:
            averageGateTime = sum(self.savedGateTimes) / numGates
            return numGates**3 / averageGateTime # averageGateTime is currently equal to zero

    # End generation based on simulation controls
    def checkStopConditions(self):
        # Car has not moved sufficient distance
        if len(self.savedGateTimes) == 0 and self.timeAlive > ZERO_GATE_TIMEOUT:
            self.kill()
        
        # Car is going backwards
        if len(self.savedGateTimes) == 1: 
            x1, y1 = list(self.gatesVisited)[0]
            if currTrack.GATE_TRACKER.isSameGate(x1, y1, currTrack.BACKWARD_GATE_X, currTrack.BACKWARD_GATE_Y):
                self.kill()
                self.getFitness = lambda : 0

        # Time limit reached
        if self.timeAlive > TIMEOUT:
            
            self.kill()

    # Move car based on controls determined by Brain or arrow keys
    def moveCar(self, dt):
        if self.control['left'] and not self.control['right']:
            self.turn(dt, -1)
        if self.control['right'] and not self.control['left']:
            self.turn(dt, 1)
        if self.control['up'] and not self.control['down']:
            self.drive(dt, 1)
        if self.control['down'] and not self.control['up']:
            self.drive(dt, -1)

    # Use car's neural network to determine how to drive
    def processBrain(self):
        if DRIVE_MANUALLY:
            return
        inputVector = self.readEyes()
        outputVector = self.brain.processNeuralNet(inputVector)
        self.control['left'] = outputVector[0]
        self.control['up'] = outputVector[1]
        self.control['right'] = outputVector[2]
        self.control['down'] = outputVector[3]

    # Pixel Debugging Function (Useful when creating new tracks)
    def on_mouse_press(self, x, y, button, modifiers):
        if not PIXEL_DEBUGGING_MODE:
            return
        print("===============")
        print(f"Coords: {(x,y)}")
        print(f"Out of Bounds: {bool(currTrack.BOUNDS[x][y])}")
        print(f"Is gate: {currTrack.GATE_TRACKER.isGate(x, y)}")
        print(f"Is start gate: {currTrack.GATE_TRACKER.isSameGate(x, y, currTrack.BACKWARD_GATE_X, currTrack.BACKWARD_GATE_Y)}")

    # Pyglet Object's update function
    def update(self, dt):
        if self.dead:
            return
        super(Car, self).update(dt)
        self.timeAlive += dt
        self.checkBounds()
        self.moveEyes()
        self.checkGates()
        self.processBrain()
        self.friction()
        self.moveCar(dt)
        self.checkStopConditions()

gen = Generation(Car, NUM_CARS, currTrack, NUM_INJECTED_BRAINS)

# Pyglet Setup
def update(dt):
    for obj in gen.cars:
        obj.update(dt)
for obj in gen.cars:
    window.push_handlers(obj)


@window.event
def on_draw():
    window.clear()
    currTrack.trackImage.draw()

    # Draw all cars and eyes
    for obj in gen.cars:
        obj.draw()
    if SHOW_EYES:
        eyeBatch.draw()

    # At end of generation, cycle track and generate new cars
    if gen.isDead():
        incrementTrack(gen.number)
        gen.geneticAlgorthm(currTrack)

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()