#!/usr/bin/env python
import os
import random
import math

#       ID      CHAR    PASSABLE?
TILES =([0,     ' ',    False],     # UNUSED
        [1,     '.',    True],      # FLOOR
        [2,     '#',    False],     # WALL
        [3,     '^',    True],      # STAIRS UP
        [4,     'v',    True],      # STAIRS DOWN
        [5,     '+',    False],     # CLOSED DOOR
        [6,     '/',    True],      # OPEN DOOR
        [7,     '@',    True])      # PLAYER (XXX need to make this separate from the level XXX)

# Some sugar
TILE_UNUSED = TILES[0][0]
TILE_FLOOR = TILES[1][0]
TILE_CORRIDOR = TILES[1][0]
TILE_WALL = TILES[2][0]
TILE_UPSTAIRS = TILES[3][0]
TILE_DOWNSTAIRS = TILES[4][0]
TILE_DOORCLOSED = TILES[5][0]
TILE_DOOROPEN = TILES[6][0]

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

class Level:
    """WARNING: This whole class uses (y, x) coordinate system (instead of 
       (x, y)). This means [3][2] doesn't indicate 3rd row of 4th column, but
       4th row of 3rd column."""


    def __init__(self, ydim, xdim):
        assert (xdim > 0 and ydim > 0), "x and y passed to constructor must \
be bigger than 0"
        # this is confusing, but it makes it so X is the horizontal
        # (left-to-right) axis and Y is the vertical (top-down) axis
        self.ysize = xdim
        self.xsize = ydim
        self.maxObjects = random.randint(10, 18)
        self.roomProb = 70
        self.rooms = []
        self.levelArr = [[TILE_UNUSED for row in range(self.xsize)] \
                                      for col in range(self.ysize)]
        # set seed to use current local time, this is done here to use same
        # seed for everything
        random.seed()
        # make a border of unpassable walls around the map (though TILE_UNUSED
        #is also unpassable, and it is the default tile used to initialize maps)
        for y in range(self.ysize):
            for x in range(self.xsize):
                if y == 0 or y == self.ysize-1:
                    self.setTile(y, x, TILE_WALL)
                elif x == 0 or x == self.xsize-1:
                    self.setTile(y, x, TILE_WALL)
        # start the level generation algorithm
        self.generateLevel()
    
    def generateRoom(self, ypos, xpos, maxylen, maxxlen, direction):
        """Creates a room at given ypos, xpos coordinates. The room is at least
           4 by 4 and at most maxylen by maxxlen, the actual dimensions are
           randomly chosen."""

        if direction < NORTH or direction > WEST:
            print("generateRoom(): Invalid direction, skipping")
            return False
        if ypos < 0 or ypos > self.ysize or xpos < 0 or xpos > self.xsize:
            print("generateRoom(): Invalid ypos or xpos arguments, skipping")
            return False
        # make the room dimensions random
        roomleny = random.randrange(4, maxylen+1)
        roomlenx = random.randrange(4, maxxlen+1)

        if not self.scanDirection(ypos, xpos, direction, roomleny, roomlenx):
            return False
        # build upwards (north)
        if direction == NORTH:
            xpos = xpos - (roomlenx // 2)
            centery = ypos - (roomleny // 2)
            centerx = xpos + (roomlenx // 2)
            if (ypos - roomleny) <= 0 or (xpos + roomlenx) >= self.xsize:
                return False
            for y in range(roomleny):
                for x in range(roomlenx):
                    if self.getTile(ypos-y, xpos+x) != TILE_UNUSED:
                        return False
                    if x == 0:
                        self.setTile(ypos-y, xpos+x, TILE_WALL)
                    elif x == roomlenx-1:
                        self.setTile(ypos-y, xpos+x, TILE_WALL)
                    elif y == 0:
                        self.setTile(ypos-y, xpos+x, TILE_WALL)
                    elif y == roomleny-1:
                        self.setTile(ypos-y, xpos+x, TILE_WALL)
                    else:
                        self.setTile(ypos-y, xpos+x, TILE_FLOOR)
        # build right (east)
        elif direction == EAST:
            ypos = ypos + (roomleny // 2)
            centery = ypos - (roomleny // 2)
            centerx = xpos + (roomlenx // 2)
            if (ypos - roomleny) <= 0 or (xpos + roomlenx) >= self.xsize:
                return False
            for y in range(roomleny):
                for x in range(roomlenx):
                    if self.getTile(ypos-y, xpos+x) != TILE_UNUSED:
                        return False
                    if x == 0:
                        self.setTile(ypos-y, xpos+x, TILE_WALL)
                    elif x == roomlenx-1:
                        self.setTile(ypos-y, xpos+x, TILE_WALL)
                    elif y == 0:
                        self.setTile(ypos-y, xpos+x, TILE_WALL)
                    elif y == roomleny-1:
                        self.setTile(ypos-y, xpos+x, TILE_WALL)
                    else:
                        self.setTile(ypos-y, xpos+x, TILE_FLOOR)
        # build down (south)
        elif direction == SOUTH:
            xpos = xpos - (roomlenx // 2)
            centery = ypos + (roomleny // 2)
            centerx = xpos + (roomlenx // 2)
            if (ypos + roomleny) >= self.ysize or (xpos + roomlenx) >= self.xsize:
                return False
            for y in range(roomleny):
                for x in range(roomlenx):
                    if self.getTile(ypos+y, xpos+x) != TILE_UNUSED:
                        return False
                    if x == 0:
                        self.setTile(ypos+y, xpos+x, TILE_WALL)
                    elif x == roomlenx-1:
                        self.setTile(ypos+y, xpos+x, TILE_WALL)
                    elif y == 0:
                        self.setTile(ypos+y, xpos+x, TILE_WALL)
                    elif y == roomleny-1:
                        self.setTile(ypos+y, xpos+x, TILE_WALL)
                    else:
                        self.setTile(ypos+y, xpos+x, TILE_FLOOR)
        # build left (west)
        elif direction == WEST:
            ypos = ypos + (roomleny // 2)
            centery = ypos - (roomleny // 2)
            centerx = xpos - (roomlenx // 2)
            if (ypos - roomleny) >= self.ysize or (xpos - roomlenx) <= 0:
                return False
            for y in range(roomleny):
                for x in range(roomlenx):
                    if self.getTile(ypos-y, xpos-x) != TILE_UNUSED:
                        return False
                    if x == 0:
                        self.setTile(ypos-y, xpos-x, TILE_WALL)
                    elif x == roomlenx-1:
                        self.setTile(ypos-y, xpos-x, TILE_WALL)
                    elif y == 0:
                        self.setTile(ypos-y, xpos-x, TILE_WALL)
                    elif y == roomleny-1:
                        self.setTile(ypos-y, xpos-x, TILE_WALL)
                    else:
                        self.setTile(ypos-y, xpos-x, TILE_FLOOR)

        # all done with building; add the room's ID and center coordinates to list
        print("room built at y {0} x {1}".format(ypos, xpos))
        self.setTile(centery, centerx, 3)
        #                   ROOM ID              Y        X    CONNECTED?
        self.rooms.append([self.objectsOnMap, centery, centerx, False])
        return True

    def generateCorridor(self, starty, startx, endy, endx):
        """Create a corridor at coordinates ypos, xpos of given length, in given
           direction."""

        # if direction < NORTH or direction > WEST:
        #     print("generateCorridor(): Invalid direction, skipping")
        #     return False
        # if ypos < 0 or ypos > self.ysize or xpos < 0 or xpos > self.xsize:
        #     print("generateCorridor(): Invalid ypos or xpos arguments, skipping")
        #     return False
        # width = 3
        # length = random.randrange(2, length+1)

        # for y in range(starty, endy+1):
        #     for x in range(startx, endx+1):
        #         # if self.getTile(y+1, x) == TILE_WALL or self.getTile(y-1, x) == TILE_WALL \
        #         #  or self.getTile(y, x+1) == TILE_WALL or self.getTile(y, x-1) == TILE_WALL:
        #         #     self.setTile(y, x, TILE_DOORCLOSED)
        #         # else:
        #         if y < endy:
        #             self.setTile(y, startx, TILE_FLOOR)
        #         elif x < endx:
        #             self.setTile(starty, x, TILE_FLOOR)
        #         elif y == endy:
        #             self.setTile(endy, x, TILE_FLOOR)
        #         elif x == endx:
        #             self.setTile(y, endx, TILE_FLOOR)
                # if y == starty or y == endy:
                #     self.setTile(y, x, TILE_DOORCLOSED)
                # elif x == startx or x == endx:
                #     self.setTile(y, x, TILE_DOORCLOSED)
                # else:
                #     self.setTile(y, x, TILE_CORRIDOR)

        # if direction == NORTH:
        #     if not self.scanDirection(ypos, xpos, direction, length, width):
        #         return False
        #     if ypos - length <= 0:
        #         return False
        #     for y in range(length):
        #         if y == length-1:
        #             self.setTile(ypos-y, xpos, TILE_DOORCLOSED)
        #         else:
        #             self.setTile(ypos-y, xpos, TILE_CORRIDOR)
        # if direction == EAST:
        #     if not self.scanDirection(ypos, xpos, direction, width, length):
        #         return False
        #     if xpos + length >= self.xsize:
        #         return False
        #     for x in range(length):
        #         if x == length-1:
        #             self.setTile(ypos, xpos+x, TILE_DOORCLOSED)
        #         else:
        #             self.setTile(ypos, xpos+x, TILE_CORRIDOR)
        # if direction == SOUTH:
        #     if not self.scanDirection(ypos, xpos, direction, length, width):
        #         return False
        #     if ypos + length >= self.ysize:
        #         return False
        #     for y in range(length):
        #         if y == length-1:
        #             self.setTile(ypos+y, xpos, TILE_DOORCLOSED)
        #         else:
        #             self.setTile(ypos+y, xpos, TILE_CORRIDOR)
        # if direction == WEST:
        #     if not self.scanDirection(ypos, xpos, direction, width, length):
        #         return False
        #     if xpos - length <= 0:
        #         return False
        #     for x in range(length):
        #         if x == length-1:
        #             self.setTile(ypos, xpos-x, TILE_DOORCLOSED)
        #         else:
        #             self.setTile(ypos, xpos-x, TILE_CORRIDOR)

            # ypos = ypos - (length // 2)
            # for y in range(width):
            #     for x in range(length):
            #         if y == 0 or y == (length - 1):
            #             self.setTile(ypos+y, xpos-x, TILE_WALL)
            #         if (xpos - x) == (xpos - width):
            #             self.setTile(ypos+y, xpos-x, TILE_WALL)
            #         else:
            #             self.setTile(ypos+y, xpos-x, TILE_CORRIDOR)
        return True

    def generateLevel(self):
        """Actual algorithm is in this function. First it generates a single
        room in center of the map (more or less), and then it enters the loop
        state, where it randomly searches for a wall tile, checks from what
        side it can be accessed and finally constructs either a room or
        a corridor."""

        self.objectsOnMap = 0
        assert self.generateRoom(self.ysize // 2, self.xsize // 2, 8, 8, \
                                random.randint(0, 3)), "generateLevel(): \
Error while generating first room"
        self.rooms[0][3] = True # set the first room's connected flag to True for algorithms
        self.objectsOnMap += 1
        # Actual body of the creation algorithm
        isValidTile = -1
        # First, generate only rooms and mark them all unconnected
        # (False flag in self.rooms list)
        # Rooms are added to the list in generateRoom() method
        while self.objectsOnMap != self.maxObjects:
            while isValidTile == -1:
                # if self.objectsOnMap == self.maxObjects:
                #     isFull = 1
                #     break
                newx, newy = 0, 0
                # xmod, ymod = 0, 0

                random.seed()
                newx = random.randrange(self.xsize)
                newy = random.randrange(self.ysize)
                isValidTile = -1
                print("newx = {0}, newy = {1}, searching for suitable place".format(newx, newy))
                if self.getTile(newy, newx) == TILE_UNUSED:
                    for y in range(-3, 4):
                        for x in range(-3, 4):
                            if self.getTile(newy+y, newx+x) == TILE_WALL or \
                               self.getTile(newy+y, newx+x) == TILE_FLOOR:
                                isValidTile = -1
                                break
                            else:
                                isValidTile = random.randint(NORTH, WEST)
                                break
                # if self.getTile(newy, newx) == TILE_WALL or self.getTile(newy, newx) == TILE_CORRIDOR:
                #     # check which way we are (should be) facing
                #     # north?
                #     #print("found a wall at x = {0} y = {1}".format(newx, newy))
                #     if self.getTile(newy+1, newx) == TILE_FLOOR or self.getTile(newy+1, newx) == TILE_CORRIDOR:
                #         # value of isValidTile also sets the direction for room and
                #         # corridor generators
                #         isValidTile = NORTH
                #         xmod = 0
                #         ymod = -1
                #     # east?
                #     elif self.getTile(newy, newx-1) == TILE_FLOOR or self.getTile(newy, newx-1) == TILE_CORRIDOR:
                #         isValidTile = EAST
                #         xmod = 1
                #         ymod = 0
                #     # south?
                #     elif self.getTile(newy-1, newx) == TILE_FLOOR or self.getTile(newy-1, newx) == TILE_CORRIDOR:
                #         isValidTile = SOUTH
                #         xmod = 0
                #         ymod = 1
                #     # west?
                #     elif self.getTile(newy, newx+1) == TILE_FLOOR or self.getTile(newy, newx+1) == TILE_CORRIDOR:
                #         isValidTile = WEST
                #         xmod = -1
                #         ymod = 0

                #     # check if any door neighbors with chosen tile
                #     if isValidTile > -1:
                #         if self.getTile(newy+1, newx) == TILE_DOORCLOSED:
                #             isValidTile = -1
                #         elif self.getTile(newy, newx+1) == TILE_DOORCLOSED:
                #             isValidTile = -1
                #         elif self.getTile(newy-1, newx) == TILE_DOORCLOSED:
                #             isValidTile = -1
                #         elif self.getTile(newy, newx-1) == TILE_DOORCLOSED:
                #             isValidTile = -1

                    # if isValidTile > -1:
                    #     break

            if isValidTile > -1:
                # objectToBuild = random.randint(0, 100)
                print("trying to build a room at y {0}, x {1}".format(newy, newx))
                if self.generateRoom(newy, newx, 11, 12, isValidTile):
                    self.objectsOnMap += 1
                isValidTile = -1

                # if objectToBuild <= self.roomProb:
                #     #print("building a room in direction {0}".format(isValidTile))
                #     if self.generateRoom(newy+ymod, newx+xmod, 8, 8, isValidTile):
                #         self.objectsOnMap += 1
                #         self.setTile(newy, newx, TILE_DOORCLOSED)
                #         self.setTile(newy+ymod, newx+xmod, TILE_FLOOR)
                # elif objectToBuild >= self.roomProb:
                #     #print("building a corridor in direction {0}".format(isValidTile))
                #     if self.generateCorridor(newy+ymod, newx+xmod, 6, isValidTile):
                #         self.objectsOnMap += 1
                #         self.setTile(newy, newx, TILE_DOORCLOSED)
        # Room quota is achieved; now it's time to add corridors between each
        # room, and switch the connected flag to True
        for room in self.rooms:
            for secondroom in self.rooms:
                # if room[3] == False:
                    # if secondroom[3] == True:
                self.generateCorridor(room[1], room[2], secondroom[1], secondroom[2])
                room[3] = True
            # if room[3] == False:
            #     nearest = self.findNearestNeighbor(room[1], room[2])
            #     if nearest > -1:
            #         print("nearest neighbor for room {0} is {1}".format(room[0], nearest))
            #         self.generateCorridor(room[1], room[2], self.rooms[nearest][1],
            #                               self.rooms[nearest][2])
            #         room[3] = True


    def findNearestNeighbor(self, y, x):
        """Looks for room closest to given y, x coords using some simple math.
           Returns matching room's ID (integer)."""

        # potentialMatch stores ID of room that's (so far) nearest to given y,x
        # potentialMatch = -1
        distances = {}

        for room in self.rooms:
            # if room[3] == False:
            dist = math.sqrt(((y - room[1])**2) + ((x - room[2])**2))
            print("room[{0}]: {1} - {2}, {3} - {4} = {5}".format(room[0], y, room[1], x, room[2], int(dist)))
            if int(dist) > 0:
                distances[room[0]] = int(dist)
            else:
                distances[room[0]] = 100
                # distances.append(int(dist))
                # if abs(dist) < lastDist:
                #     potentialMatch = room[0]
                # lastDist = dist

        # distances.remove(0)
        shortest = min(distances.values())
        for key, val in distances.items():
            if val == shortest:
                return key # returns ID of room
        # if len(distances) > 0:
        #     return distances.index(min(distances))
        # else:
        #     return

        # if potentialMatch > -1:
        #     return potentialMatch
        # else:
        #     print("Couldn't find nearest neighbor; skipping")
        #     return -1


    def getTile(self, y, x):
        """Returns tile ID at given [y][x]."""

        if y >= 0 and y < self.ysize and x >= 0 and x < self.xsize:
            return self.levelArr[y][x]
        else:
            return -1

    def setTile(self, y, x, tileid):
        """Sets [y][x] coordinates to given tile ID."""

        if y >= 0 and y < self.ysize and x >= 0 and x < self.xsize:
            self.levelArr[y][x] = TILES[tileid][0]
        else:
            return -1

    def getDungeon(self):
        return self.levelArr

    def getXDim(self):
        return self.xsize

    def getYDim(self):
        return self.ysize

    def drawLevel(self):
        """Draws the generated dungeon in terminal."""

        print(self.rooms)
    #    os.system('clear')
        for row in self.levelArr:
            print('')
            for val in row:
                if val == TILE_UNUSED:
                    print(TILES[TILE_UNUSED][1], end='')
                elif val == TILE_FLOOR:
                    print(TILES[TILE_FLOOR][1], end='')
                elif val == TILE_WALL:
                    print(TILES[TILE_WALL][1], end='')
                elif val == TILE_UPSTAIRS:
                    print(TILES[TILE_UPSTAIRS][1], end='')
                elif val == TILE_DOWNSTAIRS:
                    print(TILES[TILE_DOWNSTAIRS][1], end='')
                elif val == TILE_DOORCLOSED:
                    print(TILES[TILE_DOORCLOSED][1], end='')
                elif val == TILE_DOOROPEN:
                    print(TILES[TILE_DOOROPEN][1], end='')
                elif val == 7:
                    print(TILES[7][1], end='')

    def scanDirection(self, ypos, xpos, direction, leny, lenx):
        """Scans the level in direction originating from (y, x) coordinates for
           given length, returns True if it is empty (can build) and False
           otherwise."""

        if direction == 0:
            xpos = xpos - (lenx // 2)
            for y in range(leny):
                for x in range(lenx):
                    if self.getTile(ypos-y, xpos+x) != TILE_UNUSED:
                        #print("Scan failed")
                        return False
        elif direction == 1:
            ypos = ypos - (leny // 2)
            for y in range(leny):
                for x in range(lenx):
                    if self.getTile(ypos+y, xpos+x) != TILE_UNUSED:
                        #rint("Scan failed")
                        return False
        elif direction == 2:
            xpos = xpos - (lenx // 2)
            for y in range(leny):
                for x in range(lenx):
                    if self.getTile(ypos+y, xpos+x) != TILE_UNUSED:
                        #print("Scan failed")
                        return False
        elif direction == 3:
            ypos = ypos - (leny // 2)
            for y in range(leny):
                for x in range(lenx):
                    if self.getTile(ypos+y, xpos-x) != TILE_UNUSED:
                        #print("Scan failed")
                        return False
        else:
            print("scanDirection(): Invalid direction value. Skipping...")
            return False
        #print("Scan succeeded")
        return True


if __name__ == "__main__":
     # os.system('setterm -cursor off')
    testlev = Level(80, 20)
    testlev.drawLevel()
    print('')
    while True:
        input('')
        testlev = Level(80, 20)
        testlev.drawLevel()
    # os.system('setterm -cursor on')