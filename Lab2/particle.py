from random import *
from pyrr import Vector3


class Particle:
    def __init__(self, _json, position):
        self._json = _json
        self.position = position
        self.velocity = self.velocityVector()
        self.lifetime = self._json['lifetime']
        self.size = randint(self._json['size'][0], self._json['size'][1])


    def velocityVector(self):
        return Vector3([randrange(self._json['velocity'][0], 
                                  self._json['velocity'][1]) 
                        for _ in range(3)])
        
        
    def update(self, dt):
        self.position += self.velocity
        self.lifetime -= self._json['fade']
        self.size -= self._json['shrink'] * dt
