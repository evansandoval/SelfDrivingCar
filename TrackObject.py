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