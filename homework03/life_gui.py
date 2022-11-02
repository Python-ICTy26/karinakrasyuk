from math import trunc

import pygame
from life import GameOfLife
from pygame.locals import *
from ui import UI


class GUI(UI):
    def __init__(self, life: GameOfLife, cell_size: int = 10, speed: int = 10) -> None:
        self.cell_size = cell_size
        self.speed = speed
        # Устанавливаем размер окна
        # Создание нового окна
        super().__init__(life)

        self.height = self.life.rows * self.cell_size
        self.width = self.life.cols * self.cell_size
        self.screen_size = self.width, self.height
        self.screen = pygame.display.set_mode(self.screen_size)

    def draw_lines(self) -> None:
        # Copy from previous assignment
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def draw_grid(self) -> None:
        # Copy from previous assignment
        for i in range(self.life.rows):
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j]:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("green"),
                        (
                            j * self.cell_size + 1,
                            i * self.cell_size + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )
                else:
                    pygame.draw.rect(
                        self.screen,
                        pygame.Color("white"),
                        (
                            j * self.cell_size + 1,
                            i * self.cell_size + 1,
                            self.cell_size - 1,
                            self.cell_size - 1,
                        ),
                    )

    def run(self) -> None:
        # Copy from previous assignment
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        self.grid = self.life.curr_generation
        self.draw_grid()

        running = True
        pause = False
        after_mouse = False

        while running:
            for event in pygame.event.get():
                if event.type == "QUIT":
                    running = False
                if event.type == "KEYDOWN":
                    if event.key == "K_SPACE":
                        pause = not pause

                if event.type == "MOUSEBUTTONDOWN":
                    (y, x) = pygame.mouse.get_pos()
                    if pause:
                        cur_x = int(trunc(x / self.cell_size))
                        cur_y = int(trunc(y / self.cell_size))
                        if event.button == 1:
                            self.grid[cur_x][cur_y] ^= 1

                        self.life.curr_generation = self.grid
                        self.draw_lines()
                        self.draw_grid()
                        pygame.display.flip()
                        after_mouse = True

            if not self.life.is_changing:
                if not pause:
                    if after_mouse:
                        after_mouse = False
                    else:
                        running = False

            if self.life.is_max_generations_exceeded:
                running = False

            if not pause:
                self.grid = self.life.curr_generation
                self.draw_lines()
                self.draw_grid()
                self.life.step()

                pygame.display.flip()

            clock.tick(self.speed)
        pygame.quit()
