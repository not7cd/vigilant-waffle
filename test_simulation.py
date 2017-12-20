import sys
import sdl2.ext

import body
import applicators

from random import random

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)


WINDOW_X, WINDOW_Y = 700, 700

def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("N-body simulation", size=(WINDOW_X, WINDOW_Y))
    window.show()

    world = body.World(G=-6.674*10**(-2), dt=4)
    # world = sdl2.ext.World()


    spriterenderer = SoftwareRenderer(window)

    vel = applicators.ApplyThings()
    calc = applicators.CalculateForce()

    world.add_system(spriterenderer)
    world.add_system(vel)
    world.add_system(calc)
    world.add_system(applicators.UpdateTranslation([WINDOW_X//2, WINDOW_Y//2, 0]))

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    
    sp = factory.from_color(sdl2.ext.Color(240, 200, 0), size=(3, 3))
    s1 = body.Particle(world, sp, 10.)
    s1.properties.set_velocity(0, -0.1, 0)

    sp = factory.from_color(sdl2.ext.Color(240, 200, 0), size=(3, 3))
    s2 = body.Particle(world, sp, 10.)
    s2.properties.set_translation(20, 0, 0)
    s2.properties.set_velocity(0, 0.1, 0)


    for x in range(1,10):
        sp = factory.from_color(sdl2.ext.Color(100+x*10, 200, 200-x*10), size=(2, 2))
        s3 = body.Particle(world, sp, 0.05)
        s3.properties.set_translation(0, 50+15*x, 0)
        s3.properties.set_velocity(.10, 0, 0)

        


    running = True

    cycles = 0
    while running:
        events = sdl2.ext.get_events()
        for event in events:
            if event.type == sdl2.SDL_QUIT:
                running = False
                break


        world.process()
        sdl2.SDL_Delay(1)
        cycles += 1
        print('cycle:', cycles)
    return 0
    

if __name__ == "__main__":
    sys.exit(run())
