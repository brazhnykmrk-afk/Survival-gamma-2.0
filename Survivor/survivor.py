import pygame
import sys
import random

pygame.init()

# Music
pygame.mixer.music.load('sound/musik.ogg')
pygame.mixer.music.set_volume(0.1)
pygame.mixer.music.play(-1)

# Wood sound
wood_sound = pygame.mixer.Sound('sound/wood.ogg')

# Step on Grass sound
step_sound = pygame.mixer.Sound('sound/walking.ogg')
step_sound.set_volume(0.1)

# Score
score = 0
score2 = 0

# Colors
white = (255, 255, 255)
yellow = (255, 255, 0)
red = (255, 0, 0)

# Base
WIDTH, HEIGHT = 1200, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Survivor")
clock = pygame.time.Clock()

# Player
player_x = 0
player_y = 380
player_speed = 7

# Inventory
logs = 111110
stone_block = 11111110
grass = 0
meat = 0
hunger = 3
heart = 3

# Day - night base
day_time = True
switch_time = 1000

# Tent system
last_switch = pygame.time.get_ticks()
tent_level = 0
tent_x = 20
tent_y = 250

tent_costs = [
    {"logs": 20, "stone": 10},
    {"logs": 10, "stone": 30},
    {"logs": 100, "stone": 50},
    {"logs": 90, "stone": 75},
    {"logs": 120, "stone": 150}
]

tent_imgs = [
    pygame.image.load("img/tant_lvl1.png"),
    pygame.image.load("img/tant_lvl2.png"),
    pygame.image.load("img/tant_lvl3.png"),
    pygame.image.load("img/tant_lvl4.png"),
    pygame.image.load("img/tant_lvl5.png")
]

tent_imgs[0] = pygame.transform.scale(tent_imgs[0], (330, 330))
tent_imgs[1] = pygame.transform.scale(tent_imgs[1], (330, 330))
tent_imgs[2] = pygame.transform.scale(tent_imgs[2], (330, 330))
tent_imgs[3] = pygame.transform.scale(tent_imgs[3], (330, 330))
tent_imgs[4] = pygame.transform.scale(tent_imgs[4], (330, 330))

u_pressed = False

# Images
background = pygame.image.load("img/bg.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

tree_img = pygame.image.load("img/tree.png")
tree_img = pygame.transform.scale(tree_img, (450, 450))

stone_img = pygame.image.load("img/stone.jpg")
stone_img = pygame.transform.scale(stone_img, (60, 60))

log_img = pygame.image.load("img/log.jpg")
log_img = pygame.transform.scale(log_img, (60, 60))

grass_img = pygame.image.load("img/grass.jpg")
grass_img = pygame.transform.scale(grass_img, (60, 60))

meat_img = pygame.image.load("img/meat.png")
meat_img = pygame.transform.scale(meat_img, (100, 100))

rock_img = pygame.image.load("img/rock.png")
rock_img = pygame.transform.scale(rock_img, (260, 260))

hunger_img = pygame.image.load("img/hunger.png")
hunger_img = pygame.transform.scale(hunger_img, (70, 70))

heart_img = pygame.image.load("img/heart.png")
heart_img = pygame.transform.scale(heart_img, (50, 50))

pig_img = pygame.image.load("img/pig.png")
pig_img = pygame.transform.scale(pig_img, (250, 150))

background_night = pygame.image.load("img/bg_night.png")
background_night = pygame.transform.scale(background_night, (WIDTH, HEIGHT))

# Zanim
zombie_img = pygame.image.load("zanim/zanim1.png")
zombie_img = pygame.transform.scale(zombie_img, (260, 260))

zombie_img2 = pygame.image.load("zanim/zanim2.png")
zombie_img2 = pygame.transform.scale(zombie_img2, (260, 260))

zombie_img3 = pygame.image.load("zanim/zanim3.png")
zombie_img3 = pygame.transform.scale(zombie_img3, (260, 260))

anim_cadr_zombies = [zombie_img, zombie_img2, zombie_img3]

#Animation
zombie_animation_speed = 15
zombie_speed = 3
pig_speed = 1

# Items
item = []

# Entities
zombies = []
stones = []
trees = []
pigs = []

stones.append({"x": 700, "y": 340, "hits": 8})
trees.append({"x": 0, "y": 88, "hits": 5})
trees.append({"x": 450, "y": 88, "hits": 5})
pigs.append({"x": 200, "y": 380, "hits": 12})

# Animation
PLAYER_SIZE = (100, 140)

walk_right = [
    pygame.transform.scale(pygame.image.load("anim/pos1.png").convert_alpha(), PLAYER_SIZE),
    pygame.transform.scale(pygame.image.load("anim/pos2.png").convert_alpha(), PLAYER_SIZE),
    pygame.transform.scale(pygame.image.load("anim/pos3.png").convert_alpha(), PLAYER_SIZE),
    pygame.transform.scale(pygame.image.load("anim/pos4.png").convert_alpha(), PLAYER_SIZE)
]

hand_img = pygame.transform.scale(pygame.image.load("anim/hand_anim.png").convert_alpha(), PLAYER_SIZE)

direction = "right"
frame = 0
frame_count = 0
animation_speed = 10
image = walk_right[0]

# Zombie
zombie_live = False

# Key fix
f_key_pressed = False

# Zombie damage cooldown
last_hit_time = 0
hit_cooldown = 1000

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    if day_time:
        screen.blit(background, (0, 0))
    else:
        screen.blit(background_night, (0, 0))

    keys = pygame.key.get_pressed()
    moving = False
    hitting = False

    # Spawn trees & stones
    if player_x > 1080:
        player_x = 0

        min_distance = 120

        random_x = random.randint(0, WIDTH - 100)
        random_x2 = random.randint(0, WIDTH - 100)

        while abs(random_x - random_x2) < min_distance:
            random_x2 = random.randint(0, WIDTH - 100)

        trees.append({"x": random_x, "y": 88, "hits": 5})
        trees.append({"x": random_x2, "y": 88, "hits": 5})

        stone_offset = random.randint(-80, 80)

        stones.append({"x": max(0, random_x + stone_offset), "y": 340, "hits": 8})
        stones.append({"x": max(0, random_x2 - stone_offset), "y": 340, "hits": 8})

        pig_x = random.randint(0, WIDTH - 100)
        pigs.append({
            "x": pig_x,
            "y": 380,
            "hits": 12
        })


        if len(trees) > 6:
            trees.pop(0)
            trees.pop(0)

        if len(stones) > 6:
            stones.pop(0)
            stones.pop(0)

        if len(pigs) > 1:
            pigs.pop(0)

    # Movement
    if keys[pygame.K_a]:
        player_x -= player_speed
        direction = "left"
        moving = True
        step_sound.play()

    if keys[pygame.K_d]:
        player_x += player_speed
        direction = "right"
        moving = True
        step_sound.play()

    if keys[pygame.K_e]:
        if meat > 0 and hunger < 3:
            meat -= 1
            hunger += 1

    # HITBOXES
    player_rect = pygame.Rect(player_x + 20, player_y + 40, 60, 90)
    attack_rect = pygame.Rect(player_x - 40, player_y, 180, 140)

    # Attack
    if keys[pygame.K_f]:
        hitting = True
        if not f_key_pressed:

            for tree in trees[:]:
                tree_rect = pygame.Rect(tree["x"] + 180, tree["y"] + 300, 80, 150)
                if attack_rect.colliderect(tree_rect):
                    tree["hits"] -= 1
                    if tree["hits"] <= 0:
                        trees.remove(tree)
                        logs += 6
                        wood_sound.play()

            for stone in stones[:]:
                stone_rect = pygame.Rect(stone["x"] + 60, stone["y"] + 80, 140, 120)
                if attack_rect.colliderect(stone_rect):
                    stone["hits"] -= 1
                    if stone["hits"] <= 0:
                        stones.remove(stone)
                        stone_block += 3
                        wood_sound.play()


            for zombie in zombies[:]:
                zombie_rect = pygame.Rect(zombie["x"], zombie["y"], 260, 260)
                if attack_rect.colliderect(zombie_rect):
                    zombie["hits"] -= 1
                    if zombie["hits"] <= 0:
                        zombies.remove(zombie)
                        grass += 6
                        wood_sound.play()



            for pig in pigs[:]:
                pig_rect = pygame.Rect(pig["x"] + 40, pig["y"] + 40, 160, 70)

                if attack_rect.colliderect(pig_rect):
                    pig["hits"] -= 1

                    if pig["hits"] <= 0:
                        pigs.remove(pig)
                        meat += 1
                        wood_sound.play()


            f_key_pressed = True
    else:
        f_key_pressed = False





    # Upgrade
    if keys[pygame.K_u]:
        if not u_pressed:
            if tent_level < len(tent_costs):
                cost = tent_costs[tent_level]

                if logs >= cost["logs"] and stone_block >= cost["stone"]:
                    logs -= cost["logs"]
                    stone_block -= cost["stone"]
                    tent_level += 1

            u_pressed = True
    else:
        u_pressed = False

    # Borders
    if player_x < -40: player_x = -40
    if player_x > WIDTH - PLAYER_SIZE[0]: player_x = WIDTH - PLAYER_SIZE[0]

    # Draw
    for tree in trees:
        screen.blit(tree_img, (tree["x"], tree["y"]))

    for stone in stones:
        screen.blit(rock_img, (stone["x"], stone["y"]))

    for pig in pigs:

        # движение свиньи вправо
        pig["x"] += pig_speed

        # если ушла за экран → телепорт назад
        if pig["x"] > WIDTH:
            pig["x"] = -250

        screen.blit(pig_img, (pig["x"], pig["y"]))

    if tent_level > 0:
        screen.blit(tent_imgs[tent_level - 1], (tent_x, tent_y))

    # 🔥 ЗОМБИ: движение + анимация
    for zombie in zombies:
        if "frame" not in zombie:
            zombie["frame"] = 0
            zombie["frame_count"] = random.randint(0, 20)

        # 👉 ДВИЖЕНИЕ К ИГРОКУ
        if zombie["x"] < player_x:
            zombie["x"] += zombie_speed
        elif zombie["x"] > player_x:
            zombie["x"] -= zombie_speed

        zombie["frame_count"] += 1

        if zombie["frame_count"] >= zombie_animation_speed:
            zombie["frame"] += 1
            zombie["frame_count"] = 0

        img = anim_cadr_zombies[zombie["frame"] % len(anim_cadr_zombies)]
        screen.blit(img, (zombie["x"], zombie["y"]))


    # Player animation
    if moving:
        frame_count += 1
        if frame_count >= animation_speed:
            frame += 1
            frame_count = 0
    else:
        frame = 0

    if hitting:
        image = hand_img
    else:
        image = walk_right[frame % len(walk_right)]

    if direction == "left":
        image = pygame.transform.flip(image, True, False)


    player_rect = pygame.Rect(player_x + 20, player_y + 40, 60, 90)

    for zombie in zombies:
        zombie_rect = pygame.Rect(zombie["x"], zombie["y"], 260, 260)
        tent_rect = pygame.Rect(tent_x, tent_y, 330, 330)
        if tent_rect.colliderect(zombie_rect):
            zombie["x"] = 200

        # время сейчас
        current_hit_time = pygame.time.get_ticks()

        # если зомби касается игрока
        if player_rect.colliderect(zombie_rect):

            # проверяем кулдаун
            if current_hit_time - last_hit_time >= hit_cooldown:

                heart -= 1
                last_hit_time = current_hit_time




    screen.blit(image, (player_x, player_y))

    # UI
    screen.blit(stone_img, (20, 20))
    screen.blit(log_img, (120, 20))
    screen.blit(grass_img, (220, 20))
    screen.blit(meat_img, (290, -5))

    #hunger
    for i in range(hunger):
        screen.blit(hunger_img, (20 + i * 60, 520))

    #heart
    for i in range(hunger):
        screen.blit(heart_img, (900 + i * 60, 520))


    font_upg = pygame.font.Font(None, 40)
    screen.blit(font_upg.render("U to Upgrade", True, red), (950, 35))

    if tent_level < len(tent_costs):
        cost = tent_costs[tent_level]
        text = f"Need: {cost['logs']} wood, {cost['stone']} stone"
    else:
        text = "Max upgrade!"

    screen.blit(font_upg.render(text, True, red), (870, 70))


    # Day/Night + ZOMBIE SPAWN
    current_time = pygame.time.get_ticks()
    if current_time - last_switch >= switch_time:
        day_time = not day_time
        last_switch = current_time

        if not day_time:

            if hunger > 0:
                hunger -= 1

            for _ in range(2):
                zombies.append({
                    "x": random.randint(0, WIDTH - 260),
                    "y": 320,
                    "hits": 10
                })




    font = pygame.font.Font(None, 40)
    screen.blit(font.render(f"{stone_block}", True, red), (85, 35))
    screen.blit(font.render(f"{logs}", True, red), (185, 35))
    screen.blit(font.render(f"{grass}", True, red), (285, 35))
    screen.blit(font.render(f"{meat}", True, red), (380, 35))

    pygame.display.flip()
    clock.tick(60)