import pygame
pygame.init()

import sys
import random
import pygame.freetype

clock = pygame.time.Clock()

# window setup
WINDOW_WIDTH = 650
WINDOW_HEIGHT = 650
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Clash Royale Simple")

# colours & tile size
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
TILE_SIZE = 27

# imports
import src.screen as screen
import src.game as game
import src.cards as cards
import src.arena as arena
import src.sounds as sounds

# font
font = pygame.freetype.Font(cards.DIR_FONT, 24)

# loading screen assets
background = pygame.image.load(cards.DIR_MENU_LOADING)
background = pygame.transform.scale(background, (WINDOW_WIDTH, WINDOW_HEIGHT))
logo = pygame.image.load(cards.DIR_MENU_LOGO)
logo = pygame.transform.scale(logo, (200, 100))

# game over assets
gamewon = pygame.image.load(cards.DIR_WON)
gamewon = pygame.transform.scale(gamewon, (WINDOW_WIDTH, WINDOW_HEIGHT))
gamelost = pygame.image.load(cards.DIR_LOSS)
gamelost = pygame.transform.scale(gamelost, (WINDOW_WIDTH, WINDOW_HEIGHT))
gametied = pygame.image.load(cards.DIR_TIED)
gametied = pygame.transform.scale(gametied, (WINDOW_WIDTH, WINDOW_HEIGHT))  

# elixir display
testdisplay = font.render(str(game.player_elixir.elixir_count), True, WHITE)

# timers
elixir_regen_interval = pygame.USEREVENT
enemy_spawn_timer = pygame.USEREVENT + 1
pygame.time.set_timer(elixir_regen_interval, int(game.player_elixir.elix_interval()) * 1000)
pygame.time.set_timer(enemy_spawn_timer, 10000)

# determines attack cooldowns
card_attack_cooldown = pygame.USEREVENT + 2
pygame.time.set_timer(elixir_regen_interval, int(game.player_elixir.elix_interval()) * 1000)

# building decay event
building_jetty_decay_event = pygame.USEREVENT + 3
pygame.time.set_timer(building_jetty_decay_event, 1000)

