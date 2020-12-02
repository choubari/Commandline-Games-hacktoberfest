# Author: André Fonteles

import atexit
import random
import curses
import time
import threading 
import os

# An IOController controls the input (keyboard) and output
# (console) of the game
class IOController():

    # TODO: curses is being shared between the two threads and may 
    # incur in race condition. This should be fixed later

    KEY_UP = curses.KEY_UP
    KEY_DOWN = curses.KEY_DOWN
    KEY_LEFT = curses.KEY_LEFT
    KEY_RIGHT = curses.KEY_RIGHT

    KEY_Q = ord('q')
    KEY_A = ord('a')

    def __init__(self):
        self.__stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.__stdscr.keypad(1)

        self.__last_key = self.KEY_RIGHT
        self.__key_lock = threading.Lock() # Create a lock to prevent race condition on __last_key

        # Start thread that continuously reads user's input
        thread = threading.Thread(target = self.__read_key)
        thread.start()


    # Outputs the game_array to the console
    def print(self, game_array, score, dead):

        self.__stdscr.addstr(1, len(game_array[0]) + 1, "Score:" + str(score))
        for y in range(0, len(game_array)):
            line = ""
            for x in range(0, len(game_array[y])):
                line += game_array[y][x]
            self.__stdscr.addstr(y, 0, line)
        
        # If dead, display dead message
        if(dead):
            msg_y = len(game_array)//2
            msg_x = len(game_array[0])//4
            self.__stdscr.addstr(msg_y-1, msg_x, "You are dead")
            # self.__stdscr.addstr(msg_y+1, len(game_array[0]) + 1, "Press \"a\" to play again")
            self.__stdscr.addstr(msg_y+2, len(game_array[0]) + 1, "Press \"q\" to quit")

        self.__stdscr.refresh()


    # Returns the last key pressed by the user in terms of
    # the constants InOutputer.KEY_UP, InOutputer.KEY_DOWN
    # InOutputer.KEY_LEFT and InOutputer.KEY_RIGHT
    def get_last_key(self):
        self.__key_lock.acquire()
        key = self.__last_key
        self.__key_lock.release()
        
        return key


    # Used in a separate thread to constantly
    # update the last direction key input by 
    # the user
    def __read_key(self):

        self.__key_lock.acquire()
        while(self.__last_key != self.KEY_Q): # Continue as long as key is not 'q'
            self.__key_lock.release()
            key = self.__stdscr.getch()

            if key == curses.KEY_UP: 
                key = self.KEY_UP
            elif key == curses.KEY_DOWN: 
                key = self.KEY_DOWN
            elif key == curses.KEY_LEFT:
                key = self.KEY_LEFT
            elif key == curses.KEY_RIGHT:  
                key = self.KEY_RIGHT
            elif key == self.KEY_Q:  
                key = self.KEY_Q
            elif key == self.KEY_A:  
                key = self.KEY_A

            if(key):
                self.__key_lock.acquire()
                self.__last_key = key
                self.__key_lock.release()
            
            self.__key_lock.acquire()    
        self.__key_lock.release()


    # End terminal curses mode.
    def close(self):
        curses.endwin()


# A MazeMap represents the maze where the snake is in
class MazeMap():
    
    BG_CHAR = "."

    def __init__(self, width, height):
        self.__width = width
        self.__height = height

        self.generate_maze()


    # Generate a bidimentional array representing the maze
    def generate_maze(self):
        self.__maze_array = []
        for y in range(0, self.__height):
            self.__maze_array.append([])
            for x in range(0, self.__width):
                self.__maze_array[y].append(self.BG_CHAR)
    
        return self.__maze_array
        
