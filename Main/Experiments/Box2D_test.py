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

import itertools

import ast

import pandas as pd

import numpy as np

import timeit

# Indient in borders
INDENT = 10
# Radius of borders
LINE_RADIUS = INDENT
# Length and height of space
LENGTH, HEIGHT = 800 + LINE_RADIUS, 800 + LINE_RADIUS
# Size of figures
KOFFICIENT = 30
# Count of experiments
COUNT_OPERATIONS_DEBUG = 1
# Count of addition ticks for line
COUNT_DELTA_TICKS = 2
TICKS_TO_NEXT_BALL = 1


class Iterator(object):
    """
    iterator
    """

    def __init__(self, list_length=0):
        self.position = 0
        self.len = list_length
        self.percent_25 = False
        self.percent_50 = False
        self.percent_75 = False
        self.percent_100 = False

    def increase(self):
        self.position += 1

    def get_position(self):
        return self.position

    def check_percent(self):
        if (round(self.position / self.len * 100) == 25) and not self.percent_25:
            self.percent_25 = True
            return int(25)
        elif (round(self.position / self.len * 100) == 50) and not self.percent_50:
            self.percent_50 = True
            return int(50)
        elif (round(self.position / self.len * 100) == 75) and not self.percent_75:
            self.percent_75 = True
            return int(75)
        elif (round(self.position / self.len * 100) == 100) and not self.percent_100:
            self.percent_100 = True
            return int(100)
        else:
            return None




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
        self._dt = 1.0 / 60.0
        # Number of physics steps per screen frame
        self._physics_steps_per_frame = 90

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
        # Count figures
        self.figures_to_create = len(FIGURES_LIST)
        self.iter = 0
        self.max_height = 100000
        self.next_step = False
        self.line_y = 0
        self.COUNT_OPERATIONS_DEBUG = COUNT_OPERATIONS_DEBUG
        self.delta_ticks = COUNT_DELTA_TICKS
        # 0 - creating objects,
        self.stage = 0
        self.FIGURES_LIST = FIGURES_LIST
        self.position_x = position_x

        self.screenshot80 = None
        self.screenshot81 = None
        self.screenshot82 = None
        self.screenshot83 = None
        self.screenshot84 = None
        self.screenshot85 = None
        self.screenshot86 = None
        self.screenshot87 = None
        self.screenshot88 = None
        self.screenshot89 = None
        self.screenshot90 = None

        self.result = []

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
            elif not self.interface:
                self._update_figures()
                # Delay fixed time between frames
                # self._clock.tick(1200000000)
                self.check_line()
        return self.result

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
            if self.position_x:
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

            if not self.position_x:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            elif not self.position_x[0]:
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

            if not self.position_x:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            elif not self.position_x[0]:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            else:
                x = self.position_x[0][0]
                self.position_x[0].pop(0)

            body.position = x, 200
            shape = pymunk.Poly(body, triangle)
            shape.elasticity = 0.0
            shape.friction = 0.2
            self._space.add(body, shape)
        if element[1] == 3:
            element_size = element[0] * KOFFICIENT
            triangle = [(-element_size, -element_size), (element_size, -element_size), (element_size, element_size),
                        (-element_size, element_size)]
            inertia = pymunk.moment_for_poly(mass, triangle, (0, 0))
            body = pymunk.Body(mass, inertia)

            if not self.position_x:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            elif not self.position_x[0]:
                x = random.randint(2 * INDENT + element_size, LENGTH - element_size)
            else:
                x = self.position_x[0][0]
                self.position_x[0].pop(0)

            body.position = x, 200
            shape = pymunk.Poly(body, triangle)
            shape.elasticity = 0.0
            shape.friction = 0.2
            self._space.add(body, shape)
        if element[1] == 4:
            max_delta = [[], []]
            for i in range(len(element[0])):
                max_delta[0].append(element[0][i][0])
                max_delta[1].append(element[0][i][1])
            wide = round((max(max_delta[0]) - min(max_delta[0])) / 2)
            max_delta[0] = min(max_delta[0])
            max_delta[1] = min(max_delta[1])
            for i in range(len(element[0])):
                element[0][i] = ((element[0][i][0] - max_delta[0]) / 2, (element[0][i][1] - max_delta[1]) / 2)

            inertia = pymunk.moment_for_poly(mass, element[0], (0, 0))
            body = pymunk.Body(mass, inertia)
            shape = pymunk.Poly(body, element[0])

            if not self.position_x:
                x = random.randint(0, LENGTH - wide)
            elif not self.position_x[0]:
                x = random.randint(0, LENGTH - wide)
            else:
                x = self.position_x[0][0]
                self.position_x[0].pop(0)

            body.position = x, 200
            shape.elasticity = 0
            shape.friction = 0.2

            self._space.add(body, shape)

    def _create_line(self):
        body = pymunk.Body(mass=100, moment=math.inf)
        body.position = ((2 * INDENT + LENGTH) / 2, 2 * INDENT)
        shape = pymunk.Segment(body, (-LENGTH / 2, 0), (LENGTH / 2, 0), radius=1)
        shape.elasticity = 0.0
        shape.body.velocity = (0, 1)
        self._space.add(body, shape)

    # stage = 1 - start moving
    # stage = 2 - after close collision
    # stage = 3 - end
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
                self.result.append(self.line_y)

                for i in range(len(self.FIGURES_LIST)):
                    self.result.append([round(self._space.shapes[4 + i].area),
                                        (str(self._space.shapes[4 + i]).split('.')[2]).split(' ')[0],
                                        self.FIGURES_LIST[i][2],
                                        self._space.shapes[4 + i].body.position,
                                        self._space.shapes[4 + i].body.angle])

                    if self.interface:
                        pic = self._screen.copy()

                        area = (HEIGHT - self.result[0]) * LENGTH
                        used_area = 0
                        for j in range(len(self.FIGURES_LIST)):
                            used_area += self._space.shapes[4 + j].area

                        percent = round(used_area / area * 100)

                        if percent > 75:
                            pygame.image.save(pic, f"BestScreens/Screen_80.png")
                            print(percent)
                        if percent > 76:
                            pygame.image.save(pic, f"BestScreens/Screen_81.png")
                            print(percent)
                        if percent > 77:
                            pygame.image.save(pic, f"BestScreens/Screen_82.png")
                            print(percent)
                        if percent > 78:
                            pygame.image.save(pic, f"BestScreens/Screen_83.png")
                            print(percent)
                        if percent > 79:
                            pygame.image.save(pic, f"BestScreens/Screen_84.png")
                            print(percent)
                        if percent > 80:
                            pygame.image.save(pic, f"BestScreens/Screen_85.png")
                            print(percent)

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
                    self._running = False
                    return self.result
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


