import pygame
from pygame.locals import *
import random
import sys
import time

# Initialize Pygame
pygame.init()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Fonts
FONT = pygame.font.SysFont("arial", 24)
SMALL_FONT = pygame.font.SysFont("arial", 18)

# Constants
BOX_SIZE = 50
MARGIN = 5
HEADER_HEIGHT = 60  # Space for level, coins, time

def create_grid(size, num_mines):
    grid = [[' ' for _ in range(size)] for _ in range(size)]  # ' ' = empty, 'M' = mine
    mines = set()
    while len(mines) < num_mines:
        row = random.randint(0, size - 1)
        col = random.randint(0, size - 1)
        if (row, col) not in mines:
            mines.add((row, col))
            grid[row][col] = 'M'
    return grid, mines

def draw_grid(screen, grid, revealed, size):
    for row in range(size):
        for col in range(size):
            x = col * (BOX_SIZE + MARGIN) + MARGIN
            y = row * (BOX_SIZE + MARGIN) + MARGIN + HEADER_HEIGHT
            rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
            if (row, col) in revealed:
                if grid[row][col] == 'M':
                    pygame.draw.rect(screen, RED, rect)  # Mine
                    text = FONT.render('M', True, WHITE)
                else:
                    pygame.draw.rect(screen, GREEN, rect)  # Empty
                    text = FONT.render('E', True, WHITE)
            else:
                pygame.draw.rect(screen, GRAY, rect)  # Hidden
                text = FONT.render('*', True, BLACK)
            screen.blit(text, (x + BOX_SIZE // 2 - 10, y + BOX_SIZE // 2 - 12))

def draw_header(screen, level, coins, time_left, width):
    header_text = f"Level: {level} | Coins: {coins} | Time Left: {time_left}s"
    text_surf = FONT.render(header_text, True, BLACK)
    screen.blit(text_surf, (10, 10))

def pause_menu(screen, width, height):
    paused = True
    while paused:
        screen.fill(WHITE)
        title = FONT.render("PAUSED", True, BLACK)
        resume = SMALL_FONT.render("Press R to Resume", True, BLACK)
        quit_text = SMALL_FONT.render("Press Q to Quit", True, BLACK)
        screen.blit(title, (width // 2 - 50, height // 2 - 50))
        screen.blit(resume, (width // 2 - 80, height // 2))
        screen.blit(quit_text, (width // 2 - 70, height // 2 + 30))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_r:
                    paused = False
                if event.key == K_q:
                    pygame.quit()
                    sys.exit()

def start_menu(screen):
    num_mines = 5
    selecting = True
    while selecting:
        screen.fill(WHITE)
        title = FONT.render("Mine Hunter", True, BLACK)
        instr = SMALL_FONT.render("Choose number of mines (1-9):", True, BLACK)
        current = FONT.render(str(num_mines), True, BLUE)
        up = SMALL_FONT.render("Press UP to increase", True, BLACK)
        down = SMALL_FONT.render("Press DOWN to decrease", True, BLACK)
        start = SMALL_FONT.render("Press ENTER to start", True, GREEN)
        screen.blit(title, (200 - 80, 50))
        screen.blit(instr, (200 - 120, 100))
        screen.blit(current, (200 - 10, 130))
        screen.blit(up, (200 - 80, 180))
        screen.blit(down, (200 - 85, 200))
        screen.blit(start, (200 - 90, 230))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_UP:
                    if num_mines < 9:
                        num_mines += 1
                elif event.key == K_DOWN:
                    if num_mines > 1:
                        num_mines -= 1
                elif event.key == K_RETURN:
                    selecting = False
    return num_mines

def handle_mouse_click(pos, grid, revealed, coins, num_mines, size, screen, width, height, start_time):
    x, y = pos
    y -= HEADER_HEIGHT
    if y < 0:
        return None, coins, start_time
    col = x // (BOX_SIZE + MARGIN)
    row = y // (BOX_SIZE + MARGIN)
    if 0 <= row < size and 0 <= col < size and (row, col) not in revealed:
        revealed.add((row, col))
        if grid[row][col] == 'M':
            screen.fill(WHITE)
            lose_text = FONT.render("You clicked a mine! Game Over!", True, RED)
            screen.blit(lose_text, (width // 2 - 150, height // 2))
            pygame.display.flip()
            pygame.time.wait(2000)
            return False, coins, start_time
        else:
            if start_time is None:
                start_time = time.time()
            if len(revealed) == size * size - num_mines:
                screen.fill(WHITE)
                win_text = FONT.render("Level Complete!", True, GREEN)
                screen.blit(win_text, (width // 2 - 100, height // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                return True, coins, start_time
    return None, coins, start_time

def play_level(screen, level, coins, num_mines):
    size = 5 + level
    if num_mines >= size * size:
        num_mines = size * size - 1
    grid, mines = create_grid(size, num_mines)
    revealed = set()
    start_time = None
    time_limit = 180  # 3 minutes

    width = size * (BOX_SIZE + MARGIN) + MARGIN
    height = size * (BOX_SIZE + MARGIN) + MARGIN + HEADER_HEIGHT
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(f"Mine Hunter - Level {level}")

    clock = pygame.time.Clock()
    running = True
    paused = False

    while running:
        if start_time is not None:
            elapsed = time.time() - start_time
            if elapsed > time_limit:
                screen.fill(WHITE)
                over_text = FONT.render("Time's Up! Game Over!", True, RED)
                screen.blit(over_text, (width // 2 - 100, height // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                return False, coins
            time_left = max(0, int(time_limit - elapsed))
        else:
            time_left = time_limit
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_p:
                    paused = True
                    pause_menu(screen, width, height)
                    paused = False
            elif event.type == pygame.MOUSEBUTTONDOWN and not paused:
                result, coins, start_time = handle_mouse_click(
                    event.pos, grid, revealed, coins, num_mines, size, screen, width, height, start_time
                )
                if result is not None:
                    return result, coins

        
        screen.fill(WHITE)
        draw_header(screen, level, coins, time_left, width)
        draw_grid(screen, grid, revealed, size)
        pygame.display.flip()
        clock.tick(60)

def main():
    screen = pygame.display.set_mode((400, 300))  # Initial small window
    pygame.display.set_caption("Mine Hunter")

    num_mines = start_menu(screen)

    coins = 0
    level = 1
    max_levels = 7
    
    while level <= max_levels:
        success, coins = play_level(screen, level, coins, num_mines)
        if not success:
            screen.fill(WHITE)
            over_text = FONT.render(f"Game Over! Coins: {coins}", True, RED)
            screen.blit(over_text, (200, 150))
            pygame.display.flip()
            pygame.time.wait(3000)
            break
        level += 1
    else:
        screen.fill(WHITE)
        win_text = FONT.render(f"Congratulations! Coins: {coins}", True, GREEN)
        screen.blit(win_text, (200, 150))
        pygame.display.flip()
        pygame.time.wait(3000)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()