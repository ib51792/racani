#!/usr/bin/env python
from pyglet.gl import *
import system as p, json


class Window(pyglet.window.Window):
    def __init__(self, _json, **kwargs):
        super().__init__(**kwargs)
        self.system = p.ParticleSystem(_json)
        pyglet.clock.schedule_interval(self.update, (1.0/120.0))


    def update(self, dt):
        self.system.update(dt)


    def on_draw(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        gluPerspective(100, 1, 1, 10000)
       
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(1000, 0, 0, 0, 0, 0, 0, 1, 0)
        
        self.clear()
        self.system.draw()
        glFlush()


if __name__=="__main__":
    
    with open('particle.json', 'r') as file: 
        _json = json.load(file)

    window = Window(_json, fullscreen=True)
    pyglet.app.run()
