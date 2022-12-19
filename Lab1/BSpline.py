from pyglet.gl import *
import numpy as np, readFile as f

class BSpline:
    vertices, polygons, segments, tangents, d2s, res = ([], [], [], [], [], 50)
    batch = pyglet.graphics.Batch()

    def __init__(self, filepath):
        f.readFile(self, filepath)
        self.cSpline()
        self.addToBatch()

    def calcTBRDiff(self, nthSegment, t):
        T = np.array([2 * t, 1])
        B = 1/2 * np.array([[-1, 3, -3, 1], [2, -4, 2, 0]])
        R = np.array([self.vertices[nthSegment - 1], self.vertices[nthSegment],
                      self.vertices[nthSegment + 1], self.vertices[nthSegment + 2]])
        return np.dot(np.dot(T, B), R)

    def calcSegmentT(self, nthSegment, t):
        T = np.array([pow(t, 3), pow(t, 2), t, 1])
        B = 1/6 * np.array([[-1, 3, -3, 1], [3, -6, 3, 0], [-3, 0, 3, 0], [1, 4, 1, 0]])
        R = np.array([self.vertices[nthSegment - 1], self.vertices[nthSegment],
                      self.vertices[nthSegment + 1], self.vertices[nthSegment + 2]]) 
               
        TBR = np.dot(np.dot(T, B), R)

        Tt = [pow(t, 2), t, 1]
        Bt = 1 / 2 * np.array([[-1, 3, -3, 1], [2, -4, 2, 0], [-1, 0, 1, 0]])
        TBRt = np.dot(np.dot(Tt, Bt), R)
        return TBR, TBRt

    def cSpline(self):
        for i in range(1, len(self.vertices) - 3 + 1):
            for t in np.linspace(0, 1, self.res):
                points, tangents = self.calcSegmentT(i, t)
                self.segments.append(points)
                self.tangents.append(tangents)
                self.d2s.append(self.calcTBRDiff(i, t))

    def tangent(self, segment, i):
        scale = 0.9 # tangent length from b-spline
        tangentVerticesOnBSpline = [segment[0], segment[1], segment[2]]
        tangentVerticesFromBSpline = [(segment[0] + (self.tangents[i][0] / scale)),
                                      (segment[1] + (self.tangents[i][1] / scale)), 
                                      (segment[2] + (self.tangents[i][2] / scale))]
        
        return tangentVerticesOnBSpline + tangentVerticesFromBSpline

    def addToBatch(self):
        bsplineVertices, tangents = ([], [])
        
        for i, point in enumerate(self.segments):
            for coordinate in self.tangent(point, i): tangents.append(coordinate) # get tangent vertices for every segment
            for coordinate in point: bsplineVertices.append(coordinate) # get b-spline vertices for every segment

        # batch add (vertices, draw_mode, group, (vertex_positions, color))
        self.batch.add(len(self.segments), GL_LINE_STRIP, None, ("v3f", bsplineVertices))

        tangentCoorPoints, tanVertNum = 6, 2 # tanget is two vertices, 3d, 2 * 3
        for i in range(int(len(tangents) / tangentCoorPoints)):
            tangent = tangents[(tangentCoorPoints * i):(tangentCoorPoints * i) + tangentCoorPoints] 
            self.batch.add(tanVertNum, GL_LINES, None, ("v3f", tangent), ("c3f", [0, 2, 3, 2, 1, 1])) # white-blueish color