def run_emulations(interface=False, figure_list=None, count_of_iterations=1, position_x=None):
    """
    This function insert lists of figures and it's positions and print max height of every iteration.\n
    :param interface: ON/OFF visual interface.
    :param figure_list: List of your figures. Insert list: [[size (polygon), type],...].
    :param count_of_iterations: Count of iterations.
    :param position_x: Positions of your figures. Insert list: [[pos1_figure1, pos1_figure2, ...], ..., [posx_figure1, posx_figure2, ...]].
    :return: max_height.
    """

    if position_x is None:
        position_x = []
    if figure_list is None:
        figure_list = []
    game = Emulator(interface=interface, FIGURES_LIST=figure_list, COUNT_OPERATIONS_DEBUG=count_of_iterations,
                    position_x=position_x)
    return game.run()


def create_permutations(figures_list):
    figures_list = itertools.permutations(figures_list)
    figures_list = ([list(row) for row in figures_list])

    for i in range(len(figures_list)):
        figures_list[i] = str(figures_list[i])

    figures_list = list(set(figures_list))

    for i in range(len(figures_list)):
        figures_list[i] = ast.literal_eval(figures_list[i])
    return figures_list


def create_experiments_data_for_dataframe(figures_list):
    """
    This function do experiments with all combination and return list with results
    :param figures_list: list of figures for experiments
    :return: list with results
    """

    res_list = create_permutations(figures_list)
    data_to_df = []
    iterator = Iterator(len(res_list))

    for item in res_list:
        iterator.increase()
        iterator_res = iterator.check_percent()
        if iterator_res is not None:
            print("Complete: " + str(iterator_res) + "%")
        item = ([list(row) for row in item])
        data_to_df.append(run_emulations(figure_list=item, count_of_iterations=1, interface=False))

    # print(len(data_to_df))
    return data_to_df


