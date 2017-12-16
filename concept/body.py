import sys
import sdl2
import sdl2.ext

import numpy as np

WHITE = sdl2.ext.Color(255, 255, 255)

class Vector(object):
    def __init__(self, x=0, y=0, z=0):
        super(Vector, self).__init__()
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return "Vector({}, {}, {})".format(self.x, self.y, self.z)

class Properties(object):
    """docstring for Properties"""
    def __init__(self, position=[0,0,0], mass=1, velocity=[0,0,0]):
        super(Properties, self).__init__()
        self.position = np.array(position)
        self.velocity = np.array(velocity)
        self.mass = mass

class MovementSystem(sdl2.ext.Applicator):
    def __init__(self, minx, miny, maxx, maxy):
        super(MovementSystem, self).__init__()
        self.componenttypes = Properties, sdl2.ext.Sprite
        self.minx = minx
        self.miny = miny
        self.maxx = maxx
        self.maxy = maxy

    def process(self, world, componentsets):
        for properties, sprite in componentsets:
            swidth, sheight = sprite.size
            # apply velocity
            properties.position += properties.velocity * 5

            # print(properties.velocity)

            sprite.x = int(properties.position[0])
            sprite.y = int(properties.position[1])

            # keep in bounds
            sprite.x = max(self.minx, sprite.x)
            sprite.y = max(self.miny, sprite.y)

            pmaxx = sprite.x + swidth
            pmaxy = sprite.y + sheight
            if pmaxx > self.maxx:
                sprite.x = self.maxx - swidth
            if pmaxy > self.maxy:
                sprite.y = self.maxy - sheight


class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, sdl2.ext.Color(0, 0, 0))
        super(SoftwareRenderer, self).render(components)


class Body(sdl2.ext.Entity):
    def __init__(self, world, sprite, posx=0, posy=0):
        super(Body, self).__init__()
        self.sprite = sprite
        self.sprite.position = posx, posy
        self.properties = Properties([posx, posy, 0], 10., [0.,0.,0.])


def run():
    sdl2.ext.init()
    window = sdl2.ext.Window("Body", size=(500, 500))
    window.show()

    world = sdl2.ext.World()


    spriterenderer = SoftwareRenderer(window)
    movement = MovementSystem(0, 0, 500, 500)

    world.add_system(movement)
    world.add_system(spriterenderer)

    factory = sdl2.ext.SpriteFactory(sdl2.ext.SOFTWARE)
    sp = factory.from_color(WHITE, size=(6, 6))

    dummy = Body(world, sp, 200., 200.)
    dummy.properties.velocity[1] = 1
    dummy.properties.velocity[0] = -0.5
    dummy.properties.mass = 10

    print(dummy.properties.velocity)

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