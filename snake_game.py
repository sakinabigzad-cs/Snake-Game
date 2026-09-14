import pygame
import random
import sys
pygame.init()
WIDTH, HEIGHT = 600, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
DARK_GREEN = (0, 180, 0)
RED = (255, 50, 50)
GRAY = (40, 40, 40)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 25)
big_font = pygame.font.SysFont("arial", 50)
class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.grow = False
        self.score = 0
    def get_head(self):
        return self.positions[0]
    def move(self):
        head_x, head_y = self.get_head()
        dx, dy = self.direction
        new_head = ((head_x + dx) % GRID_WIDTH, (head_y + dy) % GRID_HEIGHT)
        if new_head in self.positions[1:]:
            return False
        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            self.score += 1
        return True
    def change_direction(self, new_dir):
        if (new_dir[0] * -1, new_dir[1] * -1) != self.direction:
            self.direction = new_dir
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            color = GREEN if i == 0 else DARK_GREEN
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1)
            pygame.draw.rect(surface, color, rect)
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.randomize()
    def randomize(self):
        self.position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE - 1, GRID_SIZE - 1)
        pygame.draw.rect(surface, RED, rect)
def draw_grid(surface):
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))
def show_text(surface, text, font, color, x, y):
    label = font.render(text, True, color)
    surface.blit(label, (x, y))
def game_over_screen(score, high_score):
    screen.fill(BLACK)
    show_text(screen, "GAME OVER", big_font, RED, WIDTH//2 - 130, HEIGHT//2 - 80)
    show_text(screen, f"Score: {score}", font, WHITE, WIDTH//2 - 50, HEIGHT//2 - 10)
    show_text(screen, f"High Score: {high_score}", font, WHITE, WIDTH//2 - 70, HEIGHT//2 + 30)
    show_text(screen, "Press SPACE to Play Again", font, GREEN, WIDTH//2 - 130, HEIGHT//2 + 80)
    show_text(screen, "Press ESC to Quit", font, WHITE, WIDTH//2 - 90, HEIGHT//2 + 120)
    pygame.display.flip()
def main():
    snake = Snake()
    food = Food()
    high_score = 0
    running = True
    game_active = True
    while running:
        clock.tick(10)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if game_active:
                    if event.key == pygame.K_UP:
                        snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction((1, 0))
                else:
                    if event.key == pygame.K_SPACE:
                        snake = Snake()
                        food = Food()
                        game_active = True
                    elif event.key == pygame.K_ESCAPE:
                        running = False

        if game_active:
            if not snake.move():
                game_active = False
                if snake.score > high_score:
                    high_score = snake.score

            if snake.get_head() == food.position:
                snake.grow = True
                food.randomize()
                while food.position in snake.positions:
                    food.randomize()
            screen.fill(BLACK)
            draw_grid(screen)
            snake.draw(screen)
            food.draw(screen)
            show_text(screen, f"Score: {snake.score}", font, WHITE, 10, 10)
            show_text(screen, f"High: {high_score}", font, WHITE, WIDTH - 120, 10)
            pygame.display.flip()
        else:
            game_over_screen(snake.score, high_score)

    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()