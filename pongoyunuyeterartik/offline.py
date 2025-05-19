import random
import pygame
import sys
import json


window_width = 1000
window_height = 700
bat_width = 20
bat_height = 100
bat_movement_speed = 20
ball_diameter = 20
game_speed = 50

WHITE = (255, 255, 255)
BG_COLOR = (30, 30, 30)
PLAYER1_COLOR = (243, 6, 6)
PLAYER2_COLOR = (0, 0, 255)
SCORE_COLOR_1 = (144, 238, 144)
SCORE_COLOR_2 = (255, 185, 127)

pygame.init()
pygame.font.init()

win = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("Offline Pong")
font = pygame.font.SysFont('Arial', 30)
clock = pygame.time.Clock()
background_image = pygame.image.load("görselişte.jpg")
background_image = pygame.transform.scale(background_image, (window_width, window_height))


class Bat:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = bat_width
        self.height = bat_height
        self.points = 0

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == 'up' and self.y > 0:
            self.y -= bat_movement_speed
        elif direction == 'down' and self.y < (window_height - self.height):
            self.y += bat_movement_speed

    def add_point(self):
        self.points += 1


class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.radius = ball_diameter // 2
        self.velocity_x = 6 * random.choice([-1, 1])
        self.velocity_y = 3 * random.choice([-1, 1])

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), self.radius)

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

    def reset(self):
        self.x = window_width // 2
        self.y = window_height // 2
        self.velocity_x *= -1
        self.velocity_y = 1 * random.choice([-1, 1])


player1 = Bat(10, window_height // 2 - bat_height // 2, PLAYER1_COLOR)
player2 = Bat(window_width - 10 - bat_width, window_height // 2 - bat_height // 2, PLAYER2_COLOR)
ball = Ball(window_width // 2, window_height // 2, WHITE)

run = True

while run:
    clock.tick(game_speed)
    win.blit(background_image, (0, 0))


    for i in range(0, window_height, 40):
        pygame.draw.rect(win, WHITE, (window_width // 2 - 2, i, 4, 20))


    player1.draw(win)
    player2.draw(win)
    ball.draw(win)


    p1_score_text = font.render(str(player1.points), True, SCORE_COLOR_1)
    p2_score_text = font.render(str(player2.points), True, SCORE_COLOR_2)
    win.blit(p1_score_text, (window_width // 4 - p1_score_text.get_width() // 2, 20))
    win.blit(p2_score_text, (3 * window_width // 4 - p2_score_text.get_width() // 2, 20))

    pygame.display.update()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        run = False
    if keys[pygame.K_w]:
        player1.move('up')
    if keys[pygame.K_s]:
        player1.move('down')
    if keys[pygame.K_UP]:
        player2.move('up')
    if keys[pygame.K_DOWN]:
        player2.move('down')


    ball.move()


    if ball.y - ball.radius <= 0 or ball.y + ball.radius >= window_height:
        ball.velocity_y *= -1


    ball_rect = pygame.Rect(ball.x - ball.radius, ball.y - ball.radius, ball.radius*2, ball.radius*2)
    player1_rect = pygame.Rect(player1.x, player1.y, player1.width, player1.height)
    player2_rect = pygame.Rect(player2.x, player2.y, player2.width, player2.height)

    if ball_rect.colliderect(player1_rect) and ball.velocity_x < 0:
        ball.velocity_x *= -1
    if ball_rect.colliderect(player2_rect) and ball.velocity_x > 0:
        ball.velocity_x *= -1


    if ball.x - ball.radius <= 0:
        player2.add_point()
        ball.reset()
    if ball.x + ball.radius >= window_width:
        player1.add_point()
        ball.reset()

    file = "keep_score.json"
    if player1.points >= 3 or player2.points >= 3:
        winner = "Left Player" if player1.points >= 10 else "Right Player"
        with open(file, "r", encoding="utf-8") as f:
            scores = json.load(f)
        if winner == "Left Player":
            scores["player1"] += 1
        elif winner == "Right Player":
            scores["player2"] += 1
        with open(file, "w", encoding="utf-8") as f:
            json.dump(scores, f, ensure_ascii=False, indent=4)

        win.fill((10, 10, 30))
        font_big = pygame.font.SysFont("Arial", 72)
        winner_text = font_big.render(f"Winner: {winner}", True, WHITE)
        win.blit(winner_text,
                    (window_width // 2 - winner_text.get_width() // 2, window_height // 2 - winner_text.get_height() // 2))
        pygame.display.flip()

        pygame.time.delay(1000)
        pygame.quit()
        sys.exit()

pygame.quit()
sys.exit()
