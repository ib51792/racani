import particle as p, sys
from random import *
from pyglet.gl import *
from pyrr import Vector3


class ParticleSystem:
    def __init__(self, _json):
        self._json = _json
        self.particles = []
        self.color = {}
        self.texture = pyglet.image.load(sys.argv[1]).get_texture()
        self.generateParticles()
        self.timer = 0


    def generateParticles(self):
        number = randint(self._json['number'][0], 
                         self._json['number'][1])
        
        center = Vector3([randint(self._json['center'][0], 
                                  self._json['center'][1]) 
                          for _ in range(3)])
        
        color = self.setColor()
        
        for _ in range(0, number): 
            particle = p.Particle(self._json, center.copy())
            self.particles.append(particle)
            
            if self._json['fireworks'][0]:
                self.color[particle] = color


    def update(self, dt):
        self.timer += 1
        
        for i, particle in enumerate(self.particles):
            particle.update(dt)
            if particle.lifetime <= 0 or particle.size <= 0: 
                del self.particles[i]
                if particle in self.color: 
                    del self.color[particle]
                
        if self.timer % self._json['generateAfter'] == 0:
            self.generateParticles()


    def setColor(self):
        return [uniform(self._json['fireworks'][1],
                        self._json['fireworks'][2])
                for _ in range(4)]


    def draw(self):
        glEnable(GL_TEXTURE_2D)
        glBindTexture(GL_TEXTURE_2D, self.texture.id)
        
        glEnable(GL_BLEND)
        glBlendFunc(GL_ONE, GL_ONE)
        
        glBegin(GL_QUADS)
        
        for particle in self.particles:
            
            if particle in self.color:
                glColor4f(self.color[particle][0],
                          self.color[particle][1],
                          self.color[particle][2],
                          self.color[particle][3])
            
            glTexCoord2f(1, 1)
            glVertex3f(particle.position[0], 
                       particle.position[1] + particle.size, 
                       particle.position[2] + particle.size)
            
            glTexCoord2f(0, 1)
            glVertex3f(particle.position[0], 
                       particle.position[1] - particle.size, 
                       particle.position[2] + particle.size)
        	
            glTexCoord2f(0, 0)
            glVertex3f(particle.position[0], 
                       particle.position[1] - particle.size, 
                       particle.position[2] - particle.size)
           
            glTexCoord2f(1, 0)
            glVertex3f(particle.position[0], 
                       particle.position[1] + particle.size, 
                       particle.position[2] - particle.size)
            
        glEnd()
        glDisable(GL_BLEND)
        glDisable(GL_TEXTURE_2D)
