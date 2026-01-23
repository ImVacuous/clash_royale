import os
import pygame
import random
from pathfinding.core.diagonal_movement import DiagonalMovement
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from src.arena import arena_map
import src.animation as animation
import pyganim
import src.sounds as sounds

TILE_SIZE = 27

#gets directories of images
BASE_DIR = os.path.dirname(os.path.abspath(__file__)) 
IMG_DIR = os.path.join(BASE_DIR, "pictures") 
ANI_DIR_TOWER_R = os.path.join(BASE_DIR, 'towers') 
DIR_MENU_LOADING = os.path.join(IMG_DIR, "Loading.jpg")
DIR_MENU_LOGO = os.path.join(IMG_DIR, "Logo.jpg")
DIR_WON = os.path.join(IMG_DIR, "gamewon.png")
DIR_LOSS = os.path.join(IMG_DIR, "gameloss.png")
DIR_TIED = os.path.join(IMG_DIR, "gametied.png")
DIR_FONT = os.path.join(IMG_DIR, "font.otf")
DIR_EMOTE_ONE = os.path.join(IMG_DIR, "emoteone.png")



class Troop:
    # initializes troop logic variables
    def __init__(self, hp, speed, damage, range, attack_range, attack_cooldown, e_cost, x, y, card_png, card_animation, is_friendly, special_ability=False):
        self.hp = hp
        self.speed = speed
        self.damage = damage
        self.range = range
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.e_cost = e_cost
        self.x = x
        self.y = y
        self.pos = pygame.Vector2(self.x, self.y)
        self.card_png = card_png
        self.card_animation = card_animation
        self.is_friendly = is_friendly
        self.special_ability = special_ability
        self.last_attack_time = 0
    
    #initializes the pathfinding module
    def pathfinding(self, start_x, start_y, end_x, end_y):
        '''
        Uses the pathfinding library to find the path that a troop should take to get to its destination, which includes obstacles.
        
        Pre-conditions:
        start_x; int - must be a valid x coordinate in arena map
        start_y; int - must be a valid y coordinate in arena map
        end_x; int - must be a valid x coordinate in arena map
        end_y; int - must be a valid y coordinate in arena map

        Parameters:
        start_x; starting x position
        start_y; starting y position
        end_x; ending x position
        end_y; ending y position

        Returns:
        list of tuples; returns a list of tuples that act as the next tile for the troop to move to
        '''
        grid = Grid(matrix=arena_map) #sets the grid to search as the arena_map
        start = grid.node(start_x, start_y) #finds the start node
        end = grid.node(end_x, end_y) #finds the end node
        finder = AStarFinder(diagonal_movement=DiagonalMovement.only_when_no_obstacle) #initializes the A* pathfinding algorithm
        path = finder.find_path(start, end, grid)[0] #uses the A* pathfinding algorithm to get the path
        return path # returned as a list of tuples
        
    # determines if an enemy is in range of a troop
    def attack_radius(self, card, placed_card):
        '''
        inflates a troops hitbox to find any potential enemies in range. If there is, and they are not on the same team, then return the enemy being appended to enemy_list.

        Pre-conditions:
        card; class instance
        placed_card; list

        Parameters:
        card; any troop that has been placed on the arena map
        placed_card; a list that contains all active troops on the arena map

        Returns:
        list, returns a list of all enemies in range, if there isn't any, it returns None
        '''
        enemy_list = [] #initializes an empty list that contains all enemies in range
        radius = self.character_rect(card).inflate(self.range, self.range) #inflates the troops original rect to act as the radius
        for enemy in placed_card: #for all troops on the arena
            if enemy.is_friendly != self.is_friendly: #if the troop is not friendly
                if radius.colliderect(enemy.character_rect(enemy)): #checks if the radius hits the enemy's hitbox
                    enemy_list.append(enemy)
                    return enemy_list #returns a list of all enemies in range
        return None
    
    
    #Allows troops to attack each other
    def attack(self, card, all_cards):
        '''
        Allows a troop to attack by first seeing if there are any troops in range, then moving towards them if there is. 
        Once they hit the troop's attack range, they will start taking damage.
        
        Pre-conditions:
        card; class instance
        all_cards; list

        Parameters:
        card; The troop that is doing the attacking, used to inflate its hitbox
        all_cards; a list that contains all troops currently placed

        Returns:
        Boolean; returns True if troop is attacking and False if the troop isn't attacking
        '''
        attack_range = self.character_rect(card).inflate(self.attack_range, self.attack_range) #inflates the troops original rect to act as the attack range
        enemy = self.attack_radius(card, all_cards) #Gets all enemies
        if enemy == None:   #if no enemy is found
            return False
        else:
            enemy = enemy[0] #gets the first enemy
            if enemy:
                if not attack_range.colliderect(enemy.character_rect(card)): #if not in attack range
                    self.x, self.y = self.move(self.x, self.y, int(enemy.x) // TILE_SIZE, int(enemy.y) // TILE_SIZE) #moves towards enemy
                self.pos = pygame.Vector2(enemy.x - self.x, enemy.y - self.y) #gets x and y distance to calculate the angle
                if attack_range.colliderect(enemy.character_rect(card)): #if in attack range
                    print(f'enemy: {enemy}, self: {self}')
                    if pygame.time.get_ticks() // 1000 - self.last_attack_time >= self.attack_cooldown: #checks if the troop's cooldown is over
                        enemy.take_damage(self.damage, enemy) # enemy takes damage
                        self.attack_play_sound(card) #attack sound
                        self.last_attack_time = pygame.time.get_ticks() // 1000 #resets cooldown
                    return True
        return False

    #allows troops to move
    def move(self, pos_x, pos_y, dest_x, dest_y):
        '''
        This function moves troops using the pathfinding as a helper function based on their current x,y and end x,y. 
        Returning their x and y once it reaches its destination.
        
        Pre-conditions:
        pos_x; int - must be a valid x coordinate in arena map
        pos_y; int - must be a valid y coordinate in arena map
        dest_x; int - must be a valid x coordinate in arena map
        dest_y; int - must be a valid y coordinate in arena map

        Parameters:
        pos_x; the troop's current x position
        pos_y; the troop's current y position
        dest_x; the troop's target x position
        dest_y; the troop's target y position

        Returns:
        int, int (pos_x, pos_y); This is the troop's position after reaching its destination

        '''
        path = self.pathfinding(int(pos_x // TILE_SIZE), int(pos_y // TILE_SIZE), dest_x, dest_y) #gets the path that troops use to travel
        
        if len(path) <= 1: #if the troop is at its destination
            return pos_x, pos_y
        
        endpos_x, endpos_y = path[1] #gets the next tile coordinates, [0] is the current spot

        target_x = endpos_x * TILE_SIZE #converts the target x coordinate to pixels for smoother travel
        target_y = endpos_y * TILE_SIZE #converts the target y coordinate to pixels for smoother travel
        
        if pos_x < target_x: #moving right
            pos_x += self.speed
            if pos_x > target_x: #if the character overshoots
                pos_x = target_x 

        elif pos_x > target_x: # moving left
            pos_x -= self.speed
            if pos_x < target_x: #if the character overshoots
                pos_x = target_x

        if pos_y < target_y: # moving down
            pos_y += self.speed
            if pos_y > target_y: #if the character overshoots
                pos_y = target_y

        elif pos_y > target_y: # moving up
            pos_y -= self.speed
            if pos_y < target_y: #if the character overshoots
                pos_y = target_y

        self.pos = pygame.Vector2(target_x - pos_x, target_y - pos_y) #gets x and y distance to calculate the angle

        
        return pos_x, pos_y #returns troop position

    #makes characters die
    def die(self, card):

        if card.is_friendly == True: #if card is from the player
            if card in placed_card: #checks if it hasn't already died
                placed_card.remove(card) #removes troop
        if card.is_friendly == False: #if card is from enemy
            if card in enemy_placed: #checks if it hasn't already died
                enemy_placed.remove(card) #removes enemy
        
        #stops playing sounds after death
        if isinstance(card, Knight):
            sounds.knight_attack.stop() 
        elif isinstance(card, The_Guy):
            sounds.golem_attack.stop() 
        elif isinstance(card, Archers):
            sounds.archer_attack.stop() 
        elif isinstance(card, Giant):
            sounds.giant_attack.stop() 
        elif isinstance(card, Cannon):
            sounds.cannon_attack.stop() 
        elif isinstance(card, Xbow):
            sounds.xbow_attack.stop() 

    #allows troops to take damage
    def take_damage(self, damage, card):
        self.hp -= damage #subtracts troop's health from incoming damage
        if self.hp <= 0: #if troop dies
            self.die(card) #remove from list

    #loads and scales the card pngs for the deck
    def image_pathing(self):
        image = pygame.image.load(self.card_png).convert_alpha() # loads image and smoothens edges
        scaled_image = pygame.transform.scale(image, (108, 142)) #scales image to certain pixels
        return scaled_image
    
    #gets the angle the troop is facing
    def get_direction(self):
        angle = self.pos.as_polar()[1] % 360 #gets the polar angle then converts to degrees
        if 45 <= angle < 135: #facing south
            return 'S'
        elif 135 <= angle < 225: #facing west
            return 'W'
        elif 225 <= angle < 315: #facing north
            return 'N'
        else:
            return 'E' #facing east

    #animates the cards
    def animation(self, card):
        direction = self.get_direction() #gets the angle they're facing
        card_ani = None
        if isinstance(card, Knight):
            card_ani = card_animation_list[0] #if card is knight
        elif isinstance(card, The_Guy):
            card_ani = card_animation_list[1] #if card is him
        elif isinstance(card, Archers):
            card_ani = card_animation_list[2] #if card is archers
        elif isinstance(card, Giant):
            card_ani = card_animation_list[3] #if card is giant
        elif isinstance(card, Cannon):
            card_ani = card_animation_list[4] #if card is cannon
        elif isinstance(card, Xbow):
            card_ani = card_animation_list[5] #if card is xbow

        if direction == 'E':
            return card_ani[1] #animates card facing east
        elif direction == 'N':
            return card_ani[2] #animates card facing north
        elif direction == 'S':
            return card_ani[3] #animates card facing south
        elif direction == 'W':
            return card_ani[4] #animates card facing west
        
    #gets the troop's hitbox
    def character_rect(self, card):
        character_rect = self.animation(card).getCurrentFrame().get_rect(topleft=(self.x, self.y)) #gets the character's rectangle hitbox from their animation.
        return character_rect
    
    #plays attack sounds based on card
    def attack_play_sound(self, card):
        if isinstance(card, Knight):
            sounds.knight_attack.play() #knight attacking
        elif isinstance(card, The_Guy):
            sounds.golem_attack.play() # him attacking
        elif isinstance(card, Archers):
            sounds.archer_attack.play() #archers attacking
        elif isinstance(card, Giant):
            sounds.giant_attack.play() #giant attacking
        elif isinstance(card, Cannon):
            sounds.cannon_attack.play() #cannon attacking
        elif isinstance(card, Xbow):
            sounds.xbow_attack.play() #xbow attacking
    
    #plays spawn sounds based on card
    def spawn_play_sound(self, card):
        if isinstance(card, Knight):
            sounds.knight_spawn.play() #knight spawn
        elif isinstance(card, The_Guy):
            sounds.golem_spawn.play() #him spawn
        elif isinstance(card, Archers):
            sounds.archer_spawn.play() #archers spawn
        elif isinstance(card, Giant):
            sounds.giant_spawn.play() #giant spawn
        elif isinstance(card, Cannon):
            sounds.cannon_spawn.play() #cannon spawn
        elif isinstance(card, Xbow):
            sounds.xbow_spawn.play() #xbow spawn
        



#Regular troops
class Knight(Troop):
    def __init__(self, hp=1766, speed=2, damage=202, range=100, attack_range=100, attack_cooldown=1, e_cost=3, x=0, y=0, card_png=os.path.join(IMG_DIR, "knight.png"), card_animation=None, is_friendly=None, special_ability=False):
        super().__init__(hp, speed, damage, range, attack_range, attack_cooldown, e_cost, x, y, card_png, card_animation, is_friendly, special_ability)

class Archers(Troop):
    def __init__(self, hp=304, speed=1.5, damage=112 , range=100 , attack_range=100 , attack_cooldown=1.5, e_cost=3, x=0 , y=0 , card_png=os.path.join(IMG_DIR, "Archers.png"), card_animation=None , is_friendly=None, special_ability=False):
        super().__init__(hp, speed, damage, range, attack_range, attack_cooldown, e_cost, x, y, card_png, card_animation, is_friendly, special_ability)

# Tank class (only target buildings/towers)
class Tank(Troop):
    # initializes tank logic variables
    def __init__(self, hp, speed, damage, range, attack_range, attack_cooldown, e_cost, x, y, card_png, card_animation, is_friendly, special_ability=False):
        super().__init__(hp, speed, damage, range, attack_range, attack_cooldown, e_cost, x, y, card_png, card_animation, is_friendly, special_ability)
    
    #same attack function as troops, but only targets buildings and towers
    def attack(self, card, all_cards):
        attack_range = self.character_rect(card).inflate(self.attack_range, self.attack_range)
        enemy = self.attack_radius(card, all_cards)
        
        if enemy == None:
            return False
        else:
            enemy = enemy[0]
            if enemy:
                if isinstance(enemy, Buildings) or isinstance(enemy, Towers): #if enemy is a building or tower
                    if not attack_range.colliderect(enemy.character_rect(card)):
                        self.x, self.y = self.move(self.x, self.y, int(enemy.x) // TILE_SIZE, int(enemy.y) // TILE_SIZE)
                    self.pos = pygame.Vector2(enemy.x - self.x, enemy.y - self.y)
                    if attack_range.colliderect(enemy.character_rect(card)):
                        print(f'enemy: {enemy}, self: {self}')
                        if pygame.time.get_ticks() // 1000 - self.last_attack_time >= self.attack_cooldown:
                            enemy.take_damage(self.damage, enemy)
                            self.attack_play_sound(card)
                            self.last_attack_time = pygame.time.get_ticks() // 1000
                    return True
        return False

class Giant(Tank):
    def __init__(self, hp=4090, speed=1, damage=153, range=100, attack_range=100, attack_cooldown=1.5, e_cost=5, x=0, y=0, card_png=os.path.join(IMG_DIR, "Giant.png"), card_animation=None, is_friendly=None, special_ability=False):
        super().__init__(hp, speed, damage, range, attack_range, attack_cooldown, e_cost, x, y, card_png, card_animation, is_friendly, special_ability)

class The_Guy(Tank):
    def __init__(self, hp=5120, speed=1, damage=312, range=100, attack_range=100, attack_cooldown=1.5, e_cost=8, x=0, y=0, card_png=os.path.join(IMG_DIR, "Golem.png"), card_animation=None, is_friendly=None, special_ability=False):
        super().__init__(hp, speed, damage, range, attack_range, attack_cooldown, e_cost , x , y , card_png , card_animation , is_friendly , special_ability)

# Buildings
class Buildings(Troop):
    def __init__(self, hp, speed, damage, range, attack_range, attack_cooldown, e_cost, x, y, card_png, card_animation, is_friendly, health_decay, special_ability=False):
        super().__init__(hp, speed, damage, range, attack_range, attack_cooldown, e_cost, x, y, card_png, card_animation, is_friendly, special_ability)
        self.health_decay = health_decay

    def decay(self):
        self.hp -= self.health_decay


class Cannon(Buildings):
    def __init__(self, hp=824, speed=0, damage=212, range=50, attack_range=25, attack_cooldown=1, e_cost=3, x=0, y=0, card_png=os.path.join(IMG_DIR, "Cannon.png"), card_animation=None, is_friendly=None, health_decay=25, special_ability=False):
        super().__init__(hp, speed, damage, range, attack_range, attack_cooldown, e_cost, x, y, card_png, card_animation, is_friendly, health_decay, special_ability)

class Xbow(Buildings):
    def __init__(self, hp=1600, speed=0, damage=43, range=100, attack_range=100, attack_cooldown=0.2, e_cost=6, x=0, y=0, card_png=os.path.join(IMG_DIR, "XBow.png"), card_animation=None, is_friendly=None, health_decay=53, special_ability=False):
        super().__init__(hp, speed, damage, range, attack_range, attack_cooldown, e_cost, x, y, card_png, card_animation, is_friendly, health_decay, special_ability)

# Towers
class Towers():
    # initializes tower logic variables
    def __init__(self, tower_type, hp, damage, range, attack_range, attack_cooldown, x, y, tower_animation, is_friendly):
        self.tower_type = tower_type
        self.hp = hp
        self.damage = damage
        self.range = range
        self.attack_range = attack_range
        self.attack_cooldown = attack_cooldown
        self.x = x * TILE_SIZE
        self.y = y * TILE_SIZE
        self.tower_animation = tower_animation
        self.is_friendly = is_friendly
        self.last_attack_time = 0
    
    #finds enemies in range
    def attack_radius(self, card, placed_card):
        enemy_list = []
        radius = self.character_rect(card).inflate(self.range, self.range)
        for enemy in placed_card:
            if enemy.is_friendly != self.is_friendly:
                if radius.colliderect(enemy.character_rect(enemy)):
                    enemy_list.append(enemy)
                    return enemy_list
        return None

    #allows towers to attack
    def attack(self, card, all_card):
        attack_range = self.character_rect(card).inflate(self.attack_range, self.attack_range)
        enemy = self.attack_radius(card, all_card)
        
        if enemy == None:
            return False
        else:
            enemy = enemy[0]
            if enemy:
                if attack_range.colliderect(enemy.character_rect(enemy)):
                    if pygame.time.get_ticks() // 1000 - self.last_attack_time >= self.attack_cooldown:
                        enemy.take_damage(self.damage, enemy)
                        self.last_attack_time = pygame.time.get_ticks() // 1000 
                    return True
        return False
    
    #makes towers die
    def die(self, card):
        if card in tower_deck: #if not already dead
            tower_deck.remove(card) #remove from list

    #allows towers to take damage
    def take_damage(self, damage, card):
        self.hp -= damage
        if self.hp <= 0:
            self.die(card)
    
    #loads tower png
    def animation(self, card=None):
        image = pygame.image.load(self.tower_animation)
        scaled_image = pygame.transform.scale(image, (80, 80))
        return scaled_image
    
    #creates tower's hitbox
    def character_rect(self, card):
        character_rect = self.animation(card).get_rect(topleft=(self.x, self.y))
        return character_rect

class Tower_Troop(Towers):
    def __init__(self, tower_type, hp, damage, range, attack_range, attack_cooldown, x, y, tower_animation, is_friendly):
        super().__init__(tower_type, hp, damage, range, attack_range, attack_cooldown, x=x, y=y, tower_animation=tower_animation, is_friendly=is_friendly)

    
class Crown_Tower(Towers):
    def __init__(self, tower_type, hp, damage, range, attack_range, attack_cooldown, x, y, tower_animation, is_friendly):
        super().__init__(tower_type, hp, damage, range, attack_range, attack_cooldown, x=x, y=y, tower_animation=tower_animation, is_friendly=is_friendly)

#Initializes tower instances
enemy_ptower_left = Tower_Troop("Enemy_Tower", 3056, 109, 100, 100, 1.5, 1, 3, os.path.join(IMG_DIR, "tower.jpg"), False)
enemy_ptower_right = Tower_Troop("Enemy_Tower", 3056, 109, 100, 100, 1.5, 14, 3, os.path.join(IMG_DIR, "tower.jpg"), False)
player_ptower_left = Tower_Troop("Player_Tower", 3056, 109, 100, 100, 1.5, 1, 18, os.path.join(IMG_DIR, "tower.jpg"), True)
player_ptower_right = Tower_Troop("Player_Tower", 3056, 109, 100, 100, 1.5, 14, 18, os.path.join(IMG_DIR, "tower.jpg"), True)
#crown tower setup
enemy_crown_tower = Crown_Tower("Enemy_Crown_Tower", 4824, 109, 100, 100, 1, 7.5, 1, os.path.join(IMG_DIR, "King_Tower_Red.jpg"), False)
player_crown_tower = Crown_Tower("Player_Crown_Tower", 4824, 109, 100, 100, 1.2, 7.5, 21, os.path.join(IMG_DIR, "King_Tower_Blue.jpg"), True)

deck = [Knight, Archers, Giant, The_Guy, Cannon, Xbow] #initializes player deck
enemy_deck = [Knight, Archers, Giant, The_Guy] #initializes enemy deck
placed_card = [] #list that contains all of the player's placed cards
enemy_placed = [] #lits that contains all of the enemy's placed cards
tower_deck = [enemy_ptower_left, enemy_ptower_right, enemy_crown_tower, player_ptower_left, player_ptower_right, player_crown_tower] #initializes all of the towers to the arena

#resets all of the towers back to their original state
def init_cards(tower_deck):
    #princess tower setup
    global enemy_crown_tower, enemy_ptower_left, enemy_ptower_right, player_crown_tower, player_ptower_left, player_ptower_right #overwrites the original towers
    enemy_ptower_left = Tower_Troop("Enemy_Tower", 3056, 109, 100, 100, 1.5, 1, 3, os.path.join(IMG_DIR, "tower.jpg"), False)
    enemy_ptower_right = Tower_Troop("Enemy_Tower", 3056, 109, 100, 100, 1.5, 14, 3, os.path.join(IMG_DIR, "tower.jpg"), False)
    player_ptower_left = Tower_Troop("Player_Tower", 3056, 109, 100, 100, 1.5, 1, 18, os.path.join(IMG_DIR, "tower.jpg"), True)
    player_ptower_right = Tower_Troop("Player_Tower", 3056, 109, 100, 100, 1.5, 14, 18, os.path.join(IMG_DIR, "tower.jpg"), True)
    #crown tower setup
    enemy_crown_tower = Crown_Tower("Enemy_Crown_Tower", 4824, 109, 100, 100, 1, 7.5, 1, os.path.join(IMG_DIR, "King_Tower_Red.jpg"), False)
    player_crown_tower = Crown_Tower("Player_Crown_Tower", 4824, 109, 100, 100, 1.2, 7.5, 21, os.path.join(IMG_DIR, "King_Tower_Blue.jpg"), True)
    tower_deck = [enemy_ptower_left, enemy_ptower_right, enemy_crown_tower, player_ptower_left, player_ptower_right, player_crown_tower] #creates new tower deck
    return tower_deck

#list of all the cards and their animations for easy access
card_animation_list = [
    (Knight, animation.knight_walk_E, animation.knight_walk_N, animation.knight_walk_S, animation.knight_walk_W),
    (The_Guy, animation.golem_walk_E, animation.golem_walk_N, animation.golem_walk_S, animation.golem_walk_W),
    (Archers, animation.archers_walk_E, animation.archers_walk_N, animation.archers_walk_S, animation.archers_walk_W),
    (Giant, animation.giant_walk_E, animation.giant_walk_N, animation.giant_walk_S, animation.giant_walk_W),
    (Cannon, animation.cannon_E, animation.cannon_N, animation.cannon_S, animation.cannon_W),
    (Xbow, animation.xbow_E, animation.xbow_N, animation.xbow_S, animation.xbow_W),
]
        

#cycles the deck to have new cards
def deck_cycle(selected_card, deck):
    index = deck.index(selected_card) #gets the selected card's index
    temp = deck[index] #stores in temp variable
    deck[index] = deck[4] #sets the selected card equal to the card that is coming up
    deck[4] = temp #changes the card to the selected card
    deck.append(deck.pop(4)) # puts the selected card to the end of the list
    
    
