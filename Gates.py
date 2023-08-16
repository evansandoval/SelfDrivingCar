# Class for grouping gate pixels by proximity using UnionFind

import WeightedQuickUnion as WQU

class GatesTracker:
    def __init__(self, gatesMatrix):
        self.gatesMatrix = gatesMatrix
        self.wqu = WQU.WeightedQuickUnionWithPathCompressionUF(1080*920)
        for x in range(1080):
            for y in range(920):
                if self.isGate(x,y):
                   self.addAdjacent(x, y)
    
    # Use WQU to create groups of gate pixels
    def addAdjacent(self, x, y):
        if x < 0 or y<0 or x>=1080 or y>=920:
            return
        # check spot above
        if (x > 0 and self.isGate(x, y+1)):
            self.wqu.union(y * 1080 + x, (y + 1) * 1080 + x)
            
        # check spot left
        if (y > 0 and self.isGate(x-1, y)):
            self.wqu.union(y * 1080 + x, (y) * 1080 + x-1)
            
        # check spot below
        if (x < 1080 and self.isGate(x, y-1)):
            self.wqu.union(y * 1080 + x, (y-1) * 1080 + x)
        
        # check spot right
        if (y < 920 and self.isGate(x+1, y)):
            self.wqu.union(y * 1080 + x, (y) * 1080 + x + 1)

    # Return whether a coordinate point is a Gate
    def isGate(self, x,y):
        x, y = int(x), int(y)
        return bool(0 < x < 1080 and 0 < y < 920 and self.gatesMatrix[x][y])
    
    # Return number of gates
    def count(self):
        return self.wqu.count
    
    # Use WQU data structure to detect if two coordinate points are part of the same Gate
    def isSameGate(self, x1, y1, x2, y2):       
        point1 = int(x1 + y1*1080)
        point2 = int(x2 + y2*1080)
        return self.wqu.connected(point1, point2)