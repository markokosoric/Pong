import pygame
import sys
import os

screen_width, screen_height = 800, 600
white = (255, 255, 255)
black = (0, 0, 0)
fps = 60

paddle_width, paddle_height = 10, 100
ball_size = 20
paddle_speed = 7
ball_speed_x = 5
ball_speed_y = 5
highscore_file = "highscore.txt"

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, paddle_width, paddle_height)
    
    def move(self, up_key, down_key):
        keys = pygame.key.get_pressed()
        if keys[up_key] and self.rect.top > 0:
            self.rect.y -= paddle_speed
        if keys[down_key] and self.rect.bottom < screen_height:
            self.rect.y += paddle_speed
    
    def draw(self, screen):
        pygame.draw.rect(screen, white, self.rect)

class Ball:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ball_size, ball_size)
        self.speed_x = ball_speed_x
        self.speed_y = ball_speed_y
    
    def move(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top <= 0 or self.rect.bottom >= screen_height:
            self.speed_y *= -1

    def check_collision(self, left_paddle, right_paddle):
        if self.rect.colliderect(left_paddle.rect) and self.speed_x < 0:
            self.speed_x *= -1
        if self.rect.colliderect(right_paddle.rect) and self.speed_x > 0:
            self.speed_x *= -1

    def reset(self):
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.speed_x *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, white, self.rect)

class PongGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((screen_width, screen_height))
        pygame.display.set_caption("Two-Player Pong")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)

        self.left_paddle = Paddle(50, screen_height // 2 - paddle_height // 2)
        self.right_paddle = Paddle(screen_width - 50 - paddle_width, screen_height // 2 - paddle_height // 2)
        self.ball = Ball(screen_width // 2 - ball_size // 2, screen_height // 2 - ball_size // 2)

        self.left_score = 0
        self.right_score = 0
        self.highscore = self.load_highscore()

    def load_highscore(self):
        return int(open(highscore_file).read()) if os.path.exists(highscore_file) else 0

    def save_highscore(self):
        open(highscore_file, "w").write(str(self.highscore))

    def handle_input(self):
        self.left_paddle.move(pygame.K_w, pygame.K_s)
        self.right_paddle.move(pygame.K_UP, pygame.K_DOWN)

    def update(self):
        self.ball.move()
        self.ball.check_collision(self.left_paddle, self.right_paddle)

        if self.ball.rect.left <= 0:
            self.right_score += 1
            self.ball.reset()
        if self.ball.rect.right >= screen_width:
            self.left_score += 1
            self.ball.reset()

        current_max = max(self.left_score, self.right_score)
        if current_max > self.highscore:
            self.highscore = current_max
            self.save_highscore()

    def draw(self):
        self.screen.fill(black)
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        pygame.draw.aaline(self.screen, white, (screen_width // 2, 0), (screen_width // 2, screen_height))

        left_text = self.font.render(str(self.left_score), True, white)
        right_text = self.font.render(str(self.right_score), True, white)
        highscore_text = self.font.render("Highscore: " + str(self.highscore), True, white)

        self.screen.blit(left_text, (screen_width // 4 - left_text.get_width() // 2, 20))
        self.screen.blit(right_text, (3 * screen_width // 4 - right_text.get_width() // 2, 20))
        self.screen.blit(highscore_text, (screen_width // 2 - highscore_text.get_width() // 2, 20))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            self.clock.tick(fps)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.handle_input()
            self.update()
            self.draw()
        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = PongGame()
    game.run()
