import pygame
import time
import random

# Inicialización de pygame
pygame.init()

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Dimensiones de la ventana
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600

# Configuración de la ventana
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Serpy")

# Configuración de la fuente
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)

# FPS
clock = pygame.time.Clock()
FPS = 20

# Función para mostrar el texto
def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)

# Función del menú principal
def main_menu():
    while True:
        window.fill(BLACK)
        draw_text("Serpy", large_font, WHITE, window, WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 4)
        
        mx, my = pygame.mouse.get_pos()
        
        button_play = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50, 200, 50)
        button_how_to_play = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20, 200, 50)
        button_exit = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 90, 200, 50)
        
        if button_play.collidepoint((mx, my)):
            if click:
                game()
        if button_how_to_play.collidepoint((mx, my)):
            if click:
                how_to_play()
        if button_exit.collidepoint((mx, my)):
            if click:
                pygame.quit()
                exit()
        
        pygame.draw.rect(window, RED, button_play)
        pygame.draw.rect(window, RED, button_how_to_play)
        pygame.draw.rect(window, RED, button_exit)
        
        draw_text("Jugar", font, WHITE, window, WINDOW_WIDTH // 2 - 35, WINDOW_HEIGHT // 2 - 35)
        draw_text("Cómo jugar", font, WHITE, window, WINDOW_WIDTH // 2 - 70, WINDOW_HEIGHT // 2 + 35)
        draw_text("Salir", font, WHITE, window, WINDOW_WIDTH // 2 - 30, WINDOW_HEIGHT // 2 + 105)
        
        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        
        pygame.display.update()
        clock.tick(60)

# Función para la pantalla de "Cómo jugar"
def how_to_play():
    running = True
    while running:
        window.fill(BLACK)
        draw_text("Cómo jugar", large_font, WHITE, window, WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 4)
        draw_text("Usa las teclas W, A, S, D para mover la serpiente.", font, WHITE, window, 20, WINDOW_HEIGHT // 2 - 20)
        draw_text("Presiona cualquier tecla para volver al menú.", font, WHITE, window, 20, WINDOW_HEIGHT // 2 + 20)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                running = False
        
        pygame.display.update()
        clock.tick(60)

# Función del juego
def game():
    # Configuración del juego
    snake_pos = [100, 50]
    snake_body = [[100, 50], [90, 50], [80, 50]]
    direction = 'RIGHT'
    change_to = direction

    food_pos = [random.randrange(1, (WINDOW_WIDTH // 10)) * 10, random.randrange(1, (WINDOW_HEIGHT // 10)) * 10]
    food_spawn = True

    score = 0

    def game_over():
        window.fill(BLACK)
        draw_text('Game Over', large_font, RED, window, WINDOW_WIDTH // 2 - 150, WINDOW_HEIGHT // 2 - 50)
        draw_text('Presiona cualquier tecla para volver al menú', font, WHITE, window, 20, WINDOW_HEIGHT // 2 + 20)
        pygame.display.flip()
        time.sleep(1)
        waiting_for_key = True
        while waiting_for_key:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                if event.type == pygame.KEYDOWN:
                    waiting_for_key = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == ord('w'):
                    change_to = 'UP'
                if event.key == pygame.K_DOWN or event.key == ord('s'):
                    change_to = 'DOWN'
                if event.key == pygame.K_LEFT or event.key == ord('a'):
                    change_to = 'LEFT'
                if event.key == pygame.K_RIGHT or event.key == ord('d'):
                    change_to = 'RIGHT'

        if change_to == 'UP' and direction != 'DOWN':
            direction = 'UP'
        if change_to == 'DOWN' and direction != 'UP':
            direction = 'DOWN'
        if change_to == 'LEFT' and direction != 'RIGHT':
            direction = 'LEFT'
        if change_to == 'RIGHT' and direction != 'LEFT':
            direction = 'RIGHT'

        if direction == 'UP':
            snake_pos[1] -= 10
        if direction == 'DOWN':
            snake_pos[1] += 10
        if direction == 'LEFT':
            snake_pos[0] -= 10
        if direction == 'RIGHT':
            snake_pos[0] += 10

        snake_body.insert(0, list(snake_pos))
        if snake_pos == food_pos:
            score += 10
            food_spawn = False
        else:
            snake_body.pop()

        if not food_spawn:
            food_pos = [random.randrange(1, (WINDOW_WIDTH // 10)) * 10, random.randrange(1, (WINDOW_HEIGHT // 10)) * 10]
        food_spawn = True

        window.fill(BLACK)
        for pos in snake_body:
            pygame.draw.rect(window, GREEN, pygame.Rect(pos[0], pos[1], 10, 10))

        pygame.draw.rect(window, RED, pygame.Rect(food_pos[0], food_pos[1], 10, 10))

        if snake_pos[0] < 0 or snake_pos[0] > WINDOW_WIDTH-10 or snake_pos[1] < 0 or snake_pos[1] > WINDOW_HEIGHT-10:
            game_over()
            return

        for block in snake_body[1:]:
            if snake_pos == block:
                game_over()
                return

        pygame.display.update()
        clock.tick(FPS)

# Ejecutar el menú principal
main_menu()
