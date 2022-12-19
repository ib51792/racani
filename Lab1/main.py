#!/usr/bin/env python

import argparse, ctypes, rotation as r, BSpline as b, Object as o
from pyglet.gl import *

parser = argparse.ArgumentParser()
parser.add_argument("-d", action='store_true')
options = parser.parse_args()

verticesMove = 0

obj, spline = o.Object("frog.obj"), b.BSpline("bspline.obj")
pos, rotZ, rotY, rotX = [-40, 0, -55], 1, 50, 0
window = pyglet.window.Window(height=900, width=1200, resizable=True)

@window.event
def on_draw():
    global pos, rotZ, rotY, rotX, verticesMove
    window.clear()

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(90, 1, 1, 100)

    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    glTranslatef(*pos)
    glRotatef(rotY, rotX, 1, 0)

    glPushMatrix()
    currentPoint, currentTangent = (spline.segments[verticesMove], spline.tangents[verticesMove])

    if options.d:
        RInv = r.rotationDCM(currentTangent, spline.d2s[verticesMove])
        tmp = [RInv[i][j] for i in range(4) for j in range(4)]
        tmp = (ctypes.c_float * len(tmp))(*tmp)
        glTranslatef(currentPoint[0], currentPoint[1], currentPoint[2])
        glMultMatrixf(tmp)

    else:
        glTranslatef(currentPoint[0], currentPoint[1], currentPoint[2])
        rotAxis, rotAngle = r.rotation([0, 0, 1], currentTangent)
        glRotatef(rotAngle, rotAxis[0], rotAxis[1], rotAxis[2])

    obj.batch.draw()
    glPopMatrix()
    spline.batch.draw()
    glFlush()

def update(dt):
    global verticesMove
    verticesMove += 1
    if verticesMove >= len(spline.segments): verticesMove = 0

@window.event
def on_key_press(s, m):
    global rotY, rotX, rotZ

    match s:
        case pyglet.window.key.UP: rotX -= 1
        case pyglet.window.key.DOWN: rotX += 1
        case pyglet.window.key.LEFT: rotY -= 1
        case pyglet.window.key.RIGHT: rotY += 1
        case pyglet.window.key.W: rotZ += 1
        case pyglet.window.key.S: rotZ -= 1

pyglet.clock.schedule(update)
pyglet.app.run()
    