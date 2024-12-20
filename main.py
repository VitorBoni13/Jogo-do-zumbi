import pgzrun
from random import randint

WIDTH = 1000
HEIGHT = 600

player = Actor("player_idle")
zombie = Actor("zombie_walk1")
player.pos = 40, HEIGHT - 70

level = 0
box_enemies = []
walk = True
dead = False
won = False
created = False
game_started = False  # Variável para controlar se o jogo foi iniciado

background = {
    0: ["maxresdefault", 15, 40, HEIGHT - 70],
    1: ["mountain_back", 80, 40, HEIGHT - 120],
    2: ["desertcity", 15, 40, HEIGHT - 70],
    3: ["night", 15, 40, HEIGHT - 70]
}

zombie.pos = WIDTH - 100, background[level][3]

# Variáveis de controle para a música
music_on = True
music.play("background_music")  # A música de fundo deve ser carregada

def draw():
    if not game_started:
        draw_menu()  # Desenha o menu principal
    else:
        global dead, bg
        if not won:
            if dead:
                if_dead()
            else:
                if_not_dead()
        else:
            if_won()

def draw_menu():
    # Tela de fundo do menu
    screen.fill((0, 0, 0))
    screen.draw.text("MENU PRINCIPAL", (WIDTH // 2 - 100, HEIGHT // 4), fontsize=40, color="white")
    # Botões de navegação
    screen.draw.rect(Rect((WIDTH // 2 - 100, HEIGHT // 2 - 30), (200, 50)), (0, 128, 0))
    screen.draw.text("Começar Jogo", (WIDTH // 2 - 85, HEIGHT // 2 - 15), fontsize=30, color="white")
    
    screen.draw.rect(Rect((WIDTH // 2 - 100, HEIGHT // 2 + 40), (200, 50)), (0, 128, 0))
    screen.draw.text("Música: " + ("Ligada" if music_on else "Desligada"), (WIDTH // 2 - 85, HEIGHT // 2 + 55), fontsize=30, color="white")
    
    screen.draw.rect(Rect((WIDTH // 2 - 100, HEIGHT // 2 + 110), (200, 50)), (255, 0, 0))
    screen.draw.text("Sair", (WIDTH // 2 - 30, HEIGHT // 2 + 125), fontsize=30, color="white")

def on_mouse_down(pos):
    global game_started, music_on
    # Verifica onde o jogador clicou para realizar a ação
    if Rect((WIDTH // 2 - 100, HEIGHT // 2 - 30), (200, 50)).collidepoint(pos):  # Botão "Começar Jogo"
        game_started = True
        screen.clear()  # Limpa a tela do menu
    elif Rect((WIDTH // 2 - 100, HEIGHT // 2 + 40), (200, 50)).collidepoint(pos):  # Botão "Música"
        music_on = not music_on
        if music_on:
            music.play("background_music")  # Tocar música de fundo
        else:
            music.stop()  # Parar a música
    elif Rect((WIDTH // 2 - 100, HEIGHT // 2 + 110), (200, 50)).collidepoint(pos):  # Botão "Sair"
        exit()  # Fecha o jogo

def if_dead():
    screen.blit(background[level][0], (0, 0))
    screen.draw.text("You Are Dead !!!", ((WIDTH // 2 - 100), HEIGHT // 2), fontsize=30, color="white")

def if_not_dead():
    screen.blit(background[level][0], (0, 0))
    player.draw()
    zombie.draw()
    draw_box_enemy()

def if_won():
    screen.blit(background[level][0], (0, 0))
    screen.draw.text("You Won !!!", ((WIDTH // 2 - 100), HEIGHT // 2), fontsize=30, color="white")
    player.draw()
    player.pos = (WIDTH // 2) + 100, HEIGHT // 2
    player.image = "player_cheer2"

def update():
    global count, bg, level, dead, won, created
    if not game_started:
        return  # Não faz nada se o jogo não foi iniciado

    zombie.left -= 2
    move_box()
    check_collision()

    if not dead:
        if player.bottom >= HEIGHT - background[level][1]:
            player.pos = player.x, player.y
        else:
            gravity_done()

        if level == 0:
            level_find(0)

        elif level == 1:
            level_find(1)

        elif level == 2:
            level_find(2)

        elif level == 3:
            level_find(3)

        if player.left >= WIDTH:
            if level < 3:
                level += 1
                screen.clear()
                created = False
                player.pos = background[level][2], background[level][3]
                zombie.pos = WIDTH, background[level][3]
                sounds.maximize_004.play()
            else:
                screen.clear()
                player.pos = WIDTH // 2, HEIGHT // 2
                player.image = "player_cheer2"
                won = True
                sounds.maximize_004.play()

def level_find(n):
    global created, dead
    if not created:
        num_box(n)
        created = True

    if zombie.right == 500:
        num_box(n)

    if zombie.right <= 0:
        zombie.pos = WIDTH, background[level][3]
        created = False
        num_box(n)

    if zombie.colliderect(player):
        dead = True
        sounds.minimize_004.play()

def num_box(num):
    if num == 0:
        create_box_enemy(randint(30, 40), randint(200, 299))
    elif num == 1:
        create_box_enemy(randint(30, 40), randint(200, 299))
        create_box_enemy(randint(0, 10), randint(300, 400))
    elif num == 2:
        create_box_enemy(randint(30, 40), randint(200, 299))
        create_box_enemy(randint(0, 10), randint(300, 350))
        create_box_enemy(randint(20, 30), randint(350, 400))
    elif num == 3:
        create_box_enemy(randint(30, 40), randint(200, 299))
        create_box_enemy(randint(0, 10), randint(300, 350))
        create_box_enemy(randint(20, 30), randint(350, 400))
        create_box_enemy(randint(20, 30), randint(400, 500))

def create_box_enemy(width, height):
    bg = ["bluebox", "greenbox", "redbox", "yellowbox"]
    enemy = Actor(bg[randint(0, 3)])
    enemy.draw()
    enemy.pos = WIDTH - width, background[level][3] - height
    box_enemies.append(enemy)

def draw_box_enemy():
    for enemy in box_enemies:
        enemy.draw()

def move_box():
    for enemy in box_enemies:
        enemy.x -= 3

def check_collision():
    global dead
    for enemy in box_enemies:
        if player.colliderect(enemy):
            dead = True

def gravity_done():
    player.vy = 0
    GRAVITY = 2
    uy = player.vy
    player.vy += GRAVITY
    player.y += player.vy

def on_key_down(key):
    if key == keys.UP:
        player.pos = (player.x, player.y - 80)
        player.image = "player_jump"
    elif key == keys.D:
        player.pos = (player.x + 50, player.y)
        walking()
    elif key == keys.A:
        player.pos = (player.x - 50, player.y)
        walking()

def walking():
    global walk
    if walk:
        player.image = "player_walk1"
        sounds.footstep_grass_004.play()
        walk = False
    else:
        player.image = "player_walk2"
        sounds.footstep_grass_004.play()
        walk = True

pgzrun.go()
