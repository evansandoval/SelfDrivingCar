import pyglet, math, Gates, numpy as np
from pyglet import shapes
from pyglet.window import key
from PIL import Image
from Generations import Generation

## Useful function
def rotateByTheta(vx, vy, theta):
    x = np.array([vx,vy])
    R = np.array([[math.cos(theta), -math.sin(theta)], 
                  [math.sin(theta), math.cos(theta)]])
    return np.matmul(R, x)

## TRACK IMAGE PROCESSING
trackIm = Image.open('./images/track1.png') 
pixels = trackIm.load()
boundsMatrix = np.zeros((1080, 920))
for x in range(1080):
    for y in range(920):
        if(pixels[x,y] == 0):
            boundsMatrix[x][919-y] = 1 ## 1 for when it's in bounds
                                       ## 0 for when it's out of bounds


## GATE IMAGE PROCESSING
gateIm = Image.open("./images/track1gates.png")
pixels = gateIm.load()
gatesMatrix = np.zeros((1080,920))
for x in range(1080):
    for y in range(920):      
        if pixels[x,y] == 1:
            gatesMatrix[x][919-y] = 1 # 1 for when it represents a Gate
                                      # 0 otherwise
gateObj = Gates.GatesTracker(gatesMatrix)

## PYGLET WINDOW SETUP
windowX, windowY = 1080, 920 # track images should be 1080x920
window = pyglet.window.Window(windowX, windowY)

# PYGLET IMAGE SETUP
pyglet.resource.path = ['images']
pyglet.resource.reindex()

carFile = pyglet.resource.image("car.png")
carFile.anchor_x, carFile.anchor_y  = carFile.width // 2, carFile.height // 2 
lineFile = pyglet.resource.image("line.png")
lineFile.anchor_x, lineFile.anchor_y  = 0 , lineFile.height // 2
trackFile= pyglet.resource.image("track1.png")
trackImage = pyglet.sprite.Sprite(img=trackFile)

