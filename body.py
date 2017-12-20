import sdl2.ext

import numpy as np


class Properties(object):
    """docstring for Properties"""

    

    def __init__(self, mass, tx=0, ty=0, tz=0):
        super().__init__()

        self.set_mass(mass)
        self.set_translation(tx, ty, tz)
        self.set_velocity(0, 0, 0)
        self._acceleration = np.zeros([3])

    def set_mass(self, mass):
        if mass <= 0:
            raise ValueError("Mass cannot be negative or zero")
        self._mass = float(mass)

    def get_mass(self):
        return self._mass

    def set_translation(self, x, y, z):
        self._translation = np.array([x, y, z], dtype=float)

    def get_translation(self):
        return self._translation

    def set_velocity(self, x, y, z):
        self._velocity = np.array([x, y, z], dtype=float)
        
    def get_velocity(self):
        return self._velocity



class Particle(sdl2.ext.Entity):
    """docstring for Particle"""


    def __init__(self, world, sprite, mass):
        
        self.sprite = sprite
        self.properties = Properties(mass)

class Constants():
    """docstring for Constants"""
    def __init__(self, G, dt):
        super().__init__()
        self.G = G
        self.dt = dt
        

class World(sdl2.ext.World):
    """docstring for World"""
    def __init__(self, G, dt):
        super().__init__()
        self.constants = Constants(G, dt)

        

if __name__ == '__main__':
    world = sdl2.ext.World()
    mp1 = Particle(world,None, 10)
    mp2 = Particle(world,None, 1)
    mp3 = Particle(world,None, 1000000000)