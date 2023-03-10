from src.movement import getIntendedPosition
from src.collision import Collision
from src.texture import Texture
from src.plane import Plane
from src.path import Path
from src.cube import Cube
from src.maze import Maze
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *
import keyboard


class Scene:
    def __init__(self, _json):
        self.cameraRotation = 0.0
        self.rotationAngle = 1.0
        self.controls = 1.0
        self.window = None
        self.cubeSize = 2
        self.height = 480
        self.width = 640
        
        self._json = _json
        self.maze = Maze(_json['maze']['depth'], 
                         _json['maze']['width']).generate()
        
        self.path, self.start = Path(self.maze).find()
        self.collision = Collision()
        self.plane = Plane()
        self.cube = Cube()
        
        self.rendered = {
            "wall": None,
            "floor": None,
            "path": None
            }
        
        self.texture = {
            "wall": _json['textures']['wall'],
            "floor": _json['textures']['floor'],
            "path": _json['textures']['path']
            }
        
        self.textureID = {
            "wall": None,
            "floor": None,
            "path": None
            }
        
        self.flags = {
            "invisible": _json['flags']['invisible'],
            "floor": _json['flags']['floor'],
            "wall": _json['flags']['wall'],
            "path": _json['flags']['path']
            }
        
        self.cameraPosition = [
            (self.cubeSize * (self.start * -1)),
            0.0, 
            ((self.cubeSize * (_json['maze']['depth'] * -1)) - 2)
            ]
        
        
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
        self.renderPath()


    def renderPath(self):
        self.rendered['path'] = glGenLists(1)
        glNewList(self.rendered['path'], GL_COMPILE)
        
        glPushMatrix()
        # needs to be a little bit above floor
        glTranslatef(0.0, -1.999, 0.0)
        
        nextRow = self.cubeSize * (len(self.maze[0]) * -1)
        
        for j, v in enumerate(self.maze):
            for i, _ in enumerate(v):
                if ((i, j) in self.path):
                    self.path.remove((i, j))
                    self.plane.draw(self.textureID['path'])
                glTranslatef(self.cubeSize, 0.0, 0.0)

            glTranslatef(nextRow, 0.0, self.cubeSize)
            
        glPopMatrix()
        glEndList()


    def renderFloor(self):
        self.rendered['floor'] = glGenLists(1)
        glNewList(self.rendered['floor'], GL_COMPILE)
        
        width = self._json['maze']['width'] * self.cubeSize * 1.1
        depth = self._json['maze']['depth'] * self.cubeSize * 1.1
        
        glPushMatrix()
        
        glTranslatef(0.0, -2.0, 0.0)
        glScalef(width, 1.0, depth)
        self.plane.draw(self.textureID['floor'])
       
        glPopMatrix()
        glEndList()


    def renderMaze(self):
        self.rendered['wall'] = glGenLists(1)
        glNewList(self.rendered['wall'], GL_COMPILE)
        
        glPushMatrix()
        glScalef(1.0, self.flags['wall'], 1.0)
        
        nextRow = self.cubeSize * (len(self.maze[0]) * -1)
    
        for i in self.maze:
            for j in i:
                if j: self.cube.draw(self.textureID['wall'])
                glTranslatef(self.cubeSize, 0.0, 0.0)
                
            glTranslatef(nextRow, 0.0, self.cubeSize)
            
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
            
        if self.flags['path']:
            glCallList(self.rendered['path'])
            
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
        
        #if self.cameraPosition[2] >= 1.6:
        #    glutDestroyWindow(self.window) 
    
    
    def menu(self, val):
    
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
                self.flags['wall'] = self._json["flags"]["wall"] if self.flags['wall'] == 1 else 1
                self.renderMaze()
            case 6:
                self.flags['path'] ^= 1
                
        return 0
    
    
    def main(self):
        glutInit()
        glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
        glutInitWindowSize(640, 480)
        glutInitWindowPosition(200, 200)

        self.window = glutCreateWindow('Random Maze')
    
        glutCreateMenu(self.menu)
        glutAddMenuEntry('Exit', 1)
        glutAddMenuEntry('Invisible', 2)
        glutAddMenuEntry('Floor', 3)
        glutAddMenuEntry('Movement', 4)
        glutAddMenuEntry('Walls', 5)
        glutAddMenuEntry('Path', 6)
        glutAttachMenu(GLUT_RIGHT_BUTTON)

        texture = Texture()
        self.textureID['wall'] = texture.getID(self.texture['wall'])
        self.textureID['floor'] = texture.getID(self.texture['floor'])
        self.textureID['path'] = texture.getID(self.texture['path'])
        
        glutDisplayFunc(self.draw)
        glutIdleFunc(self.draw)
        self.initGL()
        glutMainLoop()