import random
import socket
from _thread import *
import pickle
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


class Game:

    game_id = 0

    player_ids = []

    game_dto = PongDTO()

    def __init__(self):

        self.game_id = 0
        self.player_ids = []
        self.game_dto = PongDTO()

    def initiate_dto(self):

        self.game_dto.player_x = [player1_start_x, player2_start_x]
        self.game_dto.player_y = [player1_start_y, player2_start_y]
        self.game_dto.ball_x = ball_start_x
        self.game_dto.ball_y = ball_start_x
        self.game_dto.ball_velocity_x = ball_start_velocity_x
        self.game_dto.ball_velocity_y = ball_start_velocity_y

        self.game_dto.ball_direction_x = random.choice(('positive', 'negative'))
        self.game_dto.ball_direction_y = random.choice(('positive', 'negative'))
        self.game_dto.game_id = self.game_id
        self.game_dto.start_play = False
        self.game_dto.points = [0, 0]


def get_game_dto(game_id):

    for game in game_ids:

        if game_id == game.game_id:
            return game.game_dto


def get_game(game_id):

    for game in game_ids:

        if game_id == game.game_id:
            return game


def update_game_dto(dto):

    game_dto = get_game_dto(dto.game_id)
    game_dto.player_y[dto.player_id] = dto.player_y[dto.player_id]


def update_game_state(dto):

    game_dto = get_game_dto(dto.game_id)
    game_dto.player_y[dto.player_id] = dto.player_y[dto.player_id]
    if game_dto.ball_x < (player2_start_x - (ball_diameter / 2) - game_dto.ball_velocity_x) \
            and game_dto.ball_direction_x == 'positive':

        game_dto.ball_x += game_dto.ball_velocity_x

    elif game_dto.ball_x > (player1_start_x + bat_width + (ball_diameter / 2) + game_dto.ball_velocity_x) \
            and game_dto.ball_direction_x == 'negative':

        game_dto.ball_x -= game_dto.ball_velocity_x

    elif game_dto.ball_x <= (player1_start_x + bat_width + (ball_diameter / 2) + game_dto.ball_velocity_x) \
            and game_dto.ball_direction_x == 'negative':
        if dto.player_y[0] <= game_dto.ball_y <= (dto.player_y[0] + bat_height):
            if (dto.player_y[0] + (bat_height * 0.25)) > game_dto.ball_y >= dto.player_y[0]:
                game_dto.ball_velocity_y = 5
                game_dto.ball_direction_y = 'negative'
            elif (dto.player_y[0] + (bat_height * 0.5)) > game_dto.ball_y >= (dto.player_y[0] + (bat_height * 0.25)):
                game_dto.ball_velocity_y = 4
                game_dto.ball_direction_y = 'negative'
            elif (dto.player_y[0] + (bat_height * 0.75)) > game_dto.ball_y >= (dto.player_y[0] + (bat_height * 0.5)):
                game_dto.ball_velocity_y = 4
                game_dto.ball_direction_y = 'positive'
            elif (dto.player_y[0] + bat_height) >= game_dto.ball_y >= (dto.player_y[0] + (bat_height * 0.75)):
                game_dto.ball_velocity_y = 5
                game_dto.ball_direction_y = 'positive'
            game_dto.ball_direction_x = 'positive'
        else:
            game_dto.ball_x = ball_start_x
            game_dto.ball_y = ball_start_y
            game_dto.ball_velocity_x = ball_start_velocity_x
            game_dto.ball_velocity_y = ball_start_velocity_y
            game_dto.ball_direction_x = random.choice(('positive', 'negative'))
            game_dto.ball_direction_y = random.choice(('positive', 'negative'))

            game_dto.points[1] += 1

    elif game_dto.ball_x >= (player2_start_x - (ball_diameter / 2) - game_dto.ball_velocity_x) \
            and game_dto.ball_direction_x == 'positive':

        if dto.player_y[1] <= game_dto.ball_y <= (dto.player_y[1] + bat_height):

            if (dto.player_y[1] + bat_height * 0.25) > game_dto.ball_y >= dto.player_y[1]:
                game_dto.ball_velocity_y = 5
                game_dto.ball_direction_y = 'negative'
            elif (dto.player_y[1] + bat_height * 0.5) > game_dto.ball_y >= (dto.player_y[1] + bat_height * 0.25):
                game_dto.ball_velocity_y = 4
                game_dto.ball_direction_y = 'negative'
            elif (dto.player_y[1] + bat_height * 0.75) > game_dto.ball_y >= (dto.player_y[1] + bat_height * 0.5):
                game_dto.ball_velocity_y = 4
                game_dto.ball_direction_y = 'positive'
            elif (dto.player_y[1] + bat_height) >= game_dto.ball_y >= (dto.player_y[1] + bat_height * 0.75):
                game_dto.ball_velocity_y = 5
                game_dto.ball_direction_y = 'positive'
            game_dto.ball_direction_x = 'negative'
        else:
            game_dto.ball_x = ball_start_x
            game_dto.ball_y = ball_start_y
            game_dto.ball_velocity_x = ball_start_velocity_x
            game_dto.ball_velocity_y = ball_start_velocity_y
            game_dto.ball_direction_x = random.choice(('positive', 'negative'))
            game_dto.ball_direction_y = random.choice(('positive', 'negative'))
            game_dto.points[0] += 1

    if game_dto.ball_y < (window_height - (ball_diameter / 2) - game_dto.ball_velocity_y) \
            and game_dto.ball_direction_y == 'positive':
        game_dto.ball_y += game_dto.ball_velocity_y
    elif game_dto.ball_y > ((ball_diameter / 2) + game_dto.ball_velocity_y) \
            and game_dto.ball_direction_y == 'negative':
        game_dto.ball_y -= game_dto.ball_velocity_y
    elif game_dto.ball_y <= ((ball_diameter / 2) + game_dto.ball_velocity_y) \
            and game_dto.ball_direction_y == 'negative':
        game_dto.ball_direction_y = 'positive'
    elif game_dto.ball_y >= (window_height - (ball_diameter / 2) - game_dto.ball_velocity_y) \
            and game_dto.ball_direction_y == 'positive':
        game_dto.ball_direction_y = 'negative'


