import pygame
import random
import queue
import numpy as np
import math
import tkinter as tk
from tkinter import simpledialog
from tkinter import messagebox

# Constants
GRID_SIZE = 15
BLOCK_SIZE = 40
WIDTH = GRID_SIZE * BLOCK_SIZE
HEIGHT = GRID_SIZE * BLOCK_SIZE
FPS = 10

# Colors
WHITE = (255, 255, 255)
L_BLUE = (173, 216, 230)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN=(170, 255, 0)
BLACK=(0,0,0)

emoji_image = pygame.image.load('car.png')
emoji_image = pygame.transform.scale(emoji_image, (BLOCK_SIZE, BLOCK_SIZE))
emoji_block = pygame.image.load('block.png')
emoji_block = pygame.transform.scale(emoji_block, (BLOCK_SIZE, BLOCK_SIZE))
emoji_end = pygame.image.load('end.png')
emoji_end = pygame.transform.scale(emoji_end, (BLOCK_SIZE, BLOCK_SIZE))
emoji_tick = pygame.image.load('tick.png')
emoji_tick = pygame.transform.scale(emoji_tick, (BLOCK_SIZE, BLOCK_SIZE))
emoji_robot = pygame.image.load('robot.png')
emoji_robot = pygame.transform.scale(emoji_robot, (BLOCK_SIZE, BLOCK_SIZE))


def generate_maze():
    maze = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 5, 0, 0, 5, 1, 0, 0, 1, 0, 1],
        [1, 0, 5, 1, 0, 1, 1, 1, 0, 1, 0, 1, 1, 1, 1],
        [1, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 1],
        [1, 0, 0, 1, 0, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 1],
        [1, 1, 1, 1, 1, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1],
        [1, 0, 5, 0, 0, 1, 1, 1, 1, 0, 1, 1, 1, 0, 0],
        [1, 0, 1, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 1],
        [1, 0, 1, 1, 5, 1, 1, 0, 1, 0, 0, 0, 0, 1, 1],
        [1, 0, 5, 0, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1, 1, 0, 1, 1],
        [1, 0, 0, 5, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1],
        [1, 0, 5, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 5, 1]
    ]
    

    return maze

def shuffle_car_positions(maze):
    empty_positions = [(i, j) for i in range(len(maze)) for j in range(len(maze[0])) if maze[i][j] != 2]
    car_positions = [(i, j) for i in range(len(maze)) for j in range(len(maze[0])) if maze[i][j] == 5]
    random.shuffle(empty_positions)
    new_maze = [[maze[i][j] for j in range(len(maze[0]))] for i in range(len(maze))]  # Create a copy of the maze
    for index, (i, j) in enumerate(car_positions):
        new_maze[i][j] = 0  # Clear the original car position
    for index, (i, j) in enumerate(empty_positions[:len(car_positions)]):
        new_maze[i][j] = 5  # Assign the shuffled car positions
    return new_maze


class Robot:
    def __init__(self, start):
        self.x = start[0]
        self.y = start[1]
        self.color = BLUE
        self.rect = pygame.Rect(self.x * BLOCK_SIZE, self.y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE)

    def move(self, direction, maze):
        if direction == 'up':
            self.x -= 1
        elif direction == 'down': 
            self.x += 1
        elif direction == 'left':
            self.y -= 1
        elif direction == 'right':
            self.y += 1
        
        #self.rect.y = self.x * BLOCK_SIZE 
        #self.rect.x = self.y * BLOCK_SIZE

    def draw(self, screen):
        #pygame.draw.rect(screen, self.color, self.rect)
        screen.blit(emoji_robot, (self.y * BLOCK_SIZE, self.x * BLOCK_SIZE))

