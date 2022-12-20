from OpenGL.GL import *

class Plane:

    def draw(self, textureID):

        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, textureID)
        
        # Repeat texture if smaller than cube
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        
        # when MAGnifying the image or when MINifying the image, use NEAREST filtering
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_NEAREST)
        glTexParameterf(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST)

        # Generate Mipmap
        glGenerateMipmap(GL_TEXTURE_2D)

        glBegin(GL_QUADS)

        glTexCoord2f(0.0, 0.0); glVertex3f( 1.0, 1.0,-1.0)
        glTexCoord2f(1.0, 0.0); glVertex3f(-1.0, 1.0,-1.0)
        glTexCoord2f(1.0, 1.0); glVertex3f(-1.0, 1.0, 1.0)
        glTexCoord2f(0.0, 1.0); glVertex3f( 1.0, 1.0, 1.0)
        
        glEnd()
