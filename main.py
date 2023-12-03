from dataclasses import dataclass
from designer import *
import random


@dataclass
class ToxicSpit:
    toxicSpitObject:DesignerObject
    direction:int
    speed:float

@dataclass
class Enemy:
    enemyObject:ToxicSpit
    isParalyzed:bool

@dataclass
class World:
    worm:DesignerObject
    wormSize:float
    wormCanMoveLeft: bool
    wormCanMoveRight: bool
    wormHealth: int
    wormMovementSpeed: int
    isWormDead: bool


    isGameComplete:bool
    counter:DesignerObject
    wormHealthText:DesignerObject

    waveNumber:int
    waveFruits:[list[DesignerObject]]
    waveEnemies:[list[Enemy]]

    spitList: list[ToxicSpit]
    controlsText:DesignerObject




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

def create_enemy(enemyEmoji:str,speed:float)->Enemy:
    """creates an enemy on either sided of the screen with a certain emoji and speed"""
    beetle = emoji(enemyEmoji)
    beetle.y = get_height() * (4 / 5)
    side = random.randint(0,1)
    direction = 1
    if side == 0:
        beetle.x = 0
        direction = 1
    elif side == 1:
        beetle.x = get_width()

        direction = -1
    return Enemy(ToxicSpit(beetle,direction,speed),False)

def move_enemies(world:World):
    """
    moves the enemies across the screen
    if the enemies collide with the player, they take damage and the enemies despawn
    """
    for enemy in world.waveEnemies:
        enemy.enemyObject.toxicSpitObject.x += enemy.enemyObject.speed*enemy.enemyObject.direction
        if enemy.enemyObject.toxicSpitObject.x > get_width() or enemy.enemyObject.toxicSpitObject.x < 0:
            enemy.enemyObject.direction *= -1
        if colliding(world.worm, enemy.enemyObject.toxicSpitObject) and (not enemy.isParalyzed):
            world.wormHealth-=1
            world.waveEnemies.remove(enemy)
            destroy(enemy.enemyObject.toxicSpitObject)






#End Enemy Functions

#Start Movement Functions
def worm_movement_pressed(world:World,key:str):
    """takes input and calls movement functions"""
    if key == "left":
        world.wormCanMoveLeft = True
        worm_move_left(world)
    elif key == "right":
        world.wormCanMoveRight =True
    elif key == "q":
        worm_take_damage(world)

def worm_movement_released(world:World,key:str):
    """
    stops player movement once the arrow keys are released
    """
    if key == "left":
        world.wormCanMoveLeft = False
        worm_move_left(world)
    elif key == "right":
        world.wormCanMoveRight = False

def worm_move(world:World):
    """
    moves the worm when the conditions are met
    """

    if world.wormCanMoveLeft:
        worm_move_left(world)
    elif world.wormCanMoveRight:
        worm_move_right(world)
def worm_move_left(world:World):
    """moves worm left"""
    world.worm.x -= world.wormMovementSpeed
    world.worm.flip_x = False
def worm_move_right(world:World):
    """moves worm right"""
    world.worm.x += world.wormMovementSpeed
    world.worm.flip_x = True

def worm_bounce(world: World):
    """Flips the worm to the opposite direction if it goes off-screen"""
    if world.worm.x > get_width():
        worm_move_left(world)
    elif world.worm.x < 0:
        worm_move_right(world)
#End Movement Functions

#Start Worm Health/Dying Functions

def worm_health_text(world:World):
    """Displays the health of the worm. It also will kill the worm if the health drops below 3"""
    if world.wormHealth == 3:
        world.wormHealthText.text = "Health: 3"
    elif world.wormHealth == 2:
        world.wormHealthText.text = "Health: 2"
    elif world.wormHealth == 1:
        world.wormHealthText.text = "Health: 1"
    elif world.wormHealth <= 0:

        world.wormHealthText.text = "You Died! Game Over"
        world.worm.name = "💀"
        world.isWormDead = True
def worm_take_damage(world:World):
    """Makes the worm's health reduce by 1"""
    world.wormHealth = world.wormHealth-1

def worm_get_healed(world:World):
    """Makes the worm's health increase by 1"""
    if world.wormHealth < 3:
        world.wormHealth = world.wormHealth + 1
def worm_dead_check(world:World)->bool:
    """returns True if the worm is dead"""
    return world.isWormDead

#End Worm Health/Dying Functions


#Start Worm Ability Functions

def ability_eat_enemy(world:World):
    """allows the worm to eat objects"""
    for fruit in world.waveFruits:
        if colliding(world.worm,fruit):
            world.waveFruits.remove(fruit)
            destroy(fruit)
            world.worm.scale += 0.05
            world.wormMovementSpeed += 0.05
    for enemy in world.waveEnemies:
        print(world.waveEnemies)
        if colliding(world.worm,enemy.enemyObject.toxicSpitObject):
            world.waveEnemies.remove(enemy)
            destroy(enemy.enemyObject.toxicSpitObject)
            world.worm.scale += 0.2
            world.wormMovementSpeed += 0.3


