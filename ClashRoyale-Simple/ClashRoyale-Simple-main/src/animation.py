import os
import pyganim
import pygame

# Define the base directory for animations files
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# loads animation directories
ANI_DIR_CARDKNIGHT = os.path.join(BASE_DIR, "cardknight")
ANI_DIR_CARDGOLEM = os.path.join(BASE_DIR, "cardgolem")
ANI_DIR_CARDARCHERS = os.path.join(BASE_DIR, "cardarchers")
ANI_DIR_CARDGIANT = os.path.join(BASE_DIR, "cardgiant")
ANI_DIR_CARDCANNON = os.path.join(BASE_DIR, "cardcannon")
ANI_DIR_CARDXBOW = os.path.join(BASE_DIR, "cardxbow")
ANI_DIR_KNI_E = os.path.join(ANI_DIR_CARDKNIGHT, "knight_walk_E")
ANI_DIR_KNI_N = os.path.join(ANI_DIR_CARDKNIGHT, "knight_walk_N")
ANI_DIR_KNI_S = os.path.join(ANI_DIR_CARDKNIGHT, "knight_walk_S")
ANI_DIR_KNI_W = os.path.join(ANI_DIR_CARDKNIGHT, "knight_walk_W")
ANI_DIR_GOL_E = os.path.join(ANI_DIR_CARDGOLEM, "golem_walk_E")
ANI_DIR_GOL_N = os.path.join(ANI_DIR_CARDGOLEM, "golem_walk_N")
ANI_DIR_GOL_S = os.path.join(ANI_DIR_CARDGOLEM, "golem_walk_S")
ANI_DIR_GOL_W = os.path.join(ANI_DIR_CARDGOLEM, "golem_walk_W")
ANI_DIR_ARC_E = os.path.join(ANI_DIR_CARDARCHERS, "archer_walk_E")
ANI_DIR_ARC_N = os.path.join(ANI_DIR_CARDARCHERS, "archer_walk_N")
ANI_DIR_ARC_S = os.path.join(ANI_DIR_CARDARCHERS, "archer_walk_S")
ANI_DIR_ARC_W = os.path.join(ANI_DIR_CARDARCHERS, "archer_walk_W")
ANI_DIR_GIA_N = os.path.join(ANI_DIR_CARDGIANT, "giant_walk_N")
ANI_DIR_GIA_S = os.path.join(ANI_DIR_CARDGIANT, "giant_walk_S")
ANI_DIR_GIA_E = os.path.join(ANI_DIR_CARDGIANT, "giant_walk_E")
ANI_DIR_GIA_W = os.path.join(ANI_DIR_CARDGIANT, "giant_walk_W")
ANI_DIR_CAN_E = os.path.join(ANI_DIR_CARDCANNON, "cannon_E")
ANI_DIR_CAN_N = os.path.join(ANI_DIR_CARDCANNON, "cannon_N")
ANI_DIR_CAN_S = os.path.join(ANI_DIR_CARDCANNON, "cannon_S")
ANI_DIR_CAN_W = os.path.join(ANI_DIR_CARDCANNON, "cannon_W")
ANI_DIR_XBO_E = os.path.join(ANI_DIR_CARDXBOW, "xbow_E")
ANI_DIR_XBO_N = os.path.join(ANI_DIR_CARDXBOW, "xbow_N")
ANI_DIR_XBO_S = os.path.join(ANI_DIR_CARDXBOW, "xbow_S")
ANI_DIR_XBO_W = os.path.join(ANI_DIR_CARDXBOW, "xbow_W")


# Function to load animations from a directory
def load_animation(dir_path, speed=100):
    frames = [] #animations need to be returned as a list of tuples for pyganim module to work
    for file_name in sorted(os.listdir(dir_path)): #finds every file in folder and sorts them
        file_path = os.path.join(dir_path, file_name) #gets full path of each image
        image = pygame.image.load(file_path).convert_alpha() # loads image
        scaled_image = pygame.transform.scale(image, (50, 50)) #scales image
        frames.append((scaled_image, speed)) #adds as a tuple to frames 

    anim = pyganim.PygAnimation(frames) #animates frames
    anim.play() #plays animations
    
    return anim

# Load animations for different characters and the speed of animation
knight_walk_E = load_animation(ANI_DIR_KNI_E, 400)
knight_walk_N = load_animation(ANI_DIR_KNI_N, 400)
knight_walk_S = load_animation(ANI_DIR_KNI_S, 400)
knight_walk_W = load_animation(ANI_DIR_KNI_W, 400)
golem_walk_E = load_animation(ANI_DIR_GOL_E, 1000)
golem_walk_N = load_animation(ANI_DIR_GOL_N, 1000)
golem_walk_S = load_animation(ANI_DIR_GOL_S, 1000)
golem_walk_W = load_animation(ANI_DIR_GOL_W, 1000)
archers_walk_E = load_animation(ANI_DIR_ARC_E, 300)
archers_walk_N = load_animation(ANI_DIR_ARC_N, 300)
archers_walk_S = load_animation(ANI_DIR_ARC_S, 300)
archers_walk_W = load_animation(ANI_DIR_ARC_W, 300)
giant_walk_E = load_animation(ANI_DIR_GIA_E, 600)
giant_walk_N = load_animation(ANI_DIR_GIA_N, 600)
giant_walk_S = load_animation(ANI_DIR_GIA_S, 600)
giant_walk_W = load_animation(ANI_DIR_GIA_W, 600)
cannon_E = load_animation(ANI_DIR_CAN_E, 1000)
cannon_N = load_animation(ANI_DIR_CAN_N, 1000)
cannon_S = load_animation(ANI_DIR_CAN_S, 1000)
cannon_W = load_animation(ANI_DIR_CAN_W, 1000)
xbow_E = load_animation(ANI_DIR_XBO_E, 1000)
xbow_N = load_animation(ANI_DIR_XBO_N, 1000)
xbow_S = load_animation(ANI_DIR_XBO_S, 1000)
xbow_W = load_animation(ANI_DIR_XBO_W, 1000)

