import pygame
from dataclasses import dataclass
from enum import Enum
from typing import List

pygame.init()
SCREEN_WIDTH: int = 700
SCREEN_HEIGHT: int = 700
CELL_SIZE: int = 35

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True


class Direction(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4


@dataclass
class Food:
    x: int
    y: int
    width: int
    height: int


@dataclass
class SnakeBlock:
    x: int
    y: int
    width: int
    height: int


class Snake:
    def __init__(self):
        self.body: List[SnakeBlock] = []
        self.direction = Direction.RIGHT
        self.body.append(SnakeBlock(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, CELL_SIZE, CELL_SIZE))

    def move(self):
        # Calculate new position of the head
        head = self.body[0]
        if self.direction == Direction.UP:
            new_head = SnakeBlock(head.x, head.y - CELL_SIZE, CELL_SIZE, CELL_SIZE)
        elif self.direction == Direction.DOWN:
            new_head = SnakeBlock(head.x, head.y + CELL_SIZE, CELL_SIZE, CELL_SIZE)
        elif self.direction == Direction.LEFT:
            new_head = SnakeBlock(head.x - CELL_SIZE, head.y, CELL_SIZE, CELL_SIZE)
        elif self.direction == Direction.RIGHT:
            new_head = SnakeBlock(head.x + CELL_SIZE, head.y, CELL_SIZE, CELL_SIZE)

        # Move the body
        self.body = [new_head] + self.body[:-1]

    def grow(self):
        # Get the last block in the body
        last_block = self.body[-1]

        # Determine the new block's position based on the direction of the last block
        if self.direction == Direction.UP:
            new_block = SnakeBlock(last_block.x, last_block.y + CELL_SIZE, CELL_SIZE, CELL_SIZE)
        elif self.direction == Direction.DOWN:
            new_block = SnakeBlock(last_block.x, last_block.y - CELL_SIZE, CELL_SIZE, CELL_SIZE)
        elif self.direction == Direction.LEFT:
            new_block = SnakeBlock(last_block.x + CELL_SIZE, last_block.y, CELL_SIZE, CELL_SIZE)
        elif self.direction == Direction.RIGHT:
            new_block = SnakeBlock(last_block.x - CELL_SIZE, last_block.y, CELL_SIZE, CELL_SIZE)

        # Add the new block to the end of the body
        self.body.append(new_block)

    def change_direction(self, new_direction: Direction):
        # Prevent the snake from reversing
        if (self.direction == Direction.UP and new_direction != Direction.DOWN) or \
                (self.direction == Direction.DOWN and new_direction != Direction.UP) or \
                (self.direction == Direction.LEFT and new_direction != Direction.RIGHT) or \
                (self.direction == Direction.RIGHT and new_direction != Direction.LEFT):
            self.direction = new_direction

    def check_collision_border(self) -> bool:
        head = self.body[0]

        # Check collision with boundaries
        if head.x < 0 or head.x >= SCREEN_WIDTH or head.y < 0 or head.y >= SCREEN_HEIGHT:
            return True

        # Check collision with itself
        for block in self.body[1:]:
            if head.x == block.x and head.y == block.y:
                return True

        return False

    def check_collision_food(self, food: Food) -> bool:
        head = self.body[0]

        # Check collision with boundaries
        if head.x == food.x and head.x == food.y:
            return True

        return False


snake = Snake()

# Fixed time step for game logic updates (in seconds)
UPDATE_RATE = 0.125  # Update game logic every 125 milliseconds (8 updates per second)

# Time accumulator
accumulator = 0.0

f = Food(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2, CELL_SIZE, CELL_SIZE)

while running:
    dt = clock.tick(60) / 1000.0  # Amount of time since the last frame (in seconds)
    accumulator += dt

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                snake.change_direction(Direction.UP)
            elif event.key == pygame.K_s:
                snake.change_direction(Direction.DOWN)
            elif event.key == pygame.K_a:
                snake.change_direction(Direction.LEFT)
            elif event.key == pygame.K_d:
                snake.change_direction(Direction.RIGHT)
            elif event.key == pygame.K_SPACE:
                snake.grow()

    # Update game logic with fixed time step
    while accumulator >= UPDATE_RATE:
        snake.move()
        if snake.check_collision_border():
            print("Collision detected! Game over.")
            running = False
        if snake.check_collision_food(f):
            print("Collision detected! Food eaten.")
        accumulator -= UPDATE_RATE

    screen.fill("light green")

    pygame.draw.rect(screen,"red", (f.x, f.y, f.width, f.height))

    for s in snake.body:
        pygame.draw.rect(screen, "black", (s.x, s.y, s.width, s.height))

    pygame.display.flip()

pygame.quit()