# resets game for new round
def reset(): 
    game.player_elixir.elixir_count = 5 # reset elixir counts
    game.enemy_elixir.elixir_count = 5 # reset elixir counts
    cards.placed_card.clear() # reset placed cards
    cards.enemy_placed.clear() # reset enemy placed cards
    cards.tower_deck.clear() # reset towers
    cards.tower_deck = cards.init_cards(cards.tower_deck) # reinitialize towers
    game.arena_reset() # reset arena
    global gamelogic # reset gamelogic
    gamelogic = game.Gamelogic(0, 0, (pygame.time.get_ticks() // 1000), None)# resets player, enemy towers and game results


# menu screen
def menu():
    loading = True
    while loading:
        WINDOW.blit(background, (0, 0))
        WINDOW.blit(logo, ((WINDOW_WIDTH // 2 - 100), (WINDOW_HEIGHT // 4 - 100)))
        font.render_to(WINDOW, ((WINDOW_WIDTH // 2 - 150), (WINDOW_HEIGHT // 4 + 50)), "Press Enter to start", BLACK)
        font.render_to(WINDOW, ((WINDOW_WIDTH // 2 - 200), (WINDOW_HEIGHT // 4 + 100)), "Press Space for tutorial", BLACK)
        pygame.display.update()  
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit game
                pygame.quit()
            if event.type == pygame.KEYDOWN: # key press
                if event.key == pygame.K_RETURN: # start game
                    loading = False
                    return 'play'
                elif event.key == pygame.K_SPACE: # tutorial
                    loading = False
                    return 'tutorial'
          
#  tutorial screen
def tutorial():
    in_tutorial = True
    while in_tutorial:
        WINDOW.fill(BLACK)
        font.render_to(WINDOW, (50, 50), "Tutorial", WHITE)
        font.render_to(WINDOW, (50, 100), "1. Click on a card in your deck to select it.", WHITE)
        font.render_to(WINDOW, (50, 150), "2. Click on the arena to place the selected card.", WHITE)
        font.render_to(WINDOW, (50, 200), "3. You need enough elixir to place a card.", WHITE)
        font.render_to(WINDOW, (50, 250), "4. Defeat the enemy towers to win!", WHITE)
        font.render_to(WINDOW, (50, 300), "Press Space to return to menu.", WHITE)

        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN: # key press
                if event.key == pygame.K_SPACE: # return to menu
                    in_tutorial = False
                    return 'menu'
        pygame.display.update()

# main game loop
def game_loop():
    running = True 
    selected_card = None # currently selected card
    emote_list = []
    global gamelogic
    gamelogic = game.Gamelogic(0, 0, (pygame.time.get_ticks() // 1000), None) # initializes gamelogic
    while running:
        WINDOW.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # exit game
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN: # mouse click
                click_state = True
                # Check if a card in the deck is clicked
                if screen.rect_1.collidepoint(event.pos): # first card
                    selected_card = cards.deck[0]
                    click_state = False
                elif screen.rect_2.collidepoint(event.pos): # second card
                    selected_card = cards.deck[1]
                    click_state = False
                elif screen.rect_3.collidepoint(event.pos): # third card
                    selected_card = cards.deck[2]
                    click_state = False
                elif screen.rect_4.collidepoint(event.pos): # fourth card
                    selected_card = cards.deck[3]
                    click_state = False

                # card placement on arena
                if click_state and selected_card:
                    mouse_x, mouse_y = event.pos
                    grid_x = mouse_x // TILE_SIZE
                    grid_y = mouse_y // TILE_SIZE

                    # check valid placement
                    if grid_x <= 18 and grid_y <= 24:
                        if arena.arena_map[grid_y][grid_x] == 0:
                            continue
                        
                        #only place on your side
                        if grid_y < 13:
                            continue
                
                        # new card instance
                        new_card = selected_card(
                            x=grid_x * TILE_SIZE,
                            y=grid_y * TILE_SIZE,
                            is_friendly=True)
                        
                        # valid elixir check
                        if game.player_elixir.can_subtract_elixir(new_card):
                            game.player_elixir.subtract_elixir(new_card)
                            # card placement
                            cards.placed_card.append(new_card)
                            cards.deck_cycle(selected_card, cards.deck)
                            new_card.spawn_play_sound(new_card)
                        else:
                            print("Not enough elixir to place this card.")
                    selected_card = None
                    click_state = False
            elif event.type == elixir_regen_interval: # player elixir regen
                if game.player_elixir.elixir_count < 10:
                    game.player_elixir.elixir_count += 1
                if game.enemy_elixir.elixir_count < 10:
                    game.enemy_elixir.elixir_count += 1

            elif event.type == enemy_spawn_timer: # enemy card spawn

                if game.enemy_elixir.elixir_count > 0:
                    selected = random.choice(cards.enemy_deck)
                    x_cord = random.choice([random.randint(0, 6), random.randint(11, 17)]) # selects random x coordinate(not on non-walkable area)
                    temp_enemy = selected(x=x_cord * TILE_SIZE, y=0, is_friendly=False) # creates enemy
                    if game.enemy_elixir.can_subtract_elixir(temp_enemy): # check elixir
                        game.enemy_elixir.subtract_elixir(temp_enemy) # removes elixir from player dependent on card's elixir cost
                        cards.enemy_placed.append(temp_enemy) # adds enemy to enemy cards list
            
            # building decay event
            elif event.type == building_jetty_decay_event:
                for card in all_cards:
                    if isinstance(card, cards.Buildings):
                        card.decay()

            elif event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_m: # mutes attack sounds when M is pressed
                    sounds.mute_attack()
                if event.key == pygame.K_s: # unmutes attack sounds when S is pressed
                    sounds.unmute_attack()

        # drawing screen elements
        screen.draw_arena()
        screen.draw_deck()
        screen.draw_elixir()
        screen.draw_towers(cards.tower_deck)

        # game timer
        current_time = 180 - gamelogic.time()
        min = current_time // 60
        sec = current_time % 60
        font.render_to(WINDOW, (screen.ARENA_WIDTH + 50, WINDOW_HEIGHT - 50), f'{min}:{sec}', WHITE)
        
        # game logic
        gamelogic.tower_down()

        # combines all cards types into one list
        all_cards = cards.tower_deck + cards.placed_card + cards.enemy_placed
        
        for card in all_cards:
            card.pos = pygame.math.Vector2(card.x, card.y)

            # process combat for card
            attacking = card.attack(card, all_cards)
            
            # determines movement when not in combat 
            if not attacking:
                if hasattr(card, 'move'):
                    if card.is_friendly: # movement end location for player cards
                        card.x, card.y = card.move(card.x, card.y, 9, 3)
                    else: # movement end location for enemy cards
                        card.x, card.y = card.move(card.x, card.y, 9, 20) 
            
            # renders card at new location
            screen.draw_cards(card, card.x, card.y) 
        # game status
        game_status = gamelogic.game_results # checks whether player has won, lost or tied
        print(f'hp: {cards.enemy_crown_tower.hp}')
        print(game_status)
        if game_status == 'W': # player has won
            WINDOW.blit(gamewon, (0, 0)) # displays game won screen
            font.render_to(WINDOW, (250, 300), "You Won!", WHITE)
            pygame.display.update()
            pygame.time.delay(3000) # waits 3 seconds
            pygame.display.update()
            running = False # ends game
            reset() # resets game information for future rounds

        elif game_status == 'L': # enemy has won
            WINDOW.blit(gamelost, (0, 0)) # displays game lost screen
            font.render_to(WINDOW, (250, 300), "You Lost!", WHITE)
            pygame.display.update()
            pygame.time.delay(3000) # waits 3 seconds
            pygame.display.update()
            running = False # ends game
            reset() # resets game information for future rounds
        
        elif game_status == 'T': # player has tied
            WINDOW.blit(gametied, (0, 0)) # displays game tied screen
            font.render_to(WINDOW, (250, 300), "Tie Game!", WHITE)
            pygame.display.update()
            pygame.time.delay(3000) # waits 3 seconds
            pygame.display.update()
            running = False # ends game
            reset() # resets game information for future rounds

        pygame.display.update()
    return 'menu' # returns to menu

# main function
def main():
    state = "menu" # automatically sends user to menu
    while True:
        if state == "menu": # sends user to menu
            state = menu()
        elif state == "play": # sends user into game
            state = game_loop()
        elif state == "tutorial": # sends user to tutorial
            state = tutorial()
        else:
            pygame.quit() # exits program

if __name__ == "__main__":
    main()


#doc string
#sounds overlapping
#attack range
