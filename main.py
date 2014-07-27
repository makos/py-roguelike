#!/usr/bin/env python
import sys
import tty
import termios
from level import *
from actor import *

def _getch():
    """Hack to get keyboard input in real-time.
       Thanks to: http://code.activestate.com/recipes/134892/
       WARNING: Disables CTRL-D and CTRL-C combos in terminal, so there must
       be an event handler that closes the program, otherwise it will run
       infinitely until terminated forcefully."""

    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

class Game:


    def __init__(self):
        os.system('setterm -cursor off')

        self.dungeon = Level(80, 20)
        for y in range(self.dungeon.getYDim()):
            for x in range(self.dungeon.getXDim()):
                if self.dungeon.getTile(y, x) == TILE_FLOOR:
                    playerY = y
                    playerX = x
                    continue

        self.player = Actor(playerY, playerX, '@')
        self.dungeon.setTile(playerY, playerX, 7)
        self.dungeon.drawLevel()

        while True:
            print('')
            keypress = _getch()
            if keypress == 'Q':
                break
            elif keypress == 'w':
                self.player.move(0)
            elif keypress == 'd':
                self.player.move(1)
            elif keypress == 's':
                self.player.move(2)
            elif keypress == 'd':
                self.player.move(3)
            else:
                pass
            
            oldpos = self.player.getCurrentYX()
            self.player.update()
            move = self.player.getCurrentYX()
            self.dungeon.setTile(move[0], move[1], 7)
            self.dungeon.setTile(oldpos[0], oldpos[1], TILE_FLOOR)
            self.dungeon.drawLevel()

        os.system('setterm -cursor on')
        sys.exit()


if __name__ == '__main__':
    g = Game()