import pygame
import nimsweeper as ns
import random

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

SAFE = 0
UNKNOWN = -1
MINE = -4


class Visualize:
    def __init__(self, mine_count):
        # Initialize pygame
        self.rows = ns.ROWS
        self.cols = ns.COLS
        self.mine_count = mine_count

        self.game = [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.completed = False
        self.revealed = [[False for _ in range(
            self.cols)] for _ in range(self.rows)]
        self.likely_mines = [[False for _ in range(
            self.cols)] for _ in range(self.rows)]
        self.likely_safe = [[False for _ in range(
            self.cols)] for _ in range(self.rows)]
        self.flags = [[False for _ in range(
            self.cols)] for _ in range(self.rows)]
        self.confirmed_flags = [
            [False for _ in range(self.cols)] for _ in range(self.rows)]
        self.running = True
        self.win = False
        self.switch = False  # True for game-design mode
        self.truth = [[0 for _ in range(self.cols)]
                      for _ in range(self.rows)]
        self._generate_board()

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

        self._init_buttons()
        self.cur_safe_pct, self.cur_mine_pct = 0, 0

    def draw_board(self):
        game = self.game
        self.screen.fill(self.WHITE)

        pct_font = pygame.font.Font(None, self.CELL_SIZE // 2)
        for i in range(self.BOARD_HEIGHT):
            for j in range(self.BOARD_WIDTH):
                # Draw the cell background
                pygame.draw.rect(self.screen, self.GRAY, (j*self.CELL_SIZE,
                                                          i*self.CELL_SIZE, self.CELL_SIZE, self.CELL_SIZE))

                # Draw the cell contents
                if self.completed and self.truth[i][j] == MINE:
                    self.screen.blit(
                        self.mine_image, (j*self.CELL_SIZE, i*self.CELL_SIZE))
                else:
                    if game[i][j] == MINE:
                        self.screen.blit(self.mine_image,
                                         (j*self.CELL_SIZE, i*self.CELL_SIZE))
                        self.completed = True
                    elif game[i][j] == UNKNOWN:
                        self.screen.blit(self.unknown_image,
                                         (j*self.CELL_SIZE, i*self.CELL_SIZE))
                    elif game[i][j] == SAFE:
                        pass
                    else:
                        font = pygame.font.Font(None, self.CELL_SIZE)
                        text = font.render(
                            str(game[i][j]), True, NUMBER_COLORS[game[i][j]])
                        text_rect = text.get_rect(
                            center=(j*self.CELL_SIZE+self.CELL_SIZE/2, i*self.CELL_SIZE+self.CELL_SIZE/2))
                        self.screen.blit(text, text_rect)

                    if self.likely_safe[i][j]:
                        self.screen.blit(
                            self.safe_image, (j*self.CELL_SIZE, i*self.CELL_SIZE))
                        # TODO: add text for percent likelihood of being safe (cur_safe_pct if nonzero)
                        if self.cur_safe_pct > 0:
                            color = (0, 0, 0)
                            if self.cur_safe_pct < 100:
                                color = (255, 0, 0)
                            text_surface = pct_font.render(
                                "{:.0f}%".format(self.cur_safe_pct), True, color)
                            text_rect = text_surface.get_rect(center=(
                                j*self.CELL_SIZE+self.CELL_SIZE//2, i*self.CELL_SIZE+int(self.CELL_SIZE*3/4)))
                            self.screen.blit(text_surface, text_rect)
                    if self.likely_mines[i][j]:
                        self.screen.blit(
                            self.deadly_image, (j*self.CELL_SIZE, i*self.CELL_SIZE))
                        # TODO: add text for percent likelihood of being a mine (cur_mine_pct if nonzero)
                        if self.cur_mine_pct > 0:
                            color = (0, 0, 0)
                            if self.cur_mine_pct < 100:
                                color = (255, 0, 0)
                            text_surface = pct_font.render(
                                "{:.0f}%".format(self.cur_mine_pct), True, color)
                            text_rect = text_surface.get_rect(center=(
                                j*self.CELL_SIZE+self.CELL_SIZE//2, i*self.CELL_SIZE+int(self.CELL_SIZE*3/4)))
                            self.screen.blit(text_surface, text_rect)

                    if self.flags[i][j]:
                        self.screen.blit(
                            self.flag_image, (j*self.CELL_SIZE, i*self.CELL_SIZE))
                    elif self.confirmed_flags[i][j]:
                        self.screen.blit(
                            self.flag_confirm_image, (j*self.CELL_SIZE, i*self.CELL_SIZE))
                    else:
                        pass

            if self.completed:
                self.draw_gameover()

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

        # Draw Play button
        self.screen.blit(self.play_button, self.play_button_rect)
        text = font.render("Play", True, self.WHITE)
        text_rect = text.get_rect(center=self.play_button_rect.center)
        self.screen.blit(text, text_rect)

        # Draw Design button
        self.screen.blit(self.design_button, self.design_button_rect)
        text = font.render("Design", True, self.WHITE)
        text_rect = text.get_rect(center=self.design_button_rect.center)
        self.screen.blit(text, text_rect)

        pygame.display.flip()

    def _init_buttons(self):
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

        # Create Play button
        self.play_button = pygame.Surface((100, 50))
        self.play_button.fill(self.GRAY)
        self.play_button_rect = self.play_button.get_rect(
            bottomleft=(self.WINDOW_WIDTH * 0.6, self.WINDOW_HEIGHT))

        # Create Switch button
        self.design_button = pygame.Surface((100, 50))
        self.design_button.fill(self.GRAY)
        self.design_button_rect = self.design_button.get_rect(
            bottomleft=(self.WINDOW_WIDTH * 0.2, self.WINDOW_HEIGHT))

    def draw_gameover(self):
        gameover_text = pygame.font.Font(None, 50).render(
            "You Win!" if self.win else "Game Over!", True, self.BLACK)
        gameover_rect = gameover_text.get_rect(
            center=(self.WINDOW_WIDTH // 2, self.WINDOW_HEIGHT // 2))
        pygame.draw.rect(self.screen, self.WHITE, (
            gameover_rect.left - 10, gameover_rect.top - 10, gameover_rect.width + 20, gameover_rect.height + 20))
        pygame.draw.rect(self.screen, self.BLACK, (
            gameover_rect.left - 10, gameover_rect.top - 10, gameover_rect.width + 20, gameover_rect.height + 20), 5)
        self.screen.blit(gameover_text, gameover_rect)

    def place_likely(self, likely_mines, likely_safe):
        # for i, j in likely_mines:
        #     self.game[i][j] = DEADLY if self.game[i][j] != - \
        #         2 and self.game[i][j] != CONFIRMED_FLAG else CONFIRMED_FLAG

        # for i, j in likely_safe:
        #     self.game[i][j] = SAFE
        # self.draw_board(self.game, self.mines, self.completed)

        for i, j in likely_mines:
            if not self.flags[i][j] and not self.confirmed_flags[i][j]:
                self.likely_mines[i][j] = True
            else:
                self.flags[i][j] = False
                self.confirmed_flags[i][j] = True

        for i, j in likely_safe:
            self.likely_safe[i][j] = True

    def display(self):
        # Run the game loop
        self.draw_board()
        while self.running:
            self.handle_events()
            if not self.completed:
                self.draw_board()
            else:
                self.draw_board()
                self.handle_events()

            pygame.display.flip()

        # Quit pygame
        pygame.quit()

    def handle_events(self):
        game = self.game

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONUP:
                pos = pygame.mouse.get_pos()
                col = pos[0] // self.CELL_SIZE
                row = pos[1] // self.CELL_SIZE

                if event.button == 1:  # left-click
                    # Check if Reset button was clicked
                    if self.reset_button_rect.collidepoint(pos):
                        self._handle_reset()

                    # Check if Solve button was clicked
                    elif self.solve_button_rect.collidepoint(pos):
                        self._handle_solve()

                    # Check if Switch button was clicked
                    elif self.design_button_rect.collidepoint(pos):
                        self.switch = True

                    elif self.play_button_rect.collidepoint(pos):
                        self.switch = False

                    elif row < BOARD_HEIGHT and col < BOARD_WIDTH and not self.completed:
                        if self.switch:
                            if self.confirmed_flags[row][col]:
                                self.confirmed_flags[row][col] = False
                            if self.likely_mines[row][col]:
                                self.likely_mines[row][col] = False
                            if self.likely_safe[row][col]:
                                self.likely_safe[row][col] = False
                            # alternate from values -1 to 8
                            game[row][col] = ((game[row][col] + 2) % 10) - 1
                        else:
                            if not self.confirmed_flags[row][col]:
                                if self.likely_safe[row][col]:
                                    self.likely_safe[row][col] = False
                                self._handle_play(row, col)
                            else:
                                pass

                elif event.button == 3:  # right-click
                    self._handle_right_click(game, row, col)

    def _handle_reset(self):
        self.game = [[-1 for _ in range(self.cols)] for _ in range(self.rows)]
        self.completed = False
        self.revealed = [[False for _ in range(
            self.cols)] for _ in range(self.rows)]
        self.likely_mines = [[False for _ in range(
            self.cols)] for _ in range(self.rows)]
        self.likely_safe = [[False for _ in range(
            self.cols)] for _ in range(self.rows)]
        self.running = True
        self.truth = [[0 for _ in range(self.cols)]
                      for _ in range(self.rows)]
        self.flags = [[False for _ in range(
            self.cols)] for _ in range(self.rows)]
        self.confirmed_flags = [
            [False for _ in range(self.cols)] for _ in range(self.rows)]
        self._generate_board()

    def _handle_solve(self):
        num_sols, sols = ns.solve(self.game,
                                  blanks_no_adj=False,
                                  constrain_mines=True,
                                  limit_sols=True)
        ns.print_boards(sols)
        likely_mines, mine_pct = ns.likely_mines(sols)
        likely_safe, safe_pct = ns.likely_safe(sols, self.game)
        print("num_solutions", num_sols)
        # due to non-full sampling, can't be 100% safe
        self.cur_mine_pct = mine_pct*100 if num_sols >= ns.LIMIT_SOL_SPACE else mine_pct*99
        self.cur_safe_pct = safe_pct*100
        self.place_likely(likely_mines, likely_safe)

    def _handle_right_click(self, game, row, col):
        if self.switch:
            if self.confirmed_flags[row][col]:
                self.confirmed_flags[row][col] = False

        if self.flags[row][col]:
            self.flags[row][col] = False
        elif game[row][col] == UNKNOWN:
            self.flags[row][col] = True
        self.draw_board()

    def _handle_play(self, x, y):
        if self.truth[x][y] == MINE:
            self.game[x][y] = self.truth[x][y]
            self.completed = True
        else:
            self._reveal(x, y)
        if all(all(row) for row in self.revealed):
            self.completed = True
            self.win = True

    def _reveal(self, x, y):
        if self.revealed[x][y]:  # If the cell has already been revealed, do nothing
            return

        self.revealed[x][y] = True
        self.game[x][y] = self.truth[x][y]
        self.draw_board()

        if self.truth[x][y] == SAFE:
            for dx in range(-1, 2):  # if its unknown
                for dy in range(-1, 2):
                    if 0 <= x+dx < self.rows and 0 <= y+dy < self.cols:
                        self._reveal(x+dx, y+dy)

    def _generate_board(self):
        self.mines = []
        while len(self.mines) < self.mine_count:
            x, y = random.randint(
                0, self.rows-1), random.randint(0, self.cols-1)
            if self.truth[x][y] != MINE:
                self.truth[x][y] = MINE
                self.mines.append((x, y))
                # increment cell values for adjacent cells
                for dx in range(-1, 2):
                    for dy in range(-1, 2):
                        if 0 <= x+dx < self.rows and 0 <= y+dy < self.cols and self.truth[x+dx][y+dy] != MINE:
                            self.truth[x+dx][y+dy] += 1


def run(mine_count):
    v = Visualize(mine_count)
    v.display()
