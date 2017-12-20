import body
import sdl2.ext

import numpy as np

class UpdateTranslation(sdl2.ext.Applicator):
    """Apply translation is used to update sprite's position on screen"""
    def __init__(self, center):
        super().__init__()
        self.center = np.array(center)
        self.componenttypes = body.Properties, sdl2.ext.Sprite

    def process(self, world, componentsets):
        for properties, sprite in componentsets:
            sprite.x, sprite.y, _ = (properties.get_translation() * [1, -1, 1] + self.center).astype(int)




class ApplyThings(sdl2.ext.Applicator):
    """what"""
    def __init__(self):
        super().__init__()
        self.componenttypes = body.Properties,

    def process(self, world, componentsets):
        for p, in componentsets:
            p._velocity += p._acceleration * world.constants.dt
            p._translation += p._velocity * world.constants.dt

            # print(np.linalg.norm(p._velocity))

            



class CalculateForce(sdl2.ext.Applicator):
    def __init__(self):
        super().__init__()
        self.componenttypes = body.Properties,

    def process(self, world, componentsets):
        killme = list(componentsets)
        for p_i, in killme:
            a = np.zeros([3])
            for p_j, in killme:
                if p_i is not p_j:
                    r = p_i._translation - p_j._translation
                    a += calculate_gravity_acceleration(world.constants.G, p_j._mass ,r)
            p_i._acceleration = a

def calculate_gravity_acceleration(G, m, r):
    return G * m * r / np.linalg.norm(r, ord=1)**3