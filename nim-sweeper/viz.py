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


def explore_empty_cells(game, row, col):
    if game[row][col] != 0:
        return

    game[row][col] = -3  # mark as explored

    # explore adjacent cells
    for i in range(max(0, row-1), min(BOARD_HEIGHT, row+2)):
        for j in range(max(0, col-1), min(BOARD_WIDTH, col+2)):
            if game[i][j] != -2 and game[i][j] != -3:  # not flagged or explored
                explore_empty_cells(game, i, j)


def handle_click(game, row, col):
    rows = len(game)
    cols = len(game[0])
    if game[row][col] == -1:
        explore_empty_cells(game, row, col)
    elif game[row][col] == 0:
        return
    else:
        adjacents = [(row + r, col + c) for r in [-1, 0, 1]
                     for c in [-1, 0, 1] if r != 0 or c != 0]
        adj_mine_count = sum(1 for r, c in adjacents if 0 <=
                             r < rows and 0 <= c < cols and game[r][c] == -1)
        game[row][col] = adj_mine_count


def main():
    game = [[-1 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    mines = {(i, j): 0 for i in range(BOARD_HEIGHT)
             for j in range(BOARD_WIDTH)}
    completed = False

    draw_board(game, mines, completed)

    # Create Reset button
    reset_button = pygame.Surface((100, 50))
    reset_button.fill(GRAY)
    reset_button_rect = reset_button.get_rect(
        bottomleft=(0, WINDOW_HEIGHT))

    # Create Solve button
    solve_button = pygame.Surface((100, 50))
    solve_button.fill(GRAY)
    solve_button_rect = solve_button.get_rect(
        bottomright=(WINDOW_WIDTH, WINDOW_HEIGHT))

    # Game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                col = pos[0] // CELL_SIZE
                row = pos[1] // CELL_SIZE

                if event.button == 1:  # left-click
                    if game[row][col] == -1:
                        game[row][col] = 0
                        draw_board(game, mines, completed)

                elif event.button == 3:  # right-click
                    if game[row][col] == -1:
                        game[row][col] = -2
                    elif game[row][col] == -2:
                        game[row][col] = -1

                # Check if Reset button was clicked
                if reset_button_rect.collidepoint(pos):
                    game = [[-1 for _ in range(BOARD_WIDTH)]
                            for _ in range(BOARD_HEIGHT)]
                    completed = False
                    draw_board(game, mines, completed)

                # Check if Solve button was clicked
                if solve_button_rect.collidepoint(pos):
                    # TODO: Implement board solver
                    pass

        draw_board(game, mines, completed)

        # Draw Reset button
        screen.blit(reset_button, reset_button_rect)
        font = pygame.font.Font(None, 25)
        text = font.render("Reset", True, WHITE)
        text_rect = text.get_rect(center=reset_button_rect.center)
        screen.blit(text, text_rect)

        # Draw Solve button
        screen.blit(solve_button, solve_button_rect)
        text = font.render("Solve", True, WHITE)
        text_rect = text.get_rect(center=solve_button_rect.center)
        screen.blit(text, text_rect)

        pygame.display.flip()


if __name__ == "__main__":
    main()

# Quit pygame
pygame.quit()