def get_game_player_id():

    game_id = 0
    player_id = 0

    if len(game_ids) == 0:
        game = Game()
        game.game_id = game_id
        game.player_ids.append(player_id)

        game.initiate_dto()

        game_ids.append(game)
        return game_id, player_id
    else:
        found = False

        for game in game_ids:

            if len(game.player_ids) == 1:
                found = True

                player_id = list({0, 1} - set(game.player_ids))[0]
                game.player_ids.append(player_id)

                game.game_dto.start_play = True
                break

        if not found:
            game_id = game_ids[-1].game_id + 1
            game = Game()
            game.game_id = game_id
            player_id = 0
            game.player_ids.append(player_id)
            game.initiate_dto()
            game_ids.append(game)

        return game_id, player_id


def threaded_client(conn, game_id, player_id):

    send_dto = get_game_dto(game_id)

    send_dto.player_id = player_id
    send_dto.msg = "Welcome to game " + str(game_id) + ", Player " + str(player_id)

    conn.send(pickle.dumps(send_dto))

    run = True
    clock = pygame.time.Clock()

    while run:

        clock.tick(game_speed)
        try:

            receive_dto = pickle.loads(conn.recv(data_size))
            if not receive_dto:
                print('DTO not received')
                run = False
            else:
                receive_dto.player_id = player_id
                if receive_dto.start_play:
                    update_game_state(receive_dto)
                else:
                    update_game_dto(receive_dto)
                game_dto = get_game_dto(game_id)
                game_dto.player_id = player_id
                conn.sendall(pickle.dumps(game_dto))
        except Exception as e:
            run = False
            print("An error occurred:", e)

    print("Lost connection")
    game = get_game(game_id)
    game.player_ids.remove(player_id)
    if len(game.player_ids) == 0:
        game_ids.remove(game)
    else:
        game.initiate_dto()
    conn.close()


server = "0.0.0.0"
port = 12345
print(server,port)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    print("hata burda")
    exit()

s.listen()
print("Waiting for a connection, Server Started")

game_ids = []
while True:
    conn, addr = s.accept()
    print("Connected to:", addr)

    game_id, player_id = get_game_player_id()
    print("Game id -", game_id, ", Player id -", player_id)
    print('Game length -', len(game_ids))

    start_new_thread(threaded_client, (conn, game_id,player_id))