def ability_create_toxic_spit(world:World)->ToxicSpit:
    """creates a fruit with a random fruit emoji"""
    toxicSpitObject = emoji("💧")
    toxicSpitObject.x = world.worm.x
    toxicSpitObject.y = world.worm.y
    direction = -1
    if world.worm.flip_x:
        direction = 1
    speed=10.0

    return ToxicSpit(toxicSpitObject,direction,speed)
def ability_toxic_spit_movement(world:World):
    """
    moves the toxic spit across the screen and deletes it if it goes off-screen
    also handles collision with enemies
    """
    for spit in world.spitList:
        if spit.toxicSpitObject.x > get_width() or spit.toxicSpitObject.x < 0:
            world.spitList.remove(spit)
            destroy(spit.toxicSpitObject)
        else:
            spit.toxicSpitObject.x += spit.speed*spit.direction
        for enemy in world.waveEnemies:
            if colliding(enemy.enemyObject.toxicSpitObject,spit.toxicSpitObject) and (not enemy.isParalyzed):
                enemy.isParalyzed = True
                enemy.enemyObject.speed = 0
                world.spitList.remove(spit)
                destroy(spit.toxicSpitObject)

def ability_mouse_inputs(world:World, x:int, y:int, button:str):
    """
    handles inputs related to the left and right mouse buttons
    left = eat
    right = spit
    """
    if button == "left":
        ability_eat_enemy(world)
    elif button == "right":
        world.spitList.append(ability_create_toxic_spit(world))

#End Worm Ability Functions

#Start Wave/Level Functions
def wave_update(world:World):
    """
    calls the function that spawns the next wave once
    all the enemies in a given wave are defeated
    """
    if len(world.waveFruits)<=0 and len(world.waveEnemies)<=0:
        world.waveNumber += 1
        world.worm.x = get_width()/2
        if world.wormHealth < 3:
            world.wormHealth+=1
        wave_spawn(world)
def wave_spawn(world:World):
    """
    spawns different enemies based on waveNumber
    """
    #wave 0 spawned when starting game
    if world.waveNumber == 1:
        world.waveFruits = make_fruits(world, 2)
    elif world.waveNumber == 2:
        world.waveFruits = make_fruits(world, 3)
        world.waveEnemies.append(create_enemy("🐌", 1.0))
    elif world.waveNumber == 3:
        world.waveFruits = make_fruits(world, 2)
        world.waveEnemies.append(create_enemy("🐌", 1.2))
        world.waveEnemies.append(create_enemy("🐌", 0.8))
        world.waveEnemies.append(create_enemy("🪲", 3.0))
    elif world.waveNumber == 4:
        world.waveFruits = make_fruits(world, 5)
        world.waveEnemies.append(create_enemy("🐞", 8.0))
        world.waveEnemies.append(create_enemy("🪲", 4.2))
        world.waveEnemies.append(create_enemy("🪲", 3.0))
    elif world.waveNumber == 5:
        world.waveFruits = make_fruits(world, 6)
        world.waveEnemies.append(create_enemy("🐞", 8.0))
        world.waveEnemies.append(create_enemy("🪲", 4.2))
        world.waveEnemies.append(create_enemy("🪲", 3.0))
        world.waveEnemies.append(create_enemy("🐌", 1.2))
        world.waveEnemies.append(create_enemy("🐌", 0.8))
    elif world.waveNumber == 6:
        world.waveEnemies.append(create_enemy("🐞", 8.0))
        world.waveEnemies.append(create_enemy("🐞", 5.2))
        world.waveEnemies.append(create_enemy("🐞", 6.0))
        world.waveEnemies.append(create_enemy("🪲", 4.2))
        world.waveEnemies.append(create_enemy("🪲", 4.8))
        world.waveFruits = make_fruits(world, 7)
    elif world.waveNumber == 7:
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
    return World(create_worm(),
                 1.0,
                 False,
                 False,
                 3,
                 3,
                 False,
                 False,
                 text("black", "game", 50,get_width()/2-200, 50),
                 text("black", "Health: 3", 50,get_width()/2+200, 50),
                 0,
                 [create_fruit()],
                 [],
                 [],
                 text("black","Left Click: Eat | Right Click: Toxic Spit | Arrow Keys: Movement", 35, get_width()/2,150))


when('starting', create_world)

#worm movement events
when('typing',worm_movement_pressed)
when('done typing', worm_movement_released)
when('updating', worm_move)
when('updating',worm_bounce)

#worm ability events
when('clicking',ability_mouse_inputs)


#text overlay events
when('updating',wave_text)
when('updating',worm_health_text)

#miscellaneous events
when('updating',wave_update)
when(worm_dead_check,pause)
when('updating',ability_toxic_spit_movement)
when('updating',move_enemies)
start()