def create_csv_of_experiment(figures_list, path: str):
    """
    Create csv file with results of experiments
    :param path: path to saving csv file
    :param figures_list: list of figures for experiments
    :return: None
    """
    data = create_experiments_data_for_dataframe(figures_list)
    columns_for_df = ['Min height']

    for i in range(len(figures_list)):
        columns_for_df.append(f"s{i}")

    df = pd.DataFrame(data, columns=columns_for_df)
    df.to_csv(path, index=False, header=True)


def find_usage_percent(screen_length, screen_height, experiment_height, figures_area):
    """
    :param screen_length: Length of screen
    :param screen_height: Height of screen
    :param experiment_height: Height of experiment
    :param figures_area: All area of figures
    :return: percent of usage area
    """
    return figures_area / ((screen_length - experiment_height) * screen_height) * 100


# Use in production:
def get_best_position(figures_list, max_time=np.inf):
    """
    Do experiments with time limit and return results
    :param figures_list: list of figures
    :param max_time: max time of function execution
    :return: results of experiment (position and angle)
    """
    # timer
    start_timer = timeit.default_timer()
    end_timer = timeit.default_timer()

    # permutations
    res_list = create_permutations(figures_list)

    # variables
    max_res = 0
    positions_max_res = []
    iterator_for_list = Iterator()
    iterator_for_percents = Iterator(list_length=len(res_list))

    # list for graph (iterator count, percent)
    graph_param = []

    shape_area = 0
    result = run_emulations(figure_list=res_list[0], count_of_iterations=1, interface=False)
    for i in range(1, len(result)):
        shape_area += result[i][0]

    # time checker
    while (max_time > (end_timer - start_timer)) and (iterator_for_list.get_position() < len(res_list)):
        iterator_for_percents.increase()
        iterator_res = iterator_for_percents.check_percent()

        if iterator_res is not None:
            print("Complete permutations: " + str(iterator_res) + "%")

        result = run_emulations(figure_list=res_list[iterator_for_list.get_position()], count_of_iterations=1, interface=False)
        experiment_height = result[0]

        # for graph
        percent = find_usage_percent(LENGTH, HEIGHT, experiment_height, shape_area)
        if percent > 76:
            graph_param.append([iterator_for_list.get_position(), percent])

        if max_res < experiment_height:
            max_res = experiment_height
            positions_max_res = result
        end_timer = timeit.default_timer()
        iterator_for_list.increase()


    for i in range(1, len(result)):
        item = [positions_max_res[i][2], positions_max_res[i][3], positions_max_res[i][4]]
        positions_max_res[i] = item
    positions_max_res.pop(0)
    percent = find_usage_percent(LENGTH, HEIGHT, max_res, shape_area)

    return percent, positions_max_res, graph_param


# RunEmulations(interface=False, FIGURES_LIST=FIGURES_LIST, COUNT_OPERATIONS_DEBUG=100, position_x=[])
'''
[[100,100,100,100,100,100,100,100,100,100], [400,400,400,400,400,400,400,400,400,400]]
'''
