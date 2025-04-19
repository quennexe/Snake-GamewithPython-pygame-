import pygame
import time
import random

# Pygame başlat
pygame.init()

# Renkler
white = (255, 255, 255)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)
dark_gray = (50, 50, 50)
light_gray = (200, 200, 200)
pink = (255, 182, 193)  

# Temalar
light_bg = white
dark_bg = black
light_snake = black
dark_snake = white
light_text = black
dark_text = white

# Ekran boyutu
width = 600
height = 400

# Oyun ekranı
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("🐍 Yılan Oyunu")

clock = pygame.time.Clock()
snake_block = 10
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 30)

# Başlangıç Ekranı
def mesaj(msg, color, y_offset=0):
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [width / 6, height / 3 + y_offset])

def skor_goster(score, text_color):
    value = score_font.render(f"Skor: {score}", True, text_color)
    screen.blit(value, [10, 10])

def highscore_goster(highscore, text_color):
    value = score_font.render(f"En Yüksek Skor: {highscore}", True, text_color)
    screen.blit(value, [width / 2 - 150, 10])

# En yüksek skoru okuma ve yazma
def get_highscore():
    try:
        with open("highscore.txt", "r") as file:
            highscore = int(file.read())
    except:
        highscore = 0
    return highscore

def set_highscore(new_highscore):
    with open("highscore.txt", "w") as file:
        file.write(str(new_highscore))

# Tema değişiklikleri
screen_bg = light_bg
snake_color = light_snake
food_color = red
text_color = light_text

def theme_toggle():
    global screen_bg, snake_color, food_color, text_color
    if screen_bg == light_bg:
        screen_bg = dark_bg
        snake_color = dark_snake
        food_color = red
        text_color = dark_text
    else:
        screen_bg = light_bg
        snake_color = light_snake
        food_color = red
        text_color = light_text

# Zorluk seçimi
def zorluk_secin():
    intro = True
    while intro:
        screen.fill(pink)  # Başlangıç ekranı pembe olacak
        mesaj("🐍 Yılan Oyunu", white, -50)
        mesaj("Tema: 'T' (Tema Değiştir)", white, 50)
        mesaj("Zorluk Seç: '1, 2, 3'", white, 100)
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                intro = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_t:
                    theme_toggle()
                elif event.key == pygame.K_1:
                    intro = False
                    return 15  # Kolay
                elif event.key == pygame.K_2:
                    intro = False
                    return 60  # Orta
                elif event.key == pygame.K_3:
                    intro = False
                    return 80  # Zor

# Yılan oyun fonksiyonu
def yilan_ciz(snake_block, snake_list):
    for x in snake_list:
        pygame.draw.rect(screen, snake_color, [x[0], x[1], snake_block, snake_block])

def oyun(difficulty):
    game_over = False
    game_close = False

    x1 = width / 2
    y1 = height / 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
    foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0

    difficulty = difficulty  # Zorluk seçimini al
    zorluk_aktif = False

    current_score = 0
    highscore = get_highscore()  # Yüksek skoru dosyadan oku

    while not game_over:

        while game_close:
            screen.fill(screen_bg)
            mesaj("Kaybettin! Q:Çık R:Yeniden Başla", red)
            skor_goster(current_score, text_color)
            highscore_goster(highscore, text_color)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_over = True
                    game_close = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                        game_close = False
                    if event.key == pygame.K_r:
                        oyun(difficulty)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -snake_block
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = snake_block
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -snake_block
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = snake_block
                    x1_change = 0

        x1 += x1_change
        y1 += y1_change

        if x1 >= width or x1 < 0 or y1 >= height or y1 < 0:
            game_close = True

        screen.fill(screen_bg)
        pygame.draw.rect(screen, food_color, [foodx, foody, snake_block, snake_block])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for segment in snake_list[:-1]:
            if segment == snake_head:
                game_close = True

        yilan_ciz(snake_block, snake_list)
        skor_goster(length_of_snake - 1, text_color)
        highscore_goster(highscore, text_color)

        pygame.display.update()

        if x1 == foodx and y1 == foody:
            foodx = round(random.randrange(0, width - snake_block) / 10.0) * 10.0
            foody = round(random.randrange(0, height - snake_block) / 10.0) * 10.0
            length_of_snake += 1

        current_score = length_of_snake - 1

        # Eğer yeni skor daha yüksekse, yüksek skoru güncelle
        if current_score > highscore:
            highscore = current_score
            set_highscore(highscore)

        clock.tick(difficulty)  # Zorluk seviyesine göre hız

    pygame.quit()
    quit()

# Başlangıç menüsüne git ve zorluk seçimi yap
difficulty = zorluk_secin()
oyun(difficulty)
