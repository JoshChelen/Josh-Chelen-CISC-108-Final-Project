from dataclasses import dataclass
from designer import *
import random

MOVESPEED = 10

@dataclass
class World:
    worm:DesignerObject
    isGameComplete:bool
    wormSize:float
    counter:DesignerObject
    waveNumber:int
    waveEnemies:[list[DesignerObject]]


def create_worm() -> DesignerObject:
    """ Create the worm """
    worm = emoji("🐛")
    worm.y = get_height() * (4 / 5)
    worm.flip_x = True
    return worm



#Start Enemy Functions
def create_fruit()->DesignerObject:
    """creates a fruit with a random fruit emoji"""
    fruitList = ["🍇","🍐","🫐","🥭"]
    fruit = emoji(fruitList[random.randint(0, len(fruitList)-1)])
    fruit.y = get_height() * (4 / 5)
    fruit.x = random.randint(get_width()*0.4,get_width()*0.6)
    return fruit

def make_fruits(world:World,fruitCount:int)->[DesignerObject]:
    """returns a list of fruits with a length of fruitCount"""
    fruits = []
    for num in range(fruitCount):
        fruits.append(create_fruit())
    return fruits
#End Enemy Functions

#Start Movement Functions
def worm_move(world:World,key:str):
    """takes input and calls movement functions"""
    if key == "left":
        worm_move_left(world)
    elif key == "right":
        worm_move_right(world)

def worm_move_left(world:World):
    """moves worm left"""
    world.worm.x -= MOVESPEED
    world.worm.flip_x = False
def worm_move_right(world:World):
    """moves worm right"""
    world.worm.x += MOVESPEED
    world.worm.flip_x = True

def worm_bounce(world: World):
    """Flips the worm to the opposite direction if it goes off screen"""
    if world.worm.x > get_width():
        worm_move_left(world)
    elif world.worm.x < 0:
        worm_move_right(world)
#End Movement Functions


#Start Worm Ability Functions

def ability_eat_enemy(world:World,key:str):
    """allows the worm to eat objects"""
    if key == "space":
        for enemy in world.waveEnemies:
            if colliding(world.worm,enemy):
                world.waveEnemies.remove(enemy)
                destroy(enemy)
                world.worm.scale += 0.1

#End Worm Ability Functions

#Start Wave/Level Functions
def wave_update(world:World):
    """
    calls the function that spawns the next wave once
    all the enemies in a given wave are defeted
    """
    if len(world.waveEnemies)<=0:
        world.waveNumber += 1
        wave_spawn(world)
def wave_spawn(world:World):
    """
    spawns different enemies based on waveNumber
    """

    #wave 0 spawned when starting game
    if world.waveNumber == 1:
        world.waveEnemies = make_fruits(world,2)
    elif world.waveNumber == 2:
        world.waveEnemies = make_fruits(world, 3)
    elif world.waveNumber == 3:
        world.waveEnemies = make_fruits(world, 4)
    elif world.waveNumber == 4:
        world.waveEnemies = make_fruits(world, 5)
    elif world.waveNumber == 5:
        world.waveEnemies = make_fruits(world, 6)
    elif world.waveNumber == 6:
        world.waveEnemies = make_fruits(world, 7)
    elif world.waveNumber == 7:
        world.waveEnemies = make_fruits(world, 8)
    elif world.waveNumber == 8:
        world.waveEnemies = make_fruits(world, 9)
    elif world.waveNumber == 9:
        world.isGameComplete=True

def wave_text(world:World):
    """updates the text on the top of the screen"""
    if world.isGameComplete:
        world.counter.text = "All waves complete! You win"
    else:
        world.counter.text = "Current Wave: "+str(world.waveNumber+1)
#End Wave/Level Functions


def create_world() -> World:
    """ Create the world """
    return World(create_worm(),False,1.0,text("black", "game", 50,get_width()/2, 50),0,[create_fruit()])


when('starting', create_world)

when('typing',worm_move)
when('updating',worm_bounce)

when('typing',ability_eat_enemy)

when('updating',wave_text)
when('updating',wave_update)

start()