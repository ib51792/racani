from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import keyboard
from src.collision import Collision
from src.cube import Cube
from src.maze import Maze
from src.movement import getIntendedPosition
from src.texture import Texture
from src.plane import Plane


class Scene:
    def __init__(self, _json):
        self._json = _json
        self.maze = Maze(_json['maze']['depth'], 
                         _json['maze']['width']).generate()
        
        self.collision = Collision()
        self.plane = Plane()
        self.cube = Cube()
        
        self.rendered = {
            "wall": None,
            "floor": None
            }
        
        self.texture = {
            "wall": _json['textures']['wall'],
            "floor": _json['textures']['floor'],
            }
        
        self.textureID = {
            "wall": None,
            "floor": None
            }
        
        self.flags = {
            "invisible": _json['flags']['invisible'],
            "floor": _json['flags']['floor'],
            "wall": _json['flags']['wall']
            }
        
        self.cameraPosition = [
            -2 * _json['maze']['width'] + 5, 
            0.0, 
            -2 * _json['maze']['depth'] - 5
            ]
        
        self.cameraRotation = 0.0
        self.rotationAngle = 1.0
        self.controls = 1.0
        self.window = None
        self.cubeSize = 2
        self.height = 480
        self.width = 640
        
        
    def initGL(self):    
        glClearColor(0.0, 0.0, 0.0, 0.0)
        glClearDepth(1.0)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        glShadeModel(GL_SMOOTH)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(50.0, self.width / self.height, 0.1, 100.0)
        glMatrixMode(GL_MODELVIEW)
        self.renderFloor()
        self.renderMaze()


    def renderFloor(self):
        self.rendered['floor'] = glGenLists(1)
        glNewList(self.rendered['floor'], GL_COMPILE)
        
        glPushMatrix()
        
        glTranslatef(0.0, -2.0, 0.0)
        glScalef(self._json['maze']['width'] * 2.5, 1.0, self._json['maze']['depth'] * 2.5)
        self.plane.draw(self.textureID['floor'])
        
        glPopMatrix()
        
        glEndList()


    def renderMaze(self):
        self.rendered['wall'] = glGenLists(1)
        glNewList(self.rendered['wall'], GL_COMPILE)
        
        glPushMatrix()
        
        glScalef(1.0, self.flags['wall'], 1.0)
        row, col = (0, 0)
    
        for i in self.maze:
            for j in i:
                if (j == 1): self.cube.draw(self.textureID['wall'])
                
                glTranslatef(self.cubeSize, 0.0, 0.0)

                col += 1

            glTranslatef(((self.cubeSize * col) * -1), 0.0, self.cubeSize)

            row += 1
            col = 0
            
        glPopMatrix()
        
        glEndList()


    def draw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        glTranslatef(0.0, 0.0, 0.0)
        glRotatef(self.cameraRotation, 0.0, self.controls, 0.0)
        glTranslatef(self.cameraPosition[0], self.cameraPosition[1], self.cameraPosition[2])
            
        if self.flags['floor']:
            glCallList(self.rendered['floor'])
            
        glCallList(self.rendered['wall'])
        
        glutSwapBuffers()
    
        self.handleInput()


    def handleInput(self):
        
        if keyboard.is_pressed("a"):
            self.cameraRotation -= self.rotationAngle
        elif keyboard.is_pressed("d"):
            self.cameraRotation += self.rotationAngle
        elif keyboard.is_pressed(chr(27)):
            glutDestroyWindow(self.window)
            
        iX, _, iZ = self.cameraPosition
        
        if keyboard.is_pressed("w"): 
            iX, iZ = getIntendedPosition(self.cameraRotation, iX, iZ, 90, 1)
        elif keyboard.is_pressed("s"): 
            iX, iZ = getIntendedPosition(self.cameraRotation, iX, iZ, 90, -1)
        elif keyboard.is_pressed("g"): 
            iX, iZ = getIntendedPosition(self.cameraRotation, iX, iZ, 0, 1)
        elif keyboard.is_pressed("h"): 
            iX, iZ = getIntendedPosition(self.cameraRotation, iX, iZ, 0, -1)

        if self.flags['invisible'] or not (self.collision.testCollision(self.maze, iX, iZ)):
            self.cameraPosition = [iX, 0, iZ]
        
        if self.cameraPosition[2] >= 1.6:
            glutDestroyWindow(self.window) 
    
    
    def JoinStyle(self, val):
    
        match val:
            case 1:
                glutDestroyWindow(self.window)
            case 2:
                self.flags['invisible'] ^= 1
            case 3:
                self.flags['floor'] ^= 1
            case 4:
                self.controls *= -1
            case 5:
                self.flags['wall'] = 1000 if self.flags['wall'] == 1 else 1
                self.renderMaze()
                
        return 0
    
    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(200, 200)

        self.window = glutCreateWindow('Random Maze')
    
        glutCreateMenu(self.JoinStyle)
        glutAddMenuEntry('Exit', 1)
        glutAddMenuEntry('Invisible', 2)
        glutAddMenuEntry('Floor', 3)
        glutAddMenuEntry('Movement', 4)
        glutAddMenuEntry('Walls', 5)
        glutAttachMenu(GLUT_RIGHT_BUTTON)

        texture = Texture()
        self.textureID['wall'] = texture.getID(self.texture['wall'])
        self.textureID['floor'] = texture.getID(self.texture['floor'])

        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        self.initGL()
        glutMainLoop()