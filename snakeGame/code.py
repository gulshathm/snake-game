import pygame
import random

WIDTH, HEIGHT = 600, 600
BLOCK_SIZE = 10
pygame.font.init()
score_font = pygame.font.SysFont("consolas", 30)
score = 0
WHITE = (150, 150, 150)
RED = (150, 0, 0)
pygame.init()

win = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
snake_pos = [[WIDTH//1, HEIGHT//1]]
snake_speed = [0, BLOCK_SIZE]

teleport_walls = True
def generate_food():
    while True:
        x = random.randint(0, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE ) * BLOCK_SIZE
        y = random.randint(0, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE ) * BLOCK_SIZE
        food_pos = [x, y]
        if food_pos not in snake_pos:
            return food_pos
food_pos = generate_food()

def draw_objects():
    win.fill((0, 0, 0))
    pygame.draw.circle(win, RED, (food_pos[0] + BLOCK_SIZE // 1.5, food_pos[1] + BLOCK_SIZE // 1), BLOCK_SIZE // 1)
    for pos in snake_pos:
        pygame.draw.circle(win, WHITE, (pos[0] + BLOCK_SIZE // 1.5, pos[1] + BLOCK_SIZE // 1), BLOCK_SIZE // 1)

    score_text = score_font.render(f"Score: {score}", True, WHITE)
    win.blit(score_text, (7, 7))


def update_snake():
    global food_pos, score
    new_head = [snake_pos[0][0] + snake_speed[0], snake_pos[0][1] + snake_speed[1]]

    if teleport_walls:
        if new_head[0] >= WIDTH:
            new_head[0] = 0
        elif new_head[0] < 0:
            new_head[0] = WIDTH - BLOCK_SIZE
        if new_head[1] >= HEIGHT:
            new_head[1] = 0
        elif new_head[1] < 0:
            new_head[1] = HEIGHT - BLOCK_SIZE
    if new_head == food_pos:
        food_pos = generate_food()
        score += 1
    else:
        snake_pos.pop()

    snake_pos.insert(0, new_head)
def game_over():
    if teleport_walls:
        return snake_pos[0] in snake_pos[1:]
    else:
        return snake_pos[0] in snake_pos[1:] or \
            snake_pos[0][0] > WIDTH - BLOCK_SIZE or \
            snake_pos[0][0] < 0 or \
            snake_pos[0][1] > HEIGHT - BLOCK_SIZE or \
            snake_pos[0][1] < 0
def game_over_screen():
    global score
    win.fill((0, 0, 0))
    game_over_font = pygame.font.SysFont("consolas", 50)
    game_over_text = game_over_font.render(f"Game Over! Score: {score}", True, WHITE)
    win.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3 - game_over_text.get_height() // 3))
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    run()  # replay the game
                    return
                elif event.key == pygame.K_q:
                    pygame.quit()  # quit the game
                    return
def run():
    global snake_speed, snake_pos, food_pos, score
    snake_pos = [[WIDTH//2, HEIGHT//2]]
    snake_speed = [0, BLOCK_SIZE]
    food_pos = generate_food()
    score = 0
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            keys = pygame.key.get_pressed()
            for key in keys:
                if keys[pygame.K_UP]:
                    if snake_speed[1] == BLOCK_SIZE:
                        continue
                    snake_speed = [0, -BLOCK_SIZE]
                if keys[pygame.K_DOWN]:
                    if snake_speed[1] == -BLOCK_SIZE:
                        continue
                    snake_speed = [0, BLOCK_SIZE]
                if keys[pygame.K_LEFT]:
                    if snake_speed[0] == BLOCK_SIZE:
                        continue
                    snake_speed = [-BLOCK_SIZE, 0]
                if keys[pygame.K_RIGHT]:
                    if snake_speed[0] == -BLOCK_SIZE:
                        continue
                    snake_speed = [BLOCK_SIZE,0]
        if game_over():
            game_over_screen()
            return
        update_snake()
        draw_objects()
        pygame.display.update()
        clock.tick(15)
if __name__ == '__main__':
    run()