def draw_maze(screen, maze):
    screen.fill(L_BLUE)
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            # Example code based on provided maze layout:
            if maze[i][j] == 1:  # Block
                 # Blit the emoji image
                screen.blit(emoji_block, (j * BLOCK_SIZE, i * BLOCK_SIZE))
                continue
            elif maze[i][j] == 3:  # Starting point
                color = BLUE
            elif maze[i][j]==9: #destination reached
                # Blit the emoji image
                screen.blit(emoji_tick, (j * BLOCK_SIZE, i * BLOCK_SIZE))
                continue
            elif maze[i][j] == 2:  # Ending point
                 # Blit the emoji image
                screen.blit(emoji_end, (j * BLOCK_SIZE, i * BLOCK_SIZE))
                continue
            elif maze[i][j] == 5:
               # Blit the emoji image
                screen.blit(emoji_image, (j * BLOCK_SIZE, i * BLOCK_SIZE))
                continue
            else:  # Empty space
                color = L_BLUE
            pygame.draw.rect(screen, color, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
            pygame.draw.rect(screen, L_BLUE, (j * BLOCK_SIZE, i * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)


def get_input(title, prompt):
    root = tk.Tk()
    root.withdraw()
    user_input = simpledialog.askstring(title=title, prompt=prompt)
    return user_input


def main():
    maze = generate_maze()
    flag=True
    while(flag):
        # Get number of deliveries
        num_deliveries = int(get_input("Number of Deliveries", "Enter number of deliveries: "))
        # Get delivery details
        delivery_details = []
        for i in range(num_deliveries):
            item = get_input("Delivery {}".format(i+1), "Enter item for delivery (e.g., pizza, burger, etc.): ")
            destination = get_input("Delivery {}".format(i+1), "Enter destination coordinates (x, y) separated by comma: ")
            dest_x, dest_y = map(int, destination.split(','))
            delivery_details.append((item, (dest_x, dest_y)))
        print(delivery_details)

        #taking destination points
        ending_points = []
        for _, destination in delivery_details:
            ending_points.append(destination)

        for point in ending_points:
            x, y = point  # Assuming point is a tuple of (x, y) coordinates
            if maze[x][y] == 1:
                flag=False 
        if(not flag):
            messagebox.showinfo("Message", "invalid input try agian :( ")
            flag=True
        else:
            flag=False
    #----------------------pygame interface-----------------------
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Maze with Robot")
    clock = pygame.time.Clock()

    start=(1,1) #starting point
    
     # Seting ending points
    for row,col in ending_points:
        maze[row][col]=2

    window_closed = False
    # Repeat for number of deliveries
    for i in range(len(ending_points)):
        robot = Robot(start)
        moves = a_star(maze,start,ending_points[i])
        if moves==None:
            draw_maze(screen, maze)
            messagebox.showinfo("Message", f"No path to delivery {i+1} :( ")
            continue
        move_index = 0
        while move_index < len(moves) and not window_closed:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    window_closed = True

            if not window_closed:
                draw_maze(screen, maze)

                # Move robot
                robot.move(moves[move_index], maze)
                robot.draw(screen)
                pygame.display.flip()
                pygame.time.delay(500)
                clock.tick(FPS)

                move_index += 1

        
        messagebox.showinfo("Message", f"destination {i+1} reached :) ")
        maze = shuffle_car_positions(maze)
        start = ending_points[i]
        maze[start[0]][start[1]] = 9
   
    # Quit Pygame after all deliveries are completed or the window is closed
    pygame.quit()



#-------------------------------------------------------------algo implementaion-----------------------------------------------------------------------
def is_valid_move(maze, rows, cols, pos):
    x, y = pos
    if 0 <= x < rows and 0 <= y < cols and maze[x][y] != 1 and maze[x][y] !=5:
        return True
    return False

def calculate_cost(prev_pos, new_pos, direction):
    # checking for cost according to given direction
    if direction == "left":
        return 1
    elif direction == "up":
        return 2
    elif direction == "down":
        return 3
    elif direction == "right":
        return 4
    else:
        return float('inf')  # Default to infinity for invalid direction

def euclidean_distance(start, goal): 
    return math.dist(start,goal)

def a_star(maze,start,goal_pos):
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    direction_names = ["up", "down", "left", "right"]

    rows, cols = len(maze), len(maze[0])

    # Perform A* Search
    frontier = queue.PriorityQueue()
    frontier.put((0, start))
    visited = set()
    max_frontier_size = 0
    paths = {start: []}  # Store paths separately
    costs = {start: 0}  # Store costs to reach each position

    while not frontier.empty():
        max_frontier_size = max(max_frontier_size, frontier.qsize())
        priority, current = frontier.get()

        if current == goal_pos:
            return paths[current]  # Return the path from paths dictionary

        visited.add(current)
        for i in range(len(directions)):
            dirr = directions[i]
            dir_name = direction_names[i]
            new_pos = (current[0] + dirr[0], current[1] + dirr[1])
            if is_valid_move(maze, rows, cols, new_pos) and new_pos not in visited:
                new_cost = costs[current] + calculate_cost(current, new_pos, dir_name)
                priority = new_cost + euclidean_distance(new_pos, goal_pos)
                frontier.put((priority, new_pos))
                visited.add(new_pos)
                costs[new_pos] = new_cost
                paths[new_pos] = paths[current] + [dir_name]  # Add path to paths dictionary
    
    return None  # No paths found
#-------------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    main()
