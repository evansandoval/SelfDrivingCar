import pyglet
from pyglet.window import key
import math
import numpy as np
from PIL import Image
from numpy import savetxt

windowX, windowY = 1080, 920 # track images should be 1080x920
window = pyglet.window.Window(windowX, windowY)

pyglet.resource.path = ['images']
pyglet.resource.reindex()

trackFile= pyglet.resource.image("track1.png")
trackImage = pyglet.sprite.Sprite(img=trackFile)
trackIm = Image.open('./images/track1.png') # Can be many different formats.
pixels = trackIm.load()
boundsMatrix = np.ones((1080, 920))
for i in range(1080):
    for j in range(920):
        if(pixels[i,j] == 0):
            boundsMatrix[i][919-j] = 0 ## 0 for when it's in bounds
                                       ## 1 for when it's out of bounds

carFile = pyglet.resource.image("car.png")
carX, carY = 150, 415
# car = pyglet.sprite.Sprite(img=carFile, x=carX, y=carY)

def center_image(image):
    """Sets an image's anchor point to its center"""
    image.anchor_x = image.width // 2
    image.anchor_y = image.height // 2

center_image(carFile)

class PhysicalObject(pyglet.sprite.Sprite):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.velocity_x, self.velocity_y = 0.0, 0.0

    def check_bounds(self):
        min_x = -self.image.width / 2
        min_y = -self.image.height / 2
        max_x = windowX + self.image.width / 2
        max_y = windowY + self.image.height / 2
        # if self.x < min_x:
        #     print("Out of Bounds")
        # elif self.x > max_x:
        #     print("Out of Bounds")
        # if self.y < min_y:
        #     print("Out of Bounds")
        # elif self.y > max_y:
        #     print("Out of Bounds")
    
    def update(self, dt):
        self.x += self.velocity_x * dt
        self.y += self.velocity_y * dt
        self.check_bounds()

def update(dt):
    for obj in game_objects:
        obj.update(dt)


def rotateByTheta(vx, vy, theta):
    x = np.array([vx,vy])
    R = np.array([[math.cos(theta), -math.sin(theta)], 
                  [math.sin(theta), math.cos(theta)]])
    return np.matmul(R, x)


class Player(PhysicalObject):
    def __init__(self, setSpeed, setRotateSpeed, *args, **kwargs):
        self.speed = setSpeed
        self.rotate_speed = setRotateSpeed
        self.mu = .999 # FRICTION CONSTANT
        super().__init__(img=carFile, *args, **kwargs)
        self.rotation = -90
        self.keys = dict(left=False, right=False, up=False, down=False)
    
    def on_key_press(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = True
        elif symbol == key.LEFT:
            self.keys['left'] = True
        elif symbol == key.RIGHT:
            self.keys['right'] = True
        elif symbol == key.DOWN:
            self.keys['down'] = True

    def on_key_release(self, symbol, modifiers):
        if symbol == key.UP:
            self.keys['up'] = False
        elif symbol == key.LEFT:
            self.keys['left'] = False
        elif symbol == key.RIGHT:
            self.keys['right'] = False
        elif symbol == key.DOWN:
            self.keys['down'] = False
    def magnitudeVelocity(self):
        return np.linalg.norm(np.array([self.velocity_x, self.velocity_y])) 
    def friction(self):
        self.velocity_x *= self.mu
        self.velocity_y *= self.mu
        if all([not v for v in self.keys.values()]) and self.magnitudeVelocity() < 45:
            self.velocity_x = 0
            self.velocity_y = 0
    def kill(self):
        self.rotation = -90
        self.velocity_x, self.velocity_y = 0, 0
        self.x, self.y = carX, carY
    def update(self, dt):
        super(Player, self).update(dt)
        self.friction()
        if not (0 < self.x < 1080) or not (0 < self.y < 920) or not boundsMatrix[int(self.x)][int(self.y)]:
            self.kill()
        if self.keys['left']:
            theta0 = -math.radians(self.rotation)
            self.rotation -= self.rotate_speed * dt
            thetaf = -math.radians(self.rotation)
            dtheta = thetaf-theta0
            newRotatedVector = rotateByTheta(self.velocity_x, self.velocity_y, dtheta)
            self.velocity_x, self.velocity_y = newRotatedVector[0], newRotatedVector[1]
        if self.keys['right']:
            theta0 = -math.radians(self.rotation)
            self.rotation += self.rotate_speed * dt
            thetaf = -math.radians(self.rotation)
            dtheta = thetaf-theta0
            newRotatedVector = rotateByTheta(self.velocity_x, self.velocity_y, dtheta)
            self.velocity_x, self.velocity_y = newRotatedVector[0], newRotatedVector[1]
        if self.keys['up']:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.speed * dt
            force_y = math.sin(angle_radians) * self.speed * dt
            self.velocity_x += force_x
            self.velocity_y += force_y
        if self.keys['down']:
            angle_radians = -math.radians(self.rotation)
            force_x = math.cos(angle_radians) * self.speed * dt
            force_y = math.sin(angle_radians) * self.speed * dt
            self.velocity_x -= force_x
            self.velocity_y -= force_y

car = Player(300.0, 200.0, x=carX, y=carY, batch=None)
game_objects = [car] # add more car objects to run simultaneously later
window.push_handlers(car)
@window.event
def on_draw():
    window.clear()

    trackImage.draw()
    car.draw()

if __name__ == '__main__':
    pyglet.clock.schedule_interval(update, 1/120.0)
    pyglet.app.run()