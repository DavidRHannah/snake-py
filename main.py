import pygame
from dataclasses import dataclass
from enum import Enum
from typing import List
import random

pygame.init()

SCREEN_WIDTH:   int = 600
SCREEN_HEIGHT:  int = 600
CELL_SIZE:      int = 30

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running: bool = True


def draw_grid():
    """Draws the game grid."""
    for col in range(0, SCREEN_WIDTH, CELL_SIZE):
        for row in range(0, SCREEN_HEIGHT, CELL_SIZE):
            rect = pygame.Rect(col, row, CELL_SIZE, CELL_SIZE)
            pygame.draw.rect(screen, "dark green", rect, 1)


class Direction(Enum):
    UP:     int = 1
    DOWN:   int = 2
    LEFT:   int = 3
    RIGHT:  int = 4


@dataclass
class Food:
    x:      int
    y:      int
    width:  int
    height: int

    @staticmethod
    def create_random_food() -> 'Food':
        """Creates a Food object at a random location within the grid."""
        food_x = random.randint(0, (SCREEN_WIDTH // CELL_SIZE) - 1) * CELL_SIZE
        food_y = random.randint(0, (SCREEN_HEIGHT // CELL_SIZE) - 1) * CELL_SIZE
        return Food(food_x, food_y, CELL_SIZE, CELL_SIZE)


@dataclass
class SnakeBlock:
    x:      int
    y:      int
    width:  int
    height: int


class Snake:
    def __init__(self):
        self.body: List[SnakeBlock] = []
        self.direction: Direction = Direction.RIGHT
        self.direction_changed = False
        starting_pos_x: int = SCREEN_WIDTH // 2
        starting_pos_y: int = SCREEN_HEIGHT // 2
        self.body.append(SnakeBlock(starting_pos_x, starting_pos_y, CELL_SIZE, CELL_SIZE))

    def move(self):
        """Moves the snake in the current direction."""
        head: SnakeBlock = self.body[0]
        new_head: SnakeBlock = SnakeBlock(0, 0, 0, 0)
        match self.direction:
            case Direction.UP:
                new_head = SnakeBlock(head.x, head.y - CELL_SIZE, CELL_SIZE, CELL_SIZE)
            case Direction.DOWN:
                new_head = SnakeBlock(head.x, head.y + CELL_SIZE, CELL_SIZE, CELL_SIZE)
            case Direction.LEFT:
                new_head = SnakeBlock(head.x - CELL_SIZE, head.y, CELL_SIZE, CELL_SIZE)
            case Direction.RIGHT:
                new_head = SnakeBlock(head.x + CELL_SIZE, head.y, CELL_SIZE, CELL_SIZE)

        self.body = [new_head] + self.body[:-1]
        self.direction_changed = False

    def grow(self):
        """Grows the snake by adding a new block to its body."""
        last_block: SnakeBlock = self.body[-1]
        new_block: SnakeBlock = SnakeBlock(0, 0, 0, 0)
        match self.direction:
            case Direction.UP:
                new_block = SnakeBlock(last_block.x, last_block.y + CELL_SIZE, CELL_SIZE, CELL_SIZE)
            case Direction.DOWN:
                new_block = SnakeBlock(last_block.x, last_block.y - CELL_SIZE, CELL_SIZE, CELL_SIZE)
            case Direction.LEFT:
                new_block = SnakeBlock(last_block.x + CELL_SIZE, last_block.y, CELL_SIZE, CELL_SIZE)
            case Direction.RIGHT:
                new_block = SnakeBlock(last_block.x - CELL_SIZE, last_block.y, CELL_SIZE, CELL_SIZE)

        self.body.append(new_block)

    def change_direction(self, new_direction: Direction):
        """Changes the direction of the snake if it is not reversing."""
        if not self.direction_changed and \
                ((self.direction == Direction.UP and new_direction != Direction.DOWN) or
                 (self.direction == Direction.DOWN and new_direction != Direction.UP) or
                 (self.direction == Direction.LEFT and new_direction != Direction.RIGHT) or
                 (self.direction == Direction.RIGHT and new_direction != Direction.LEFT)):
            self.direction = new_direction
            self.direction_changed = True

    def check_collision_border(self) -> bool:
        """Checks if the snake has collided with the border or itself."""
        head: SnakeBlock = self.body[0]
        if head.x < 0 or head.x >= SCREEN_WIDTH or head.y < 0 or head.y >= SCREEN_HEIGHT:
            return True
        snakeBlock: SnakeBlock
        for snakeBlock in self.body[1:]:
            if head.x == snakeBlock.x and head.y == snakeBlock.y:
                return True
        return False

    def check_collision_food(self, f: Food) -> bool:
        """Checks if the snake has collided with the food."""
        head: SnakeBlock = self.body[0]
        return head.x == f.x and head.y == f.y


snake = Snake()
food = Food.create_random_food()

UPDATE_RATE = 0.125
accumulator = 0.0

while running:
    dt = clock.tick(60) / 1000.0
    accumulator += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_w:
                    snake.change_direction(Direction.UP)
                case pygame.K_s:
                    snake.change_direction(Direction.DOWN)
                case pygame.K_a:
                    snake.change_direction(Direction.LEFT)
                case pygame.K_d:
                    snake.change_direction(Direction.RIGHT)

    while accumulator >= UPDATE_RATE:
        snake.move()
        if snake.check_collision_border():
            running = False
        if snake.check_collision_food(food):
            snake.grow()
            food = Food.create_random_food()
        accumulator -= UPDATE_RATE

    screen.fill("light green")
    draw_grid()

    pygame.draw.rect(screen, "red", (food.x, food.y, food.width, food.height))

    for block in snake.body:
        pygame.draw.rect(screen, "black", (block.x, block.y, block.width, block.height))

    pygame.display.flip()

pygame.quit()
