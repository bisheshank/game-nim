import pygame
import random

# Define constants
WIDTH, HEIGHT = 400, 400
CELL_SIZE = 20
GRID_WIDTH, GRID_HEIGHT = WIDTH // CELL_SIZE, HEIGHT // CELL_SIZE
MINE_COUNT = 50

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.Font(None, 30)

# Define colors
BACKGROUND_COLOR = (255, 255, 255)
GRID_COLOR = (0, 0, 0)
TEXT_COLOR = (255, 0, 0)

# Create grid
grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
mines = []
revealed = [[False for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]


def generate_mines():
    global mines
    mines = []
    while len(mines) < MINE_COUNT:
        x, y = random.randint(
            0, GRID_WIDTH-1), random.randint(0, GRID_HEIGHT-1)
        if grid[y][x] != -1:
            grid[y][x] = -1
            mines.append((x, y))
            # increment cell values for adjacent cells
            for dx in range(-1, 2):
                for dy in range(-1, 2):
                    if 0 <= x+dx < GRID_WIDTH and 0 <= y+dy < GRID_HEIGHT and grid[y+dy][x+dx] != -1:
                        grid[y+dy][x+dx] += 1

    print(mines)
    print(grid)


def draw_cell(x, y, color):
    pygame.draw.rect(screen, color, (x*CELL_SIZE, y *
                     CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GRID_COLOR, (x*CELL_SIZE, y *
                     CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)


def reveal_cell(x, y):
    global revealed
    if revealed[y][x]:
        return
    revealed[y][x] = True
    draw_cell(x, y, BACKGROUND_COLOR)
    if grid[y][x] == -1:
        draw_cell(x, y, TEXT_COLOR)
        end_game(False)
    elif grid[y][x] == 0:
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                if 0 <= x+dx < GRID_WIDTH and 0 <= y+dy < GRID_HEIGHT:
                    reveal_cell(x+dx, y+dy)
    else:
        text = font.render(str(grid[y][x]), True, TEXT_COLOR)
        screen.blit(text, (x*CELL_SIZE + 4, y*CELL_SIZE + 4))


def end_game(win):
    for x, y in mines:
        if not revealed[y][x]:
            draw_cell(x, y, BACKGROUND_COLOR)
            draw_cell(x, y, TEXT_COLOR)
    if win:
        text = font.render("You win!", True, TEXT_COLOR)
    else:
        text = font.render("You lose!", True, TEXT_COLOR)
    screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 2 - 15))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()


# Generate mines and calculate cell values
generate_mines()

# Main game loop
running = True
while running:
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # Handle mouse clicks
        elif event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos[0] // CELL_SIZE, event.pos[1] // CELL_SIZE
            if event.button == 1:  # left click
                reveal_cell(x, y)
                if all(all(row) for row in revealed):
                    end_game(True)
            elif event.button == 3:  # right click
                if not revealed[y][x]:
                    draw_cell(x, y, BACKGROUND_COLOR)
                    pygame.draw.polygon(screen, TEXT_COLOR, [(x*CELL_SIZE+4, y*CELL_SIZE+4), (x*CELL_SIZE+4, y*CELL_SIZE+CELL_SIZE-4), (
                        x*CELL_SIZE+CELL_SIZE-4, y*CELL_SIZE+CELL_SIZE//2), (x*CELL_SIZE+CELL_SIZE-4, y*CELL_SIZE+CELL_SIZE-4)])
                    pygame.display.flip()
                else:
                    nearby_mines = 0
                    for dx in range(-1, 2):
                        for dy in range(-1, 2):
                            if 0 <= x+dx < GRID_WIDTH and 0 <= y+dy < GRID_HEIGHT and grid[y+dy][x+dx] == -1:
                                nearby_mines += 1
                    if nearby_mines == grid[y][x]:
                        for dx in range(-1, 2):
                            for dy in range(-1, 2):
                                if 0 <= x+dx < GRID_WIDTH and 0 <= y+dy < GRID_HEIGHT and not revealed[y+dy][x+dx]:
                                    reveal_cell(x+dx, y+dy)
                    else:
                        draw_cell(x, y, BACKGROUND_COLOR)
                        pygame.display.flip()

        # Draw grid
        screen.fill(BACKGROUND_COLOR)
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if revealed[y][x]:
                    if grid[y][x] == -1:
                        draw_cell(x, y, TEXT_COLOR)
                    elif grid[y][x] == 0:
                        draw_cell(x, y, BACKGROUND_COLOR)
                    else:
                        text = font.render(str(grid[y][x]), True, TEXT_COLOR)
                        screen.blit(text, (x*CELL_SIZE + 4, y*CELL_SIZE + 4))
                else:
                    draw_cell(x, y, BACKGROUND_COLOR)
        pygame.display.flip()

# Clean up
pygame.quit()
