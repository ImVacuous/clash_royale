import pygame
import os
import src.cards as cards
import time
import src.arena as arena

start_time = pygame.time.get_ticks() // 1000  #convert to seconds


#make elixir
class Elixir():
    # initializes elixir logic variables
    def __init__(self, elixir_count):
        self.elixir_count = elixir_count

    #sets the speed at which elixir regenerates
    def elix_interval(self):
        current_time = pygame.time.get_ticks() // 1000
        single_elix_interval = 2.8 #elixir regenerates every 2.8s
        double_elix_interval = 1.4 #elixir regenerates every 1.4s
        triple_elix_interval = 0.9 #elixir regenerates every 0.9s
        elixir = single_elix_interval #sets the elixir to regen every 2.8s at the start of the game
        
        #elixir recharges faster
        if current_time == 60: #after 1 minute
            elixir = double_elix_interval
        elif current_time == 120: #after 2 minutes
            elixir = triple_elix_interval
        return elixir

    #checks if the player has enough elixir
    def can_subtract_elixir(self, card):
        print(f'self.elixir_count: {self.elixir_count}')
        #if elixir count is less than card cost, cannot play card
        if card.e_cost > self.elixir_count:
            return False
        
        #if elixir count is greater than or equal to card cost, can play card
        elif card.e_cost <= self.elixir_count:
            return True
    #subtract elixir when a card is played
    def subtract_elixir(self, card):
        if self.can_subtract_elixir(card): #check if enough elixir to play card
            self.elixir_count -= card.e_cost
            return self.elixir_count
    
#creates instances of elixir for player and enemy
player_elixir = Elixir(8)
enemy_elixir = Elixir(8)

class Gamelogic():
    # initializes game logic variables
    def __init__(self, player_crowns, enemy_crowns, start_time, game_results = None):
        self.player_crowns = player_crowns
        self.enemy_crowns = enemy_crowns
        self.start_time = start_time
        self.game_results = game_results

    #gets the current time in seconds
    def time(self):
        start_time = self.start_time
        overall_time = pygame.time.get_ticks() // 1000
        current_time = overall_time - start_time

        return current_time
    
    #checks if a tower is down and updates crowns and game results accordingly
    def tower_down(self):
        """ Checks current tower hit points and game time to update crown counts and determine the game result.

        Pre-conditions: 
            self: instance of Gamelogic class

        Parameters: 
            self: the current instances of gamelogic

        Returns: 
            None. 
        """
        current_time = self.time() #Gets the time
        
        #if either of the player's towers are destroyed, the enemy gets a point
        if cards.player_ptower_left.hp <= 0 or cards.player_ptower_right.hp <= 0:
            self.enemy_crowns = 1

            #if both player towers are down, the enemy gets 2 points
            if cards.player_ptower_left.hp <= 0 and cards.player_ptower_right.hp <= 0:
                self.enemy_crowns = 2

        #if either of the enemy's towers are destroyed, the player gets a point 
        elif cards.enemy_ptower_left.hp <= 0 or cards.enemy_ptower_right.hp <= 0:
            self.player_crowns = 1

            #if both enemy towers are down, the player gets 2 points
            if cards.enemy_ptower_left.hp <= 0 and cards.enemy_ptower_right.hp <= 0:
                self.player_crowns = 2

        #  determine win/loss/tie at end of match
        if current_time >= 180:
            if self.player_crowns > self.enemy_crowns:# player wins
                self.game_results = 'W'
            
            elif self.enemy_crowns > self.player_crowns:# enemy wins
                self.game_results = 'L'
            
            else:# tie
                self.game_results = 'T'

        #if the player's crown tower is destroyed, player loses
        if cards.player_crown_tower.hp <= 0:
            self.game_results = 'L' #enemy wins

        #if the enemy's crown tower is destroyed, player wins
        if cards.enemy_crown_tower.hp <= 0:
            self.game_results = 'W' #player wins

    #changes arena if towers are destroyed
    def arena_change(self):
        if cards.player_ptower_left.hp <= 0: #player's left tower
            for r in range(17, 21):
                for c in range(0, 4):
                    arena.arena_map[r][c] = 1

        if cards.player_ptower_right.hp <= 0: #player's right tower
            for r in range(17, 21):
                for c in range(13, 17):
                    arena.arena_map[r][c] = 1

        if cards.enemy_ptower_left.hp <= 0: #enemy's lef tower
            for r in range(2, 6):
                for c in range(0, 4):
                    arena.arena_map[r][c] = 1

        if cards.enemy_ptower_right.hp <= 0: #enemy's right tower
            for r in range(3, 7):
                for c in range(13, 17):
                    arena.arena_map[r][c] = 1

def arena_reset():
    for r in range(3, 6): #enemy left tower
        for c in range(1, 4):
            arena.arena_map[r][c] = 0
    for r in range(3, 6): #enemy right tower
        for c in range(14, 17):
            arena.arena_map[r][c] = 0
    for r in range(18, 21): #player left tower
        for c in range(1, 4):
            arena.arena_map[r][c] = 0
    for r in range(18, 21): #player right tower
        for c in range(14, 17):
            arena.arena_map[r][c] = 0





    