# PYGLET OBJECTS
class PhysicalObject(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0
    
    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
eyeBatch = pyglet.graphics.Batch()

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
            self.line = shapes.Line(self.x, self.y, self.targetXY()[0], self.targetXY()[1], width=2, batch=eyeBatch)
        def read(self):
            x, y = self.targetXY()
            if 0 < x < 1080 and 0 < y < 920 and boundsMatrix[x][y]:
                return 1
            return 0

        def updateLine(self):
            self.line.x = self.x
            self.line.y = self.y
            self.line.x2 = self.targetXY()[0]
            self.line.y2 = self.targetXY()[1]

        def targetXY(self):
            angle_radians = math.radians(self.rotation + 90)
            return round(self.x + self.length * math.sin(angle_radians)), round(self.y + self.length * math.cos(angle_radians))
        
    def __init__(self, setSpeed, setRotateSpeed, eyeParams, brain, *args, **kwargs):
        super().__init__(img=carFile, *args, **kwargs)
        self.speed = setSpeed
        self.rotate_speed = setRotateSpeed
        self.dead = False
        self.timeAlive = 0
        self.mu = .999 # FRICTION CONSTANT
        self.rotation = -90
        self.startX, self.startY = self.x, self.y
        self.makeEyes(eyeParams)
        self.params = [setSpeed, setRotateSpeed]
        self.eyeParams = eyeParams
        self.control = dict(left=False, right=False, up=False, down=False)
        self.gatesVisited = {}
        self.control = {'up': 0, 'left': 0, 'down': 0, 'right': 0}
        self.brain = brain

    def makeEyes(self, eyeParams):
        self.eyes = []
        for eye in eyeParams:
            self.eyes.append(self.Eye(eye[0], eye[1], self))
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.control['up'] = 1
        elif symbol == key.LEFT:
            self.control['left'] = 1
        elif symbol == key.RIGHT:
            self.control['right'] = 1
        elif symbol == key.DOWN:
            self.control['down'] = 1
    
    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.control['up'] = 0
        elif symbol == key.LEFT:
            self.control['left'] = 0
        elif symbol == key.RIGHT:
            self.control['right'] = 0
        elif symbol == key.DOWN:
            self.control['down'] = 0

    def magnitudeVelocity(self):
        return np.linalg.norm(np.array([self.velocity_x, self.velocity_y])) 
    
    def checkGates(self):
        x, y = int(self.x), int(self.y)
        if gateObj.isGate(x, y):
            for gate in self.gatesVisited:
                if gateObj.sameGateAs(gate[0], gate[1], x, y):
                    return
            if len(self.gatesVisited) == 0:
                self.gatesVisited[(x,y)] = self.timeAlive
                self.lastGate = (x,y)  
            else:
                self.gatesVisited[(x,y)] = self.timeAlive - self.gatesVisited[self.lastGate]

    def friction(self):
        self.velocity_x *= self.mu
        self.velocity_y *= self.mu
        if all([not v for v in self.control.values()]) and self.magnitudeVelocity() < 45:
            self.velocity_x = 0
            self.velocity_y = 0
    
    def kill(self):
        self.dead = True
        # print("Speed  :", self.speed)
        # print("Fitness:", round(self.getFitness(), 5))
        # print("Died at:", round(self.timeAlive, 5))
        # print("# Gates:", len(self.gatesVisited))
        # print("==============================")
        # self.rotation = -90
        # self.velocity_x, self.velocity_y = 0, 0
        # self.x, self.y = self.startX, self.startY
        # self.rotateEyes(0, True)
        # self.gatesVisited = {}
        # self.timeAlive = 0
    
    def checkBounds(self):
        if not (0 < self.x < 1080) or not (0 < self.y < 920) or boundsMatrix[int(self.x)][int(self.y)]:
            self.kill()

    def moveEyes(self):
        for eye in self.eyes:
            eye.x = self.x
            eye.y = self.y
            eye.updateLine()

    def rotateEyes(self, theta, kill=False):
        if kill:
            for eye in self.eyes:
                eye.rotation = self.rotation + eye.angle
                eye.updateLine()
        else: 
            for eye in self.eyes:
                eye.rotation += theta
                eye.updateLine()

    def turnLeft(self, dt):
        theta0 = -math.radians(self.rotation)
        self.rotation -= self.rotate_speed * dt
        self.rotateEyes(-self.rotate_speed * dt)
        thetaf = -math.radians(self.rotation)
        dtheta = thetaf-theta0
        newRotatedVector = rotateByTheta(self.velocity_x, self.velocity_y, dtheta)
        self.velocity_x, self.velocity_y = newRotatedVector[0], newRotatedVector[1]

    def turnRight(self, dt):  
        theta0 = -math.radians(self.rotation)
        self.rotation += self.rotate_speed * dt
        self.rotateEyes(self.rotate_speed * dt)
        thetaf = -math.radians(self.rotation)
        dtheta = thetaf-theta0
        newRotatedVector = rotateByTheta(self.velocity_x, self.velocity_y, dtheta)
        self.velocity_x, self.velocity_y = newRotatedVector[0], newRotatedVector[1]

    def forward(self, dt):
        angle_radians = -math.radians(self.rotation)
        force_x = math.cos(angle_radians) * self.speed * dt
        force_y = math.sin(angle_radians) * self.speed * dt
        self.velocity_x += force_x
        self.velocity_y += force_y
    
    def backward(self, dt):
        angle_radians = -math.radians(self.rotation)
        force_x = math.cos(angle_radians) * self.speed * dt
        force_y = math.sin(angle_radians) * self.speed * dt
        self.velocity_x -= force_x
        self.velocity_y -= force_y
        
    def readEyes(self):
        vector = []
        for eye in self.eyes:
            vector.append(eye.read())
        return vector

    def getFitness(self):
        if len(self.gatesVisited) == 0:
            return 0
        numGates = len(self.gatesVisited)
        averageGateTime = sum(self.gatesVisited.values()) / numGates
        return numGates**3 / averageGateTime

    def checkStopConditions(self):
        if len(self.gatesVisited) == 0 and self.timeAlive > 7:
            # print("Car has not moved sufficient distance")
            self.kill()
        if len(self.gatesVisited) == 20:
            # print("Car has completed the course")
            self.kill()

    def moveCar(self, dt):
        if self.control['left']:
            self.turnLeft(dt)
        if self.control['right']:
            self.turnRight(dt)
        if self.control['up']:
            self.forward(dt)
        if self.control['down']:
            self.backward(dt)

    def processBrain(self):
        inputVector = self.readEyes()
        outputVector = self.brain.process(inputVector)
        self.control['left'] = outputVector[0]
        self.control['up'] = outputVector[1]
        self.control['right'] = outputVector[2]
        self.control['down'] = outputVector[3]

    def update(self, dt):
        if self.dead:
            return
        super(Car, self).update(dt)
        self.timeAlive += dt
        self.friction()
        self.checkBounds()
        self.moveEyes()
        self.checkGates()
        self.checkStopConditions()
        self.processBrain()
        self.moveCar(dt)

# Universal update function by pyglet
def update(dt):
    for obj in cars:
        obj.update(dt)

gen = Generation(Car, 100, showEyes=True)
cars = gen.cars # Creates a generation of 5 cars
for obj in cars:
    window.push_handlers(obj)

@window.event
def on_draw():
    window.clear()

    trackImage.draw()
    for obj in cars:
        obj.draw()
    if gen.showEyes:
        eyeBatch.draw()
    
    if gen.isDead():
        gen.nextGeneration()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()