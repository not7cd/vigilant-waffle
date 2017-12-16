import sys
import sdl2
import sdl2.ext

import numpy as np

import force as sim
import body

G =  6.674*10**(-9)

class CentralGravitySystem(sdl2.ext.Applicator):
    def __init__(self):
        super(CentralGravitySystem, self).__init__()
        self.componenttypes = body.Properties, sim.Forces

    def process(self, world, componentsets):
        for properties, forces in componentsets:
            distance = properties.position - np.array([250,250,0])
            distance_norm = np.linalg.norm(distance)
            if distance_norm > 10:
                
                force = (distance/distance_norm) * -self.gravity_force(G, properties.mass, 100000000, distance_norm)

                print('grav' ,force)
                forces.resultant = force

    def gravity_force(self, gravity_const, mass1, mass2, distance):
        return gravity_const*(mass1*mass2)/distance**2
            
class Static(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        super(Static, self).__init__()
        self.sprite = sprite
        self.sprite.position = posx, posy


def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Gravity", size=(500, 500))
    window.show()

    world = sdl2.ext.World()


    spriterenderer = sim.SoftwareRenderer(window)
    movement = sim.MovementSystem(0, 0, 500, 500)
    force = sim.ApplyForceSystem()
    gravity_force = CentralGravitySystem()

    world.add_system(gravity_force)
    world.add_system(force)
    world.add_system(movement)
    world.add_system(spriterenderer)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    
    sp = factory.from_color(sdl2.ext.Color(240, 200, 0), size=(10, 10))
    Static(world, sp, 245, 245)

    for x in range(100,230,2):
        sp = factory.from_color(sdl2.ext.Color(x, 0, 255-x), size=(2, 2))
        dummy = sim.Body(world, sp, 250., float(x))
        dummy.properties.velocity[0] = .1
        dummy.properties.mass = float(x)

    
    



    running = True
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break


        # sdl2.SDL_Delay(1)
        world.process()
    return 0


if __name__ == "__main__":
    sys.exit(run())