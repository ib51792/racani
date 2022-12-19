from pyglet.gl import *
import readFile as f

class Object:
    vertices, polygons = ([], [])
    batch = pyglet.graphics.Batch()

    def __init__(self, filepath):
        f.readFile(self, filepath)
        self.addToBatch()

    def addToBatch(self):
        for polygon in self.polygons:
            v = []
            for i in range(3): v.append(self.vertices[polygon[i] - 1])
            self.batch.add(3, GL_TRIANGLES, None,
                           ("v3f", [v[0][0], v[0][1], v[0][2], v[1][0], v[1][1], v[1][2], v[2][0], v[2][1], v[2][2]]),
                           ("c3B", (255, 255, 0)*3))