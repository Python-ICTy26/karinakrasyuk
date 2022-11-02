import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)

    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """
        row = "+" + str("-" * self.life.cols) + "+"
        screen.addstr(0, 0, row)
        for i in range(self.life.rows):
            screen.addstr(i + 1, 0, "|")
            screen.addstr(i + 1, self.life.cols + 1, "|")

        screen.addstr(self.life.rows + 1, 0, row)

    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        for i in range(self.life.rows):
            row = ""
            for j in range(self.life.cols):
                if self.life.curr_generation[i][j] == 1:
                    row += '*'
                else:
                    row += ' '

            screen.addstr(i + 1, 1, row)

    def run(self) -> None:
        screen = curses.initscr()

        running = True
        while (running):
            if not self.life.is_changing:
                running = False
            self.draw_borders(screen)
            self.life.step()
            self.draw_grid(screen)
            screen.refresh()
            time.sleep(0.2)
        curses.endwin()


if __name__ == "__main__":
    game = Console(GameOfLife((20, 50)))
    game.run()
