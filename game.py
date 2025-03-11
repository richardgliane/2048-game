import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
WINDOW_SIZE = 600
GRID_SIZE = 4
CELL_SIZE = WINDOW_SIZE // GRID_SIZE
PADDING = 10

# Colors
BACKGROUND_COLOR = (250, 248, 239)
GRID_COLOR = (187, 173, 160)
EMPTY_CELL_COLOR = (205, 193, 180)

TILE_COLORS = {
    0: (205, 193, 180),
    2: (238, 228, 218),
    4: (237, 224, 200),
    8: (242, 177, 121),
    16: (245, 149, 99),
    32: (246, 124, 95),
    64: (246, 94, 59),
    128: (237, 207, 114),
    256: (237, 204, 97),
    512: (237, 200, 80),
    1024: (237, 197, 63),
    2048: (237, 194, 46)
}

TEXT_COLORS = {
    2: (119, 110, 101),
    4: (119, 110, 101),
    8: (249, 246, 242),
    16: (249, 246, 242),
    32: (249, 246, 242),
    64: (249, 246, 242),
    128: (249, 246, 242),
    256: (249, 246, 242),
    512: (249, 246, 242),
    1024: (249, 246, 242),
    2048: (249, 246, 242)
}

class Game2048:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("2048")
        self.grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.font = pygame.font.Font(None, 72)
        self.score = 0
        self.add_new_tile()
        self.add_new_tile()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.grid[i][j] = 2 if random.random() < 0.9 else 4

    def draw_tile(self, value, x, y):
        # Draw tile background
        rect = pygame.Rect(x + PADDING, y + PADDING, CELL_SIZE - 2*PADDING, CELL_SIZE - 2*PADDING)
        pygame.draw.rect(self.screen, TILE_COLORS.get(value, TILE_COLORS[2048]), rect, border_radius=8)

        if value != 0:
            # Draw text
            color = TEXT_COLORS.get(value, TEXT_COLORS[2048])
            text = self.font.render(str(value), True, color)
            text_rect = text.get_rect(center=(x + CELL_SIZE//2, y + CELL_SIZE//2))
            self.screen.blit(text, text_rect)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        
        # Draw grid background
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                pygame.draw.rect(self.screen, GRID_COLOR,
                               (j*CELL_SIZE, i*CELL_SIZE, CELL_SIZE, CELL_SIZE))
                self.draw_tile(self.grid[i][j], j*CELL_SIZE, i*CELL_SIZE)

        pygame.display.flip()

    def move(self, direction):
        moved = False
        merged = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]

        if direction in ['UP', 'DOWN']:
            for j in range(GRID_SIZE):
                for i in range(GRID_SIZE) if direction == 'UP' else range(GRID_SIZE-1, -1, -1):
                    if self.grid[i][j] != 0:
                        row = i
                        while True:
                            next_row = row + (-1 if direction == 'UP' else 1)
                            if 0 <= next_row < GRID_SIZE:
                                if self.grid[next_row][j] == 0:
                                    self.grid[next_row][j] = self.grid[row][j]
                                    self.grid[row][j] = 0
                                    row = next_row
                                    moved = True
                                elif (self.grid[next_row][j] == self.grid[row][j] and 
                                      not merged[next_row][j] and not merged[row][j]):
                                    self.grid[next_row][j] *= 2
                                    self.score += self.grid[next_row][j]
                                    self.grid[row][j] = 0
                                    merged[next_row][j] = True
                                    moved = True
                                    break
                                else:
                                    break
                            else:
                                break

        elif direction in ['LEFT', 'RIGHT']:
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE) if direction == 'LEFT' else range(GRID_SIZE-1, -1, -1):
                    if self.grid[i][j] != 0:
                        col = j
                        while True:
                            next_col = col + (-1 if direction == 'LEFT' else 1)
                            if 0 <= next_col < GRID_SIZE:
                                if self.grid[i][next_col] == 0:
                                    self.grid[i][next_col] = self.grid[i][col]
                                    self.grid[i][col] = 0
                                    col = next_col
                                    moved = True
                                elif (self.grid[i][next_col] == self.grid[i][col] and 
                                      not merged[i][next_col] and not merged[i][col]):
                                    self.grid[i][next_col] *= 2
                                    self.score += self.grid[i][next_col]
                                    self.grid[i][col] = 0
                                    merged[i][next_col] = True
                                    moved = True
                                    break
                                else:
                                    break
                            else:
                                break

        if moved:
            self.add_new_tile()
        return moved

    def game_over(self):
        # Check if there are any empty cells
        if any(0 in row for row in self.grid):
            return False

        # Check if there are any possible merges
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                current = self.grid[i][j]
                # Check right and down neighbors
                if j < GRID_SIZE - 1 and current == self.grid[i][j + 1]:
                    return False
                if i < GRID_SIZE - 1 and current == self.grid[i + 1][j]:
                    return False
        return True

def main():
    game = Game2048()
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move('UP')
                elif event.key == pygame.K_DOWN:
                    game.move('DOWN')
                elif event.key == pygame.K_LEFT:
                    game.move('LEFT')
                elif event.key == pygame.K_RIGHT:
                    game.move('RIGHT')
                elif event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_s:
                    # Take screenshot
                    if not os.path.exists("screenshot.png"):
                        pygame.image.save(game.screen, "screenshot.png")
                        print("Screenshot saved as screenshot.png")

        game.draw()
        if game.game_over():
            font = pygame.font.Font(None, 48)
            text = font.render("Game Over!", True, (119, 110, 101))
            text_rect = text.get_rect(center=(WINDOW_SIZE//2, WINDOW_SIZE//2))
            game.screen.blit(text, text_rect)
            pygame.display.flip()

        clock.tick(60)

if __name__ == "__main__":
    main()