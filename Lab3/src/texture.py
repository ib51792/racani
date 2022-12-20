from OpenGL.GL import *
from PIL.Image import open
import numpy

class Texture:
    
    def getID(self, filename):  
          
        with open(filename, 'r') as file: 
            data = file.getdata()
            imgSize = file.size

        imageData = numpy.array(list(data), numpy.uint8)

        textureID = glGenTextures(1)
        
        # align picture into groups of 4 bytes
        glPixelStorei(GL_UNPACK_ALIGNMENT, 4)
        glBindTexture(GL_TEXTURE_2D, textureID)
        
        # Specifies the index of the lowest defined mipmap level. Initial value is 0
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_BASE_LEVEL, 0)
        # Sets the index of the highest defined mipmap level. Initial value is 1000
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAX_LEVEL, 0)
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, imgSize[0], imgSize[1], 0, GL_RGB, GL_UNSIGNED_BYTE, imageData)
        
        return textureID
