import pickle
import random
import socket
import pygame

x=1000
y=700
window_width = x
window_height = y
player1_start_x = 10
player1_start_y = 300
player2_start_x = x-30
player2_start_y = 300
ball_start_x = x/2
ball_start_y = y/2
ball_start_velocity_x = 3
ball_start_velocity_y = 1
bat_width = 20
bat_height = 100
bat_movement_speed = 20
ball_diameter = 20

data_size = 4096


game_speed = 50


class PongDTO:
    def __init__(self):
        self.game_id = 0
        self.player_id = 0
        self.player_x = []
        self.player_y = []
        self.ball_x = 0
        self.ball_y = 0
        self.ball_velocity_x = 0
        self.ball_velocity_y = 0
        self.ball_direction_x = ''
        self.ball_direction_y = ''
        self.start_play = False
        self.msg = ''
        self.end_play = False
        self.points = [0, 0]


class Bat:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = bat_width
        self.height = bat_height
        self.points = 0

    def draw(self, window):
        glow_color = (min(self.color[0] + 100, 255), min(self.color[1] + 100, 255), min(self.color[2] + 100, 255))
        for i in range(4, 0, -1):
            pygame.draw.rect(
                window,
                glow_color,
                (self.x - i, self.y - i, self.width + 2 * i, self.height + 2 * i),
                border_radius=8
            )

        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))

    def move(self, direction):
        if direction == 'up' and self.y > (bat_movement_speed / 2):
            self.y -= bat_movement_speed
        elif direction == 'down' and self.y < (window_height - bat_height - (bat_movement_speed / 2)):
            self.y += bat_movement_speed

    def add_point(self):
        self.points += 1


class Ball:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.width = ball_diameter
        self.velocity_x = ball_start_velocity_x
        self.velocity_y = ball_start_velocity_y
        self.direction_x = random.choice(('positive', 'negative'))
        self.direction_y = random.choice(('positive', 'negative'))

    def draw(self, window):
        pygame.draw.circle(window, self.color, (self.x, self.y), (ball_diameter // 2))


def update_bat_ball(dto):
    bats[player_id].color = (243,6,6)
    bats[opponent_id].color = (0,0,255)

    bats[0].x = dto.player_x[0]
    bats[0].y = dto.player_y[0]
    bats[1].x = dto.player_x[1]
    bats[1].y = dto.player_y[1]
    ball.x = dto.ball_x
    ball.y = dto.ball_y
    ball.color = (255, 255, 255)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server = "192.168.204.227"
port = 12345
addr = (server, port)
client.connect(addr)
receive_dto = pickle.loads(client.recv(data_size))
print("You are player ", receive_dto.player_id+1)

player_id = receive_dto.player_id
opponent_id = list({0, 1} - {receive_dto.player_id})[0]

bats = [Bat(0, 0, (0, 0, 0)), Bat(0, 0, (0, 0, 0))]
ball = Ball(0, 0, (0, 0, 0))

update_bat_ball(receive_dto)
pygame.font.init()
background_image = pygame.image.load("görselişte.jpg")
background_image = pygame.transform.scale(background_image, (window_width, window_height))
win = pygame.display.set_mode((window_width, window_height))
font = pygame.font.SysFont('Arial', 30)

run = True
clock = pygame.time.Clock()

while run:
    clock.tick(game_speed)
    win.blit(background_image, (0, 0))


    for i in range(0, window_height, 40):
        pygame.draw.rect(win, (255, 255, 255), (window_width // 2 - 2, i, 4, 20))


    bats[0].draw(win)
    bats[1].draw(win)
    ball.draw(win)


    p1_score_text = font.render(str(receive_dto.points[0]), True, (144, 238, 144))
    p2_score_text = font.render(str(receive_dto.points[1]), True, (255, 185, 127))
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
            bats[player_id].move('up')
        if keys[pygame.K_s]:
            bats[player_id].move('down')
        if event.type == pygame.MOUSEBUTTONDOWN:
            run = False

    receive_dto.player_y[0] = bats[0].y
    receive_dto.player_y[1] = bats[1].y

    try:
        client.sendall(pickle.dumps(receive_dto))
        receive_dto = pickle.loads(client.recv(data_size))
    except Exception as e:
        run = False
        print("Couldn't get game")
        print("An error occurred:", e)
        break

    update_bat_ball(receive_dto)
