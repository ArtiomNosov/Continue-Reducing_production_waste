__version__ = "$Id:$"
__docformat__ = "reStructuredText"

# Python imports
import random
import math

# Library imports
import pygame

# pymunk imports
import pymunk
import pymunk.pygame_util

import time


#Indient in borders
INDENT = 10
#Radius of borders
LINE_RADIUS = INDENT
#Lenght and height of space
LENGTH, HEIGHT = 600 + LINE_RADIUS, 600 + LINE_RADIUS
#Size of figures
KOFFICIENT = 20
#Count of experients
COUNT_OPERATIONS_DEBUG = 10
#Count of additicion ticks for line
COUNT_DELTA_TICKS = 1
#[size (polygon), type]
#Type of drawing figures: 1 - circles, 2 - triangle, 3 - squares, 4 - polygon
FIGURES_LIST = [[1,1], [1,3], [1,1], [2,2], [2,1], [2,2], [3,3], [3,2], [3,1], [4,1]]
TICKS_TO_NEXT_BALL = 1


class Emulator(object):
    """
    This class implements a simple scene in which there is a static platform (made up of a couple of lines)
    that don't move. Shapes appear occasionally and drop onto the platform.
    """

    def __init__(self, interface=False, FIGURES_LIST=[], COUNT_OPERATIONS_DEBUG=1, position_x=[]) -> None:
        # Space
        self._space = pymunk.Space()
        self._space.gravity = (0.0, 900.0)

        self.interface = interface
        # Physics
        # Time step
        self._dt = 1.0 / 100.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 500

        # pygame
        if self.interface:
            pygame.init()
            self._screen = pygame.display.set_mode((LENGTH + INDENT, HEIGHT + INDENT))
            self._clock = pygame.time.Clock()

            self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)

        # Static barrier walls (lines) that the balls bounce off of
        self._add_static_scenery()

        # Execution control and time until the next ball spawns
        self._running = True
        self._ticks_to_next_ball = TICKS_TO_NEXT_BALL
        self.ticks_to_spawn_line = 1
        #Count figures
        self.figures_to_create = len(FIGURES_LIST)
        self.iter = 0
        self.max_height = 100000
        self.next_step = False
        self.line_y = 0
        self.COUNT_OPERATIONS_DEBUG = COUNT_OPERATIONS_DEBUG
        self.delta_ticks = COUNT_DELTA_TICKS
        #0 - creating objects,
        self.stage = 0
        self.start_time = time.time()
        self.FIGURES_LIST = FIGURES_LIST
        self.position_x = position_x



    def run(self) -> None:
        """
        The main loop of the game.
        :return: None
        """
        # Main loop
        while self._running:
            # Progress time forward
            for x in range(self._physics_steps_per_frame):
                self._space.step(self._dt)

            if self.interface:
                self._process_events()
                self._update_figures()
                self._clear_screen()
                self._draw_objects()
                pygame.display.flip()
                # Delay fixed time between frames
                self._clock.tick(1200000000)
                pygame.display.set_caption("fps: " + str(self._clock.get_fps()))
                self.check_line()

                if self.next_step:
                    self._clear_screen()
            elif not(self.interface):
                self._update_figures()
                # Delay fixed time between frames
                #self._clock.tick(1200000000)
                self.check_line()


    def _add_static_scenery(self) -> None:
        """
        Create the static bodies.
        :return: None
        """
        static_body = self._space.static_body
        static_lines = [
            pymunk.Segment(static_body, (INDENT, INDENT), (INDENT, HEIGHT), LINE_RADIUS),
            pymunk.Segment(static_body, (INDENT, INDENT), (LENGTH, INDENT), LINE_RADIUS),
            pymunk.Segment(static_body, (LENGTH, HEIGHT), (LENGTH, INDENT), LINE_RADIUS),
            pymunk.Segment(static_body, (LENGTH, HEIGHT), (INDENT, LENGTH), LINE_RADIUS),
        ]
        for line in static_lines:
            line.elasticity = 0.0
            line.friction = 0.1
        self._space.add(*static_lines)


    def _process_events(self) -> None:
        """
        Handle game and events like keyboard input. Call once per frame only.
        :return: None
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self._running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_p:
                pygame.image.save(self._screen, "bouncing_balls.png")


    def _update_figures(self) -> None:
        """
        Create/remove balls as necessary. Call once per frame only.
        :return: None
        """
        self._ticks_to_next_ball -= 1
        if self._ticks_to_next_ball <= 0 and self.figures_to_create > 0 and self.stage == 0:
            self._create_figure(10, self.FIGURES_LIST[self.iter])
            self._ticks_to_next_ball = TICKS_TO_NEXT_BALL
            self.figures_to_create -= 1
            self.iter += 1
        if self.figures_to_create == 0 and self.ticks_to_spawn_line != 0 and self.stage == 0:
            if self.position_x != []:
                self.position_x.pop(0)
            self.ticks_to_spawn_line -= 1
        if self.figures_to_create == 0 and self.ticks_to_spawn_line == 0 and self.stage == 0:
            self._create_line()
            self.stage = 1
            self.next_step = True

        if self.stage == 2 and self.delta_ticks != 0:
            self.delta_ticks -= 1


    def _create_figure(self, mass, element) -> None:
        """
        Create a ball.
        :return:
        """

        global INDENT, LENGTH
        if element[1] == 1:
            element_size = element[0] * KOFFICIENT
            inertia = pymunk.moment_for_circle(mass, 0, element_size, (0, 0))
            body = pymunk.Body(mass, inertia)

            if self.position_x == []:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            elif self.position_x[0] == []:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            else:
                x = self.position_x[0][0]
                self.position_x[0].pop(0)

            body.position = x, 200
            shape = pymunk.Circle(body, element_size, (0, 0))
            shape.elasticity = 0.0
            shape.friction = 0.2
            self._space.add(body, shape)
        if element[1] == 2:
            element_size = element[0] * KOFFICIENT
            triangle = [(-element_size, -element_size), (element_size, -element_size), (0, element_size)]
            inertia = pymunk.moment_for_poly(mass, triangle, (0, 0))
            body = pymunk.Body(mass, inertia)

            if self.position_x == []:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            elif self.position_x[0] == []:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            else:
                x = self.position_x[0][0]
                self.position_x[0].pop(0)

            body.position = x, 200
            shape = pymunk.Poly(body, triangle)
            #shape.density = 0.01
            shape.elasticity = 0.0
            shape.friction = 0.2
            self._space.add(body, shape)
        if element[1] == 3:
            element_size = element[0] * KOFFICIENT
            triangle = [(-element_size, -element_size), (element_size, -element_size), (element_size, element_size), (-element_size, element_size)]
            inertia = pymunk.moment_for_poly(mass, triangle, (0, 0))
            body = pymunk.Body(mass, inertia)

            if self.position_x == []:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            elif self.position_x[0] == []:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            else:
                x = self.position_x[0][0]
                self.position_x[0].pop(0)

            body.position = x, 200
            shape = pymunk.Poly(body, triangle)
            #shape.density = 0.01
            shape.elasticity = 0.0
            shape.friction = 0.2
            self._space.add(body, shape)


    def _create_line(self):
        body = pymunk.Body(mass=100, moment=math.inf)
        body.position = ((2*INDENT + LENGTH)/2, 2*INDENT)
        shape = pymunk.Segment(body, (-LENGTH/2, 0), (LENGTH/2, 0), radius=1)
        shape.elasticity = 0.0
        shape.body.velocity = (0, 1)
        self._space.add(body, shape)


#stage = 1 - start moving
#stage = 2 - after close collision
#stage = 3 - end
    def check_line(self):
        if self.COUNT_OPERATIONS_DEBUG > 0:

            if self.stage == 1:
                line_y2 = self._space.bodies[len(self.FIGURES_LIST)].position.y
                if (line_y2 - self.line_y < 0.0001) and (self.delta_ticks != 0):
                    self.stage = 2
                self.line_y = line_y2

            if self.stage == 2:
                line_y2 = self._space.bodies[len(self.FIGURES_LIST)].position.y
                if (line_y2 - self.line_y < 0.0001) and (self.delta_ticks == 0):
                    self.stage = 3
                self.line_y = line_y2

            if self.stage == 3:
                print(self.line_y)
                for i in range(4, len(self.FIGURES_LIST) + 5):
                    self._space.remove(self._space.shapes[4])
                    self._space.remove(self._space.bodies[0])
                self.COUNT_OPERATIONS_DEBUG -= 1
                if self.COUNT_OPERATIONS_DEBUG > 0:
                    self.figures_to_create = len(self.FIGURES_LIST)
                    self.iter = 0
                    self.line_y = 0
                    self.delta_ticks = COUNT_DELTA_TICKS
                    self.stage = 0
                else:
                    print("--- %s seconds ---" % (time.time() - self.start_time))
                    self._running = False
        else:
            self._running = False




    def _clear_screen(self) -> None:
        """
        Clears the screen.
        :return: None
        """
        self._screen.fill(pygame.Color("white"))

    def _draw_objects(self) -> None:
        """
        Draw the objects.p
        :return: None
        """
        self._space.debug_draw(self._draw_options)


def RunEmulations(interface=False, FIGURES_LIST=[], COUNT_OPERATIONS_DEBUG=1, position_x=[]):
    '''
    This function insert lists of figures and it's positions and print max height of every iteration.\n
    :param interface: ON/OFF visual interface.
    :param FIGURES_LIST: List of your figures. Insert list: [[size (polygon), type],...].
    :param COUNT_OPERATIONS_DEBUG: Count of iterations.
    :param position_x: Positions of your figures. Insert list: [[pos1_figure1, pos1_figure2, ...], ..., [posx_figure1, posx_figure2, ...]].
    :return: max_height.
    '''

    game = Emulator(interface=interface, FIGURES_LIST=FIGURES_LIST, COUNT_OPERATIONS_DEBUG=COUNT_OPERATIONS_DEBUG, position_x=position_x)
    game.run()


if __name__ == "__main__":
    RunEmulations(interface=False, FIGURES_LIST=FIGURES_LIST, COUNT_OPERATIONS_DEBUG=10, position_x=[])

'''
[[100,100,100,100,100,100,100,100,100,100], [400,400,400,400,400,400,400,400,400,400]]
'''