# This class is used to instantiate the snake.
class Snake:

    SNAKE_CHAR = "*"

    DIRECTION_UP = "top"
    DIRECTION_DOWN = "down"
    DIRECTION_RIGHT = "right"
    DIRECTION_LEFT = "left"


    def __init__(self, game_width, game_height):
        self.__game_width = game_width
        self.__game_height = game_height

        self.__generate_snake_array()

        # Configure whether the snake is dead or not
        self.__dead = False

        # Configure snake to start moving rightwards
        self.__direction = self.DIRECTION_RIGHT

        
    # Returns an array of points (x, y) representing the snake's body
    def get_head_pos(self):
        return self.__snake_array[-1]


    # Returns a point (x, y) representing the head's position
    def get_snake_array(self):
        return self.__snake_array


    # Generates an array of points (x, y) representing the snake's body
    def __generate_snake_array(self):
        init_size = 4
        init_x = self.__game_width // 2
        init_y = self.__game_height - 2
        self.__snake_array = []
        for x in range(init_x - init_size, init_x):
            self.__snake_array.append((x, init_y))
        
        self._potential_growth = (init_x - init_size - 1, init_y)

    # Adds the snake to the game_array
    def add_itself(self, game_array):
        for point in self.__snake_array:
            game_array[point[1]][point[0]] = self.SNAKE_CHAR


    # Moves the snake towards *neighboring* point (x, y)
    # Kills the snake if it hits something other than food
    def move_towards(self, point):
        newHead = point

        # Kill the snake if it hits something other than food
        self.check_survival(newHead)
        if(not self.__dead):
            self.__snake_array.append(newHead)
            # Remove last point and add it to potential_growph.
            # If the snake is fed, potential_growth is added to
            # its queue
            self._potential_growth = self.__snake_array.pop(0)


    # Attempts to eat the food
    def attempt_to_eat(self, food):
        if(food.collide_with(self.get_head_pos())):
            self.__snake_array.insert(0, self._potential_growth)
            food.spawn_food(self.__snake_array)


    # Checks if the snake should keep alive.
    # Set __dead to True if not.
    def check_survival(self, new_pos):
        # Check if the head is outside upper and right boundaries
        if(new_pos[0] < 0 or new_pos[1] < 0):
            self.__dead = True

        # Check if the head is outside bottom and left boundaries
        if(new_pos[0] >= self.__game_width or new_pos[1] >= self.__game_height):
            self.__dead = True
        
        for i in range(1, len(self.get_snake_array()) - 1):
            if(self.get_snake_array()[i] == new_pos):
                self.__dead = True


    # Changes the direction of the snake if the new direction is not
    # incompatible with the old one. If incompatible, it does nothing.
    def set_direction(self, direction):
        invalid = False if len(direction) > 0 else True
        invalid = invalid or self.__direction == self.DIRECTION_UP and direction == self.DIRECTION_DOWN
        invalid = invalid or self.__direction == self.DIRECTION_DOWN and direction == self.DIRECTION_UP
        invalid = invalid or self.__direction == self.DIRECTION_LEFT and direction == self.DIRECTION_RIGHT
        invalid = invalid or self.__direction == self.DIRECTION_RIGHT and direction == self.DIRECTION_LEFT
        
        if(not invalid):
            self.__direction = direction


    # Returns the size of the snake
    def get_size(self):
        return len(self.__snake_array)


    # Configure whether the snake is dead or not
    def is_dead(self):
        return self.__dead


    # Updates internal logic of the snake
    def update(self, food):
        if(not self.__dead):
            if(self.__direction == self.DIRECTION_UP):
                self.move_towards((self.get_head_pos()[0], self.get_head_pos()[1]-1))
            elif(self.__direction == self.DIRECTION_DOWN):
                self.move_towards((self.get_head_pos()[0], self.get_head_pos()[1]+1))
            elif(self.__direction == self.DIRECTION_LEFT):
                self.move_towards((self.get_head_pos()[0]-1, self.get_head_pos()[1]))
            elif(self.__direction == self.DIRECTION_RIGHT):
                self.move_towards((self.get_head_pos()[0]+1, self.get_head_pos()[1]))
            
            self.attempt_to_eat(food)



# Thi class is used to instantied the food the snake is after
class Food:

    FOOD_CHAR = "x"

    def __init__(self, game_width, game_height):
        self.__game_width = game_width
        self.__game_height = game_height


    # Spawn the food point in a position that is not 
    # in a the forbiden_points list
    def spawn_food(self, forbiden_points):
        x = random.randint(0, self.__game_width-1)
        y = random.randint(0, self.__game_height-1)
        
        # Make sure the food position is not in a forbiden
        # position/point
        while((x,y) in forbiden_points):
            x = random.randint(0, self.__game_width-1)
            y = random.randint(0, self.__game_height-1)
            
        self.__pos = (x, y)


    # Return true if point collides with food and
    # false otherwise
    def collide_with(self, point):
        if(point == self.__pos):
            return True
        else:
            return False


    def add_itself(self, game_array):
        game_array[self.__pos[1]][self.__pos[0]] = self.FOOD_CHAR

# This class represents the actual game
class SnakeGame():

    def __init__(self, width, height):
        self.__maze = MazeMap(width, height)
        self.__snake = Snake(width, height)
        self.__food = Food(width, height)


    # Starts the game
    def start(self):
        self.__io = IOController()
        atexit.register(self.__io.close) # Calls a clean up function at exit.

        self.__food.spawn_food(self.__snake.get_snake_array())
        
        while(True):
            game_array = self.__maze.generate_maze()

            self.__food.add_itself(game_array)
            self.__snake.add_itself(game_array)

            self.__io.print(game_array, self.__snake.get_size(), self.__snake.is_dead())

            key = self.__io.get_last_key()
            if(self.__snake.is_dead()):
                if(key == IOController.KEY_Q):
                    self.__io.close()
                    break

            self.__snake.set_direction(self.__read_direction(key))
            self.__update()

            time.sleep(.5)         


    def __update(self):
        self.__snake.update(self.__food)


    def __read_direction(self, key):
        direction = ""
        if(key == IOController.KEY_UP):
            direction = Snake.DIRECTION_UP
        elif(key == IOController.KEY_DOWN):
            direction = Snake.DIRECTION_DOWN
        elif(key == IOController.KEY_LEFT):
            direction = Snake.DIRECTION_LEFT
        elif(key == IOController.KEY_RIGHT):
            direction = Snake.DIRECTION_RIGHT
        return direction



def main():
    game = SnakeGame(30, 10)
    game.start()

main()