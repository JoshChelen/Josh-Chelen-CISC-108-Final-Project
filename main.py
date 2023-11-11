from dataclasses import dataclass
from designer import *
import random

MOVESPEED = 10

@dataclass
class World:
    worm:DesignerObject
    wormSize:float
    fruits:list[DesignerObject]



def create_worm() -> DesignerObject:
    """ Create the worm """
    worm = emoji("🐛")
    worm.y = get_height() * (4 / 5)
    worm.flip_x = True
    return worm




def create_fruit()->DesignerObject:
    fruitList = ["🍇","🍐","🫐","🥭"]
    fruit = emoji(fruitList[random.randint(0, len(fruitList)-1)])
    fruit.y = get_height() * (4 / 5)
    fruit.x = random.randint(get_width()*0.4,get_width()*0.6)
    return fruit

def make_fruits(world:World):
    world.fruits.append(create_fruit())

#Start Movement Functions
def move(world:World,key:str):
    """takes input and calls movement functions"""
    if key == "left":
        move_left(world)
    elif key == "right":
        move_right(world)

def move_left(world:World):
    """moves worm left"""
    world.worm.x -= MOVESPEED
    world.worm.flip_x = False
def move_right(world:World):
    """moves worm right"""
    world.worm.x += MOVESPEED
    world.worm.flip_x = True

def bounce_worm(world: World):
    """Flips the worm to the opposite direction if it goes off screen"""
    if world.worm.x > get_width():
        move_left(world)
    elif world.worm.x < 0:
        move_right(world)
#End Movement Functions


#Start Worm Eating Functions

def eat_fruit(world:World,key:str):
    if key == "space":
        for fruit in world.fruits:
            if colliding(world.worm,fruit):
                world.fruits.remove(fruit)
                destroy(fruit)





#End Worm Eating Functions



def create_world() -> World:
    """ Create the world """
    return World(create_worm(),1.0,[create_fruit()])


when('starting', create_world)
when('typing',move)
when('updating',bounce_worm)
when('typing',eat_fruit)
start()