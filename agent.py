from gameobjects import GameObject
from move import Move, Direction
import math


class Agent:

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """

    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts):
        """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
        the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
        functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
        that much that it will explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of the board. The upper left most
        coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nothing at the
        given coordinate), GameObject.FOOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
        there is a wall at the given coordinate. TIP: do not run into them), GameObject.SNAKE_HEAD (meaning the head
        of the snake is located there) and GameObject.SNAKE_BODY (meaning there is a body part of the snake there.
        TIP: also, do not run into these). The snake will also die when it tries to escape the board (moving out of
        the boundaries of the array)

        :param score: The current score as an integer. Whenever the snake eats, the score will be increased by one.
        When the snake tragically dies (i.e. by running its head into a wall) the score will be reset. In ohter
        words, the score describes the score of the current (alive) worm.

        :param turns_alive: The number of turns (as integer) the current snake is alive.

        :param turns_to_starve: The number of turns left alive (as integer) if the snake does not eat. If this number
        reaches 1 and there is not eaten the next turn, the snake dies. If the value is equal to -1, then the option
        is not enabled and the snake can not starve.

        :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
        Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.

        :param head_position: (x,y) of the head of the snake. The following should always hold: board[head_position[
        0]][head_position[1]] == GameObject.SNAKE_HEAD.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.

        :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
        going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
        snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
        Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
        move left is made, the snake will go one block to the left and change its direction to west.
        """
        print(self.get_closest_food(board, head_position))
        print(self.heuristic_to_food(head_position, self.get_closest_food(board, head_position)))
        return Move.STRAIGHT

    def should_redraw_board(self):
        """
        This function indicates whether the board should be redrawn. Not drawing to the board increases the number of
        games that can be played in a given time. This is especially useful if you want to train you agent. The
        function is called before the get_move function.

        :return: True if the board should be redrawn, False if the board should not be redrawn.
        """
        return True

    def should_grow_on_food_collision(self):
        """
        This function indicates whether the snake should grow when colliding with a food object. This function is
        called whenever the snake collides with a food block.

        :return: True if the snake should grow, False if the snake should not grow
        """
        return True

    def on_die(self, head_position, board, score, body_parts):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.

        :param head_position: (x, y) position of the head at the moment of dying.

        :param board: two dimensional array representing the board of the game at the moment of dying. The board
        given does not include information about the snake, only the food position(s) and wall(s) are listed.

        :param score: score at the moment of dying.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.
        When the snake runs in its own body the following holds: head_position in body_parts.
        """

    def get_food(self, board):
        """This function will return an array consisting of tuples that represent the x and y coordinates of the
        locations of food on the current board stat.

        :param board: A two dimensional array representing the current board state. Get GameObject on location with
        board[x][y].

        :return: An array of tuples with the locations of the food represented with (x, y).
        """
        ret = []
        for x in range(0, len(board)):
            for y in range(0, len(board[x])):
                if board[y][x] is GameObject.FOOD:
                    ret.append((x, y))
        return ret

    def get_closest_food(self, board, head_position):
        """This function gets the location of the closest food. It returns None if there is no food in the list.

        :param board: A two dimensional array representing the current board state. Get GameObject on location with
        board[x][y].
        :param head_position: (x,y) of the position of the snakes head.
        :return: (x,y) of the closest food location.
        """
        food = self.get_food(board)
        closest = None
        ret = None
        for location in food:
            contender = self.heuristic_to_food(head_position, location)
            if closest is None or contender < closest:
                closest = contender
                ret = location
        return ret

    def heuristic_to_food(self, position, food_location):
        """Function that gets the distance to the food

        :param position: (x,y) of the current position of which the heuristic should be returned.
        :param board: A two dimensional array representing the current board state. Get GameObject on location with
        board[x][y].
        :param food_location: Array with tuples (x,y) that represents the location of food on the board.
        :return: The distance to the food
        """
        return math.sqrt(abs(food_location[0] - position[0]) ** 2 + abs(food_location[1] - position[1]) ** 2)

    def make_route(self, food_locations, head_position, direction):
        """This function will determine the route to the food with an A* algorithm.

        :param food_locations: Array with tuples (x,y) that represents the location of food on the board.
        :param head_position: (x,y) of the head of the snake.
        :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
        Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.
        :return: Array that represents the route that must be taken
        """
