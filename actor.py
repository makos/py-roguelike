#!/usr/bin/env python

class Actor:


    def __init__(self, ypos, xpos, sign='@'):
        self.y = ypos
        self.x = xpos
        self.deltay = 0
        self.deltax = 0
        self.character = sign

        self.update()

    def move(self, direction):
        if direction == 0:
            self.deltay = -1
            self.deltax = 0
        elif direction == 1:
            self.deltay = 0
            self.deltax = 1
        elif direction == 2:
            self.deltay = 1
            self.deltax = 0
        elif direction == 3:
            self.deltay = 0
            self.deltax = -1

    def update(self):
        self.y += self.deltay
        self.x += self.deltax
        self.deltay = 0
        self.deltax = 0

    def getCurrentYX(self):
        return (self.y, self.x)