import sys
import sdl2
import sdl2.ext

import numpy as np

import body as sim
from body import SoftwareRenderer, MovementSystem





class Forces(object):
    """docstring for Forces"""
    def __init__(self):
        super(Forces, self).__init__()
        self.resultant = np.array([0.,2.,0.])
        

class ApplyForceSystem(sdl2.ext.Applicator):
    def __init__(self):
        super(ApplyForceSystem, self).__init__()
        self.componenttypes = sim.Properties, Forces

    def process(self, world, componentsets):
        for properties, forces in componentsets:
            acceleration = np.divide(forces.resultant, properties.mass)
            properties.velocity += acceleration * 5
            # print(acceleration)



class Properties(sim.Properties):
    """docstring for Properties"""
    def __init__(self,position, mass, velocity):
        super(Properties, self).__init__(position, mass, velocity)
        
        

class Body(sim.Body):
    """docstring for Body"""
    def __init__(self, world, sprite, posx, posy):
        super(Body, self).__init__(world, sprite, posx, posy)
        # self.properties = Properties([posx, posy, 0], 10, [0,0,0])
        self.forces = Forces()

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Force", size=(500, 500))
    window.show()

    world = sdl2.ext.World()


    spriterenderer = SoftwareRenderer(window)
    movement = MovementSystem(0, 0, 500, 500)
    force = ApplyForceSystem()

    world.add_system(force)
    world.add_system(movement)
    world.add_system(spriterenderer)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp = factory.from_color(sim.WHITE, size=(6, 6))

    dummy = Body(world, sp, 200., 200.)
    dummy.properties.velocity[0] = 0.1
    dummy.properties.mass = 1000.
    dummy.forces.resultant = np.array([0., 1., 0.])



    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break


        sdl2.SDL_Delay(10)
        world.process()
    return 0


if __name__ == "__main__":
    sys.exit(run())