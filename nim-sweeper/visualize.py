import pygame
import nimsweeper as ns

# Define dimensions
WINDOW_WIDTH = 500
WINDOW_HEIGHT = 550
CELL_SIZE = 50
BOARD_WIDTH = 10
BOARD_HEIGHT = 10

NUMBER_COLORS = {
    1: (0, 0, 255),  # blue
    2: (0, 255, 0),  # green
    3: (255, 0, 0),  # red
    4: (0, 0, 128),  # dark blue
    5: (165, 42, 42),  # brown
    6: (0, 255, 255),  # cyan
    7: (0, 0, 0),  # black
    8: (60, 60, 60)  # grey
}

SAFE = -3
DEADLY = -4
CONFIRMED_FLAG = -5


class Visualize:
    def __init__(self, game, mines, completed):
        # Initialize pygame

        self.game = game
        self.mines = mines
        self.completed = completed

        self.WINDOW_WIDTH = WINDOW_WIDTH
        self.WINDOW_HEIGHT = WINDOW_HEIGHT
        self.CELL_SIZE = CELL_SIZE
        self.BOARD_HEIGHT = BOARD_HEIGHT
        self.BOARD_WIDTH = BOARD_WIDTH

        # Define colors
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)
        self.GRAY = (128, 128, 128)
        self.RED = (255, 0, 0)

        pygame.init()

        # Create the window
        self.screen = pygame.display.set_mode(
            (self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Minesweeper Visualizer")

        # Load images
        self.unknown_image = pygame.image.load("unknown.png").convert_alpha()
        self.mine_image = pygame.image.load("mine.png").convert_alpha()
        self.flag_image = pygame.image.load("flag.png").convert_alpha()
        self.safe_image = pygame.image.load("safe.png").convert_alpha()
        self.deadly_image = pygame.image.load("deadly.png").convert_alpha()
        self.flag_confirm_image = pygame.image.load(
            "flag_confirmed.png").convert_alpha()

        # Resize images to fit the cell size
        self.unknown_image = pygame.transform.scale(
            self.unknown_image, (self.CELL_SIZE, self.CELL_SIZE))
        self.mine_image = pygame.transform.scale(
            self.mine_image, (self.CELL_SIZE, self.CELL_SIZE))
        self.flag_image = pygame.transform.scale(
            self.flag_image, (self.CELL_SIZE, self.CELL_SIZE))
        self.safe_image = pygame.transform.scale(
            self.safe_image, (self.CELL_SIZE, self.CELL_SIZE))
        self.deadly_image = pygame.transform.scale(
            self.deadly_image, (self.CELL_SIZE, self.CELL_SIZE))
        self.flag_confirm_image = pygame.transform.scale(
            self.flag_confirm_image, (self.CELL_SIZE, self.CELL_SIZE))

        # Create Reset button
        self.reset_button = pygame.Surface((100, 50))
        self.reset_button.fill(self.GRAY)
        self.reset_button_rect = self.reset_button.get_rect(
            bottomleft=(0, self.WINDOW_HEIGHT))

        # Create Solve button
        self.solve_button = pygame.Surface((100, 50))
        self.solve_button.fill(self.GRAY)
        self.solve_button_rect = self.solve_button.get_rect(
            bottomright=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        self.cur_safe_pct, self.cur_mine_pct = 0, 0

    def draw_board(self, game, mines, completed):
        self.screen.fill(self.WHITE)

        pct_font = pygame.font.Font(None, self.CELL_SIZE // 2)
        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                # Draw the cell background
                pygame.draw.rect(self.screen, self.GRAY, (j*self.CELL_SIZE,
                                                          i*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

                # Draw the cell contents
                if completed and mines[(i, j)] == 1:
                    self.screen.blit(
                        self.mine_image, (j*self.CELL_SIZE, i*self.CELL_SIZE))
                else:

                    if game[i][j] == -1:
                        self.screen.blit(self.unknown_image,
                                         (j*self.CELL_SIZE, i*self.CELL_SIZE))
                    elif game[i][j] == -2:
                        self.screen.blit(
                            self.flag_image, (j*self.CELL_SIZE, i*self.CELL_SIZE))
                    elif game[i][j] == SAFE:
                        self.screen.blit(
                            self.safe_image, (j*self.CELL_SIZE, i*self.CELL_SIZE))
                        # TODO: add text for percent likelihood of being safe (cur_safe_pct if nonzero)
                        if self.cur_safe_pct > 0:
                            color = (0, 0, 0)
                            if self.cur_safe_pct == 100:
                                self.cur_mine_pct = 99  # due to non-full sampling, can't be 100% safe
                                color = (255, 0, 0)
                            text_surface = pct_font.render(
                                "{:.0f}%".format(self.cur_safe_pct), True, color)
                            text_rect = text_surface.get_rect(center=(
                                j*self.CELL_SIZE+self.CELL_SIZE//2, i*self.CELL_SIZE+int(self.CELL_SIZE*3/4)))
                            self.screen.blit(text_surface, text_rect)
                    elif game[i][j] == DEADLY:
                        self.screen.blit(
                            self.deadly_image, (j*self.CELL_SIZE, i*self.CELL_SIZE))
                        # TODO: add text for percent likelihood of being a mine (cur_mine_pct if nonzero)
                        if self.cur_mine_pct > 0:
                            color = (0, 0, 0)
                            if self.cur_mine_pct == 100:
                                self.cur_mine_pct = 99  # due to non-full sampling, can't be 100% safe
                                color = (255, 0, 0)
                            text_surface = pct_font.render(
                                "{:.0f}%".format(self.cur_mine_pct), True, color)
                            text_rect = text_surface.get_rect(center=(
                                j*self.CELL_SIZE+self.CELL_SIZE//2, i*self.CELL_SIZE+int(self.CELL_SIZE*3/4)))
                            self.screen.blit(text_surface, text_rect)
                    elif game[i][j] == CONFIRMED_FLAG:
                        self.screen.blit(
                            self.flag_confirm_image, (j*self.CELL_SIZE, i*self.CELL_SIZE))

                    elif game[i][j] == 0:
                        pass
                    else:
                        font = pygame.font.Font(None, self.CELL_SIZE)
                        text = font.render(
                            str(game[i][j]), True, NUMBER_COLORS[game[i][j]])
                        text_rect = text.get_rect(
                            center=(j*self.CELL_SIZE+self.CELL_SIZE/2, i*self.CELL_SIZE+self.CELL_SIZE/2))
                        self.screen.blit(text, text_rect)

        # Draw Reset button
        self.screen.blit(self.reset_button, self.reset_button_rect)
        font = pygame.font.Font(None, 25)
        text = font.render("Reset", True, self.WHITE)
        text_rect = text.get_rect(center=self.reset_button_rect.center)
        self.screen.blit(text, text_rect)

        # Draw Solve button
        self.screen.blit(self.solve_button, self.solve_button_rect)
        text = font.render("Solve", True, self.WHITE)
        text_rect = text.get_rect(center=self.solve_button_rect.center)
        self.screen.blit(text, text_rect)

        pygame.display.flip()

    def place_likely(self, likely_mines, likely_safe):
        for i, j in likely_mines:
            self.game[i][j] = DEADLY if self.game[i][j] != - \
                2 and self.game[i][j] != CONFIRMED_FLAG else CONFIRMED_FLAG

        for i, j in likely_safe:
            self.game[i][j] = SAFE

        # self.draw_board(self.game, self.mines, self.completed)

    def run(self):
        game = self.game
        mines = self.mines
        completed = self.completed

        self.draw_board(game, mines, completed)

        # Create Reset button
        reset_button = pygame.Surface((100, 50))
        reset_button.fill(self.GRAY)
        reset_button_rect = reset_button.get_rect(
            bottomleft=(0, self.WINDOW_HEIGHT))

        # Create Solve button
        solve_button = pygame.Surface((100, 50))
        solve_button.fill(self.GRAY)
        solve_button_rect = solve_button.get_rect(
            bottomright=(self.WINDOW_WIDTH, self.WINDOW_HEIGHT))

        # Game loop
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONUP:
                    pos = pygame.mouse.get_pos()
                    col = pos[0] // self.CELL_SIZE
                    row = pos[1] // self.CELL_SIZE

                    if event.button == 1:  # left-click
                        # Check if Reset button was clicked
                        if self.reset_button_rect.collidepoint(pos):
                            game = [[-1 for _ in range(BOARD_WIDTH)]
                                    for _ in range(BOARD_HEIGHT)]
                            mines = {(i, j): 0 for i in range(BOARD_HEIGHT)
                                     for j in range(BOARD_WIDTH)}
                            completed = False

                        # Check if Solve button was clicked
                        elif self.solve_button_rect.collidepoint(pos):
                            num_sols, sols = ns.solve(game,
                                                      blanks_no_adj=False,
                                                      constrain_mines=True,
                                                      limit_sols=True)
                            ns.print_boards(sols)
                            likely_mines, mine_pct = ns.likely_mines(sols)
                            likely_safe, safe_pct = ns.likely_safe(sols, game)
                            # print(likely_mines, mine_pct)
                            # print(likely_safe, safe_pct)
                            print("num_solutions", num_sols)
                            self.cur_safe_pct, self.cur_mine_pct = safe_pct*100, mine_pct*100
                            self.place_likely(likely_mines, likely_safe)

                        elif row < BOARD_HEIGHT and col < BOARD_WIDTH:
                            if game[row][col] == SAFE or game[row][col] == DEADLY or game[row][col] == CONFIRMED_FLAG:
                                game[row][col] = -1
                            # alternate from values -1 to 8
                            game[row][col] = ((game[row][col] + 2) % 10) - 1

                    elif event.button == 3:  # right-click
                        if game[row][col] == SAFE or game[row][col] == DEADLY or game[row][col] == CONFIRMED_FLAG:
                            game[row][col] = -1
                        if game[row][col] == -1:
                            game[row][col] = -2
                        elif game[row][col] == -2:
                            game[row][col] = -1

            self.draw_board(game, mines, completed)

            pygame.display.flip()

        # Quit pygame
        pygame.quit()


if __name__ == "__main__":
    game = [[-1 for _ in range(BOARD_WIDTH)] for _ in range(BOARD_HEIGHT)]
    mines = {(i, j): 0 for i in range(BOARD_HEIGHT)
             for j in range(BOARD_WIDTH)}
    completed = False
    v = Visualize(game, mines, completed)
    v.run()
