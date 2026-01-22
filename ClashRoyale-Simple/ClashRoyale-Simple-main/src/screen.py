import pygame
from src.arena import arena_map
from main import WINDOW, WINDOW_HEIGHT, WINDOW_WIDTH, GREEN, PURPLE, BLACK, GREY, BLUE, WHITE, TILE_SIZE
import src.game as game
import os
from src.cards import deck, Towers, Crown_Tower
import src.animation as animation
import pyganim
#Set up arena dimensions and position
ARENA_WIDTH = TILE_SIZE * 18
ARENA_HEIGHT = TILE_SIZE * 24

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ice_tile_1 = pygame.image.load(os.path.join(BASE_DIR, 'pictures', 'tile_one.png'))
ice_tile_2 = pygame.image.load(os.path.join(BASE_DIR, 'pictures', 'tile_two.png'))
water_tile = pygame.image.load(os.path.join(BASE_DIR, 'pictures', 'watertile.png'))
scaled_image = pygame.transform.scale(ice_tile_1, (TILE_SIZE, TILE_SIZE))
scaled_image_2 = pygame.transform.scale(ice_tile_2, (TILE_SIZE, TILE_SIZE))
water_scaled = pygame.transform.scale(water_tile, (TILE_SIZE, TILE_SIZE))


#Set up arena on screen
def draw_arena():
    count = 0
    for r in range(len(arena_map)):
        for c in range(len(arena_map[r])):
            tile = arena_map[r][c]
            if tile == 0: # sets up non walkable tiles
                WINDOW.blit(water_scaled, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                pygame.draw.rect(WINDOW, BLACK, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)

            elif tile == 1: # sets up walkable tiles
                if count == 0: # sets up lighter ice tile
                    WINDOW.blit(scaled_image, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    count += 1
                elif count == 1: # sets up darker ice tile
                    WINDOW.blit(scaled_image_2, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE))
                    count -= 1
            # draws grid outline
            pygame.draw.rect(WINDOW, BLACK, (c*TILE_SIZE, r*TILE_SIZE, TILE_SIZE, TILE_SIZE), 1)


#Set up elixir on screen

def draw_elixir():
    # draws elixir bar
    for i in range(game.player_elixir.elixir_count):
        thickness = 35
        line_height = WINDOW_HEIGHT // 10
        # elixir bar design
        pygame.draw.rect(WINDOW, PURPLE, (WINDOW_WIDTH - thickness, WINDOW_HEIGHT - ((i + 1) * line_height), thickness, line_height))
        # elixir bar outline
        pygame.draw.rect(WINDOW, BLACK, (WINDOW_WIDTH - thickness, WINDOW_HEIGHT - ((i + 1) * line_height), thickness, line_height), 2)


#Set up deck on screen
def draw_deck():
    # draws first deck card
    WINDOW.blit(deck[0]().image_pathing(), (ARENA_WIDTH, 0))
    global rect_1
    rect_1 = deck[0]().image_pathing().get_rect(topleft=(ARENA_WIDTH, 0))
    # draws second deck card
    WINDOW.blit(deck[1]().image_pathing(), (ARENA_WIDTH, 142))
    global rect_2
    rect_2 = deck[1]().image_pathing().get_rect(topleft=(ARENA_WIDTH, 142))
    # draws third deck card
    WINDOW.blit(deck[2]().image_pathing(), (ARENA_WIDTH, 284))
    global rect_3
    rect_3 = deck[2]().image_pathing().get_rect(topleft=(ARENA_WIDTH, 284))
    # draws fourth deck card
    WINDOW.blit(deck[3]().image_pathing(), (ARENA_WIDTH, 426))
    global rect_4
    rect_4 = deck[3]().image_pathing().get_rect(topleft=(ARENA_WIDTH, 426))

# Draws selected card at mouse position
def draw_cards(selected_card, grid_x, grid_y):
    """ Renders the given cards to the display window.

    Pre-conditions: 
        - selected_cards: class instances
        - grid_x: int
        - grid_y: int
     
        
    Parameters:
        - selected_cards: the player's selected card
        - grid_x: the x coordinate of chosen placement on arena map
        - grid_y: the y coordinate of chosen placement on arena_map

    Returns: 
        None
    """
    card_ani = selected_card.animation(selected_card)
    card_ani.blit(WINDOW, (grid_x - TILE_SIZE // 2, grid_y - TILE_SIZE // 2))
    
# Draws towers on the arena
def draw_towers(tower_list):
    for tower in tower_list:
        tower_picture = tower.animation()
        WINDOW.blit(tower_picture, (tower.x, tower.y))
