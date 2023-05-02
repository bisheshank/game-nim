import pygame

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Define dimensions
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 600
CELL_SIZE = 50
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

# Initialize pygame
pygame.init()

# Create the window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Minesweeper Visualizer")

# Load images
unknown_image = pygame.image.load("unknown.png").convert_alpha()
mine_image = pygame.image.load("mine.png").convert_alpha()
flag_image = pygame.image.load("flag.png").convert_alpha()

# Resize images to fit the cell size
unknown_image = pygame.transform.scale(unknown_image, (CELL_SIZE, CELL_SIZE))
mine_image = pygame.transform.scale(mine_image, (CELL_SIZE, CELL_SIZE))
flag_image = pygame.transform.scale(flag_image, (CELL_SIZE, CELL_SIZE))


def draw_board(game, mines, completed):
    screen.fill(WHITE)

    for i in range(BOARD_HEIGHT):
        for j in range(BOARD_WIDTH):
            # Draw the cell background
            pygame.draw.rect(screen, GRAY, (j*CELL_SIZE, i *
                             CELL_SIZE, CELL_SIZE, CELL_SIZE))

            # Draw the cell contents
            if completed and mines[(i, j)] == 1:
                screen.blit(mine_image, (j*CELL_SIZE, i*CELL_SIZE))
            else:
                if game[i][j] == -1:
                    screen.blit(unknown_image, (j*CELL_SIZE, i*CELL_SIZE))
                elif game[i][j] == -2:
                    screen.blit(flag_image, (j*CELL_SIZE, i*CELL_SIZE))
                else:
                    font = pygame.font.Font(None, CELL_SIZE)
                    text = font.render(str(game[i][j]), True, BLACK)
                    text_rect = text.get_rect(
                        center=(j*CELL_SIZE+CELL_SIZE/2, i*CELL_SIZE+CELL_SIZE/2))
                    screen.blit(text, text_rect)

    pygame.display.flip()


def main():
    game = [[-1 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    mines = {(i, j): 0 for i in range(BOARD_HEIGHT)
             for j in range(BOARD_WIDTH)}
    completed = False

    draw_board(game, mines, completed)

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        #     if event.type == pygame.MOUSEBUTTONUP:
        #         pos = pygame.mouse.get_pos()
        #         col = pos[0] // CELL_SIZE
        #         row = pos[1] // CELL_SIZE

        #         if event.button == 1:  # left-click
        #             if game[row][col] == -1:
        #                 game[row][col] = 0
        #                 draw_board(game, mines, completed)

        #         elif event.button == 3:  # right-click
        #             if game[row][col] == -1:
        #                 game[row][col] = -2
        #             elif game[row][col] == -2:
        #                 game[row][col] = -1

        # draw_board(game, mines, completed)


# Quit pygam
pygame.quit()
