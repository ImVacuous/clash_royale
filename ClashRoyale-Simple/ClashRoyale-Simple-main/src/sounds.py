import pygame
import os

pygame.mixer.init()

# Define the base directory for audio files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Load sound effects
golem_attack = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "golem_attack.wav"))
golem_spawn = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "golem_spawn.wav"))
knight_attack = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "knight_attack.wav"))
knight_spawn = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "knight_spawn.wav"))
archer_attack = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "archer_attack.wav"))
archer_spawn = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "archer_spawn.wav"))
giant_attack = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "giant_attack.wav"))
giant_spawn = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "giant_spawn.wav"))
cannon_attack = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "cannon_attack.wav"))
cannon_spawn = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "cannon_spawn.wav"))
xbow_attack = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "xbow_attack.wav"))
xbow_spawn = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "xbow_spawn.wav"))
log_spawn = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "log_spawn.wav"))
rocket_spawn = pygame.mixer.Sound(os.path.join(BASE_DIR, "audio", "rocket_spawn.wav"))

# Set volume levels
knight_attack.set_volume(1)
golem_attack.set_volume(0.01)
archer_attack.set_volume(0.1)
giant_attack.set_volume(1)
cannon_attack.set_volume(1)
xbow_attack.set_volume(3)    

def mute_attack():
    knight_attack.set_volume(0)
    golem_attack.set_volume(0)
    archer_attack.set_volume(0)
    giant_attack.set_volume(0)
    cannon_attack.set_volume(0)
    xbow_attack.set_volume(0)   

def unmute_attack():
    knight_attack.set_volume(0.1)
    golem_attack.set_volume(0.01)
    archer_attack.set_volume(0.1)
    giant_attack.set_volume(1)
    cannon_attack.set_volume(1)
    xbow_attack.set_volume(3)       