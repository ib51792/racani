from OpenGL.GL import *

class Cube:
    def __init__(self):
        self.vertices = [
             # x     y     z    s    t
            [-1.0, -1.0,  1.0, 0.0, 0.0,
              1.0, -1.0,  1.0, 1.0, 0.0,    # front side
              1.0,  1.0,  1.0, 1.0, 1.0,
             -1.0,  1.0,  1.0, 0.0, 1.0],

            [-1.0, -1.0, -1.0, 1.0, 0.0,
             -1.0,  1.0, -1.0, 1.0, 1.0,    # back side
              1.0,  1.0, -1.0, 0.0, 1.0,
              1.0, -1.0, -1.0, 0.0, 0.0],
            
            [ 1.0, -1.0, -1.0, 1.0, 0.0,
              1.0,  1.0, -1.0, 1.0, 1.0,    # right side
              1.0,  1.0,  1.0, 0.0, 1.0,
              1.0, -1.0,  1.0, 0.0, 0.0],
            
            [-1.0, -1.0, -1.0, 0.0, 0.0,
             -1.0, -1.0,  1.0, 1.0, 0.0,    # left side
             -1.0,  1.0,  1.0, 1.0, 1.0,
             -1.0,  1.0, -1.0, 0.0, 1.0]]
        
        
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
        
        for v in self.vertices:
            glTexCoord2f( v[3],  v[4]); glVertex3f( v[0],  v[1],  v[2])
            glTexCoord2f( v[8],  v[9]); glVertex3f( v[5],  v[6],  v[7])
            glTexCoord2f(v[13], v[14]); glVertex3f(v[10], v[11], v[12])
            glTexCoord2f(v[18], v[19]); glVertex3f(v[15], v[16], v[17])
        
        glEnd()
