# 이것은 각 상태들을 객체로 구현한 것임.

from pico2d import get_time, load_image, SDL_KEYDOWN, SDL_KEYUP, SDLK_SPACE, SDLK_LEFT, SDLK_RIGHT, load_font
from state_machine import *
from ball import Ball
import game_world
import game_framework

def touch_wall(bird):
    return bird.x > 1600 or bird.x < 0

class Fly:
    @staticmethod
    def enter(bird, e):
        bird.frame = 0
        bird.dir = 1
        bird.action = 2
        pass

    @staticmethod
    def exit(bird, e):
        pass

    @staticmethod
    def do(bird):
        TIME_PER_ACTION = 0.2
        ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
        FRAMES_PER_ACTION = 5

        bird.frame = (bird.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % 5

        if (bird.action == 2 or bird.action == 1) and int(bird.frame) == 4:
            bird.action -= 1
            bird.frame = 0
        elif bird.action == 0 and int(bird.frame) == 3:
            bird.action = 2
            bird.frame = 0

        PIXEL_PER_METER = (10.0 / 0.2)
        RUN_SPEED_KMPH = 20.0
        RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
        RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
        RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

        bird.x += bird.dir * RUN_SPEED_PPS * game_framework.frame_time

        if touch_wall(bird): bird.dir *= -1

    @staticmethod
    def draw(bird):
        if bird.dir == 1:
            bird.image.clip_composite_draw(int(bird.frame) * 183, bird.action * 168, 183, 168, 0, '', bird.x, bird.y, 90, 80)
        elif bird.dir == -1:
            bird.image.clip_composite_draw(int(bird.frame) * 183, bird.action * 168, 183, 168, 0, 'h', bird.x, bird.y, 90, 80)

class Bird:
    image = None
    def __init__(self, x):
        self.x, self.y = x, 500
        if self.image == None:
            self.image = load_image('bird_animation.png')
        self.state_machine = StateMachine(self)
        self.state_machine.start(Fly)
        self.state_machine.set_transitions(
            {
                Fly: {}
            }
        )
        
    def update(self):
        self.state_machine.update()

    def draw(self):
        self.state_machine.draw()