from robot import Robot
from maze import Maze
from code_blocks import CodeBlockManager
import pygame

class Game:
    def __init__(self):
        #self.maze = Maze()
        self.robot = Robot()
        #self.code_block_manager = CodeBlockManager()
        self.visible_group = pygame.sprite.Group()
        self.visible_group.add(self.robot)

    def update(self):
        # Handle updating code block actions
        self.code_block_manager.update()
        # Update robot position based on code blocks
        self.robot.move(self.code_block_manager.get_instructions())

    def draw(self, screen):
        # Draw maze, robot, and code blocks
        self.maze.draw(screen)
        self.robot.draw(screen)
        self.code_block_manager.draw(screen)
    