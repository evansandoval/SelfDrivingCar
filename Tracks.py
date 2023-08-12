import Gates, pyglet, numpy as np
from PIL import Image

# Struct for TrackObj
class TrackObject:
    def __init__(self):
        self.TRACK_NUMBER = None

        self.GATE_VARIABLE = None
        self.BACKWARD_GATE_X = None
        self.BACKWARD_GATE_Y = None
        self.DEFAULT_START_X = None
        self.DEFAULT_START_Y = None

        self.BOUNDS = None
        self.GATE_TRACKER = None
        self.trackImage = None
        return

def createTrackObj(trackNumber, showGates):
    trackObj = TrackObject()
    trackObj.TRACK_NUMBER = trackNumber
    match trackNumber:
        case 1:
            trackObj.GATE_VARIABLE = 1
            trackObj.BACKWARD_GATE_X = 147
            trackObj.BACKWARD_GATE_Y = 326
            trackObj.DEFAULT_START_X = 150
            trackObj.DEFAULT_START_Y = 415
        case 2:
            trackObj.GATE_VARIABLE = 2
            trackObj.BACKWARD_GATE_X = 824
            trackObj.BACKWARD_GATE_Y = 436
            trackObj.DEFAULT_START_X = 804
            trackObj.DEFAULT_START_Y = 458

    ## CREATE BOUNDS MATRIX
    trackIm = Image.open(f"./images/track{trackNumber}.png") 
    pixels = trackIm.load()
    boundsMatrix = np.zeros((1080, 920))
    for x in range(1080):
        for y in range(920):
            if(pixels[x,y] == 0):
                boundsMatrix[x][919-y] = 1 ## 1 for when it's in bounds
                                           ## 0 for when it's out of bounds
    trackObj.BOUNDS = boundsMatrix

    ## CREATE GATE OBJECT
    gateIm = Image.open(f"./images/track{trackNumber}gates.png")
    pixels = gateIm.load()
    gatesMatrix = np.zeros((1080,920))
    for x in range(1080):
        for y in range(920):      
            if pixels[x,y] == trackObj.GATE_VARIABLE:
                gatesMatrix[x][919-y] = 1 # 1 for when it represents a Gate
                                          # 0 otherwise
    trackObj.GATE_TRACKER = Gates.GatesTracker(gatesMatrix)

    if showGates:
        trackFile = pyglet.resource.image(f"track{trackNumber}gates.png")
    else:
        trackFile = pyglet.resource.image(f"track{trackNumber}.png")
    trackObj.trackImage = pyglet.sprite.Sprite(img=trackFile)

    return trackObj
