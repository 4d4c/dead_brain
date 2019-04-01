#!/usr/bin/env python3

import sys
import random

import pygame


class TetrisApp():
    CELL_SIZE = 40
    COLUMNS = 10
    ROWS = 20
    MAXFPS = 30

    COLORS = [
        (0, 0, 0),
        (255, 85, 85),
        (100, 200, 115),
        (120, 108, 245),
        (255, 140, 50),
        (50, 120, 52),
        (146, 202, 73),
        (150, 161, 218),
        (45, 45, 45)
    ]

    TETRIS_SHAPES = [
        [
            [1, 1, 1],
            [0, 1, 0]
        ],
        [
            [0, 2, 2],
            [2, 2, 0]
        ],
        [
            [3, 3, 0],
            [0, 3, 3]
        ],
        [
            [4, 0, 0],
            [4, 4, 4]
        ],
        [
            [0, 0, 5],
            [5, 5, 5]
        ],
        [
            [6, 6, 6, 6]
        ],
        [
            [7, 7],
            [7, 7]
        ]
    ]

    SPRITES = [
        "sprites/block_azure.png",
        "sprites/block_lemon.png",
        "sprites/block_magento.png",
        "sprites/block_neo.png",
        "sprites/block_strawberry.png",
        "sprites/block_sunset.png",
        "sprites/block_teal.png",

        "sprites/shadow_azure.png",
        "sprites/shadow_lemon.png",
        "sprites/shadow_magento.png",
        "sprites/shadow_neo.png",
        "sprites/shadow_strawberry.png",
        "sprites/shadow_sunset.png",
        "sprites/shadow_teal.png",
    ]


    def __init__(self):
        pygame.init()
        pygame.key.set_repeat(250, 25)
        pygame.event.set_blocked(pygame.MOUSEMOTION)

        self.height = self.CELL_SIZE * self.ROWS
        self.width = self.CELL_SIZE * (self.COLUMNS + 6)

        # self.background_grid = [[8 if x % 2 == y % 2 else 0 for x in range(self.COLUMNS)] for y in range(self.ROWS)]
        self.default_font = pygame.font.Font(None, 50)
        self.paused = False
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.shape_x = 0
        self.shape_y = 0
        self.split_line = self.CELL_SIZE * self.COLUMNS
        self.next_shape = random.choice(self.TETRIS_SHAPES)
        self.images = []
        for sprite_path in self.SPRITES:
            self.images.append(
                pygame.transform.scale(
                    pygame.image.load(sprite_path),
                    (self.CELL_SIZE, self.CELL_SIZE)
                )
            )

        self.init_game()


    def init_game(self):
        self.board = [[0] * self.COLUMNS for _ in range(self.ROWS)] + [[1] * self.COLUMNS]
        self.shape = []
        self.level = 0
        self.score = 0
        self.lines = 0
        self.game_over = False
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000)

        self.add_new_shape()


    def add_new_shape(self):
        self.shape = self.next_shape
        self.next_shape = random.choice(self.TETRIS_SHAPES)

        self.shape_x = int(self.COLUMNS / 2 - len(self.shape[0]) / 2)
        self.shape_y = 0

        if self.check_collision(self.shape, self.shape_x, self.shape_y):
            self.game_over = True


    def check_collision(self, shape, position_x, position_y):
        for shape_y, row in enumerate(shape):
            for shape_x, cell in enumerate(row):
                try:
                    if cell and self.board[shape_y + position_y][shape_x + position_x]:
                        return True
                except IndexError:
                    return True

        return False


    def run(self):
        key_actions = {
            'ESCAPE':   self.quit,
            'LEFT':     lambda: self.move_shape(-1),
            'RIGHT':    lambda: self.move_shape(+1),
            'DOWN':     self.drop_shape,
            'UP':       self.rotate_shape,
            'p':        self.toggle_pause,
            'SPACE':    self.insta_drop,
            'RETURN':   self.start_game
        }

        ticks = pygame.time.Clock()

        while True:
            self.screen.fill(self.COLORS[8])

            if self.game_over:
                self.display_message_center(
                    "Game Over!\nYour score: {}\nPress ENTER to continue".format(self.score)
                )
            else:
                if self.paused:
                    self.display_message_center("Paused")
                else:
                    pygame.draw.line(
                        self.screen,
                        (255, 255, 255),
                        (self.split_line + 1, 0),
                        (self.split_line + 1, self.height - 1)
                    )

                    self.display_message(
                        "Score: {}\n\nLevel: {}\nLines: {}".format(self.score, self.level, self.lines),
                        self.split_line + self.CELL_SIZE // 2,
                        self.CELL_SIZE * 5
                    )

                    # self.draw_matrix(self.background_grid, 0, 0)
                    self.draw_matrix(self.board, 0, 0, True)

                    # Draw shadow shape
                    counter_y = self.shape_y
                    while not self.check_collision(self.shape, self.shape_x, counter_y):
                        counter_y += 1
                    self.draw_matrix(self.shape, self.shape_x, counter_y - 1, True, True)

                    self.draw_matrix(self.shape, self.shape_x, self.shape_y, True)
                    self.draw_matrix(self.next_shape, self.COLUMNS + 1, 2, True)

            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.drop_shape(False)
                elif event.type == pygame.QUIT:
                    self.quit()
                elif event.type == pygame.KEYDOWN:
                    for key in key_actions:
                        if event.key == getattr(pygame, "K_" + key):
                            key_actions[key]()

            ticks.tick(self.MAXFPS)


    def display_message_center(self, message):
        for line_index, line in enumerate(message.splitlines()):
            message_image = self.default_font.render(line, True, (255, 255, 255), self.COLORS[8])

            message_image_x, message_image_y = message_image.get_size()
            message_image_x //= 2
            message_image_y //= 2

            self.screen.blit(
                message_image, (
                    self.width // 2 - message_image_x,
                    self.height // 2 - message_image_y + line_index * 50
                )
            )


    def display_message(self, message, position_x, position_y):
        for line in message.splitlines():
            self.screen.blit(
                self.default_font.render(
                    line,
                    True,
                    (255, 255, 255),
                    self.COLORS[8]
                ),
                (position_x, position_y)
            )

            position_y += 50


    def draw_matrix(self, matrix, offset_x, offset_y, shape=False, shadow_shape=False):
        for matrix_y, row in enumerate(matrix):
            for matrix_x, value in enumerate(row):
                if value:
                    if shape:
                        self.screen.blit(
                            self.images[value - 1 + len(self.images) // 2 if shadow_shape else value - 1],
                            pygame.Rect(
                                (offset_x + matrix_x) * self.CELL_SIZE,
                                (offset_y + matrix_y) * self.CELL_SIZE,
                                self.CELL_SIZE,
                                self.CELL_SIZE
                            )
                        )
                    else:
                        pygame.draw.rect(
                            self.screen,
                            self.COLORS[value],
                            pygame.Rect(
                                (offset_x + matrix_x) * self.CELL_SIZE,
                                (offset_y + matrix_y) * self.CELL_SIZE,
                                self.CELL_SIZE,
                                self.CELL_SIZE
                            ),
                            0
                        )


    def drop_shape(self, user_action=True):
        if not self.game_over and not self.paused:
            if user_action:
                self.score += 1

            self.shape_y += 1

            if self.check_collision(self.shape, self.shape_x, self.shape_y):
                for shape_y, shape_row in enumerate(self.shape):
                    for shape_x, shape_value in enumerate(shape_row):
                        self.board[shape_y + self.shape_y - 1][shape_x + self.shape_x] += shape_value

                self.add_new_shape()

                cleared_rows_count = 0

                for row_index, row in enumerate(self.board[:-1]):
                    if 0 not in row:
                        del self.board[row_index]
                        self.board = [[0 for i in range(10)]] + self.board

                        cleared_rows_count += 1

                self.add_score_and_check_level(cleared_rows_count)

                return True

        return False


    def add_score_and_check_level(self, new_line_count):
        line_score = [0, 40, 100, 300, 1200]

        self.lines += new_line_count
        self.score += line_score[new_line_count] * self.level

        if self.lines >= self.level * 6:
            self.level += 1
            new_delay = 1000 - 100 * (self.level - 1)
            new_delay = 100 if new_delay < 100 else new_delay
            pygame.time.set_timer(pygame.USEREVENT + 1, new_delay)


    def move_shape(self, move_x):
        if not self.game_over and not self.paused:
            shape_x = self.shape_x + move_x
            if shape_x < 0:
                shape_x = 0

            if shape_x > self.COLUMNS - len(self.shape[0]):
                shape_x = self.COLUMNS - len(self.shape[0])

            if not self.check_collision(self.shape, shape_x, self.shape_y):
                self.shape_x = shape_x


    def insta_drop(self):
        if not self.game_over and not self.paused:
            while not self.drop_shape():
                pass


    def rotate_shape(self):
        if not self.game_over and not self.paused:
            new_shape = list(map(list, zip(*self.shape[::-1])))

            if not self.check_collision(new_shape, self.shape_x, self.shape_y):
                self.shape = new_shape

            # Allow rotate next to right wall
            if self.shape_x == self.COLUMNS - len(self.shape[0]):
                if not self.check_collision(new_shape, self.shape_x - len(new_shape[0]), self.shape_y):
                    self.shape_x = self.COLUMNS - len(new_shape[0])
                    self.shape = new_shape


    def toggle_pause(self):
        self.paused = not self.paused


    def start_game(self):
        if self.game_over:
            self.init_game()


    def quit(self):
        self.display_message_center("Exiting...")
        pygame.display.update()
        sys.exit(0)


if __name__ == '__main__':
    APP = TetrisApp()
    APP.run()
