import random
import numpy as np
import pygame
import ai

# Initialize Pygame
pygame.init()

# Maze settings
cell_size = 10  # Bigger cells
grid_width = 91  # Smaller grid, still odd number
grid_height = 91
window_size = (grid_width * cell_size, grid_height * cell_size)

# Create window
screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Maze Generator")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Create maze grid
grid = np.full((grid_width, grid_height), '#')  # Start with all walls
start = (1, 1)  # Start from (1,1) to leave room for entrance
end = (grid_width-2, grid_height-2)  # End near bottom-right

def create_maze(x, y):
    grid[y, x] = ' '  # Mark current cell as path
    
    directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
    np.random.shuffle(directions)

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy

        if (0 <= new_x < grid_width and 0 <= new_y < grid_height and grid[new_y, new_x] == '#'):
            grid[y + dy//2, x + dx//2] = ' '  # Carve path
            create_maze(new_x, new_y)

def create_complex_maze(x, y, loop_chance=0.15):
    grid[y, x] = ' '  # Mark current cell as path
    
    # Mix of long and short paths
    if random.random() < 0.3:
        directions = [(0, 4), (4, 0), (0, -4), (-4, 0)]  # Long paths
    else:
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]  # Normal paths
    
    np.random.shuffle(directions)

    for dx, dy in directions:
        new_x, new_y = x + dx, y + dy
        mid_x, mid_y = x + dx//2, y + dy//2
        
        if (0 <= new_x < grid_width and 0 <= new_y < grid_height):
            # Create loops occasionally
            if grid[new_y, new_x] == ' ' and random.random() < loop_chance:
                grid[mid_y, mid_x] = ' '
            # Normal path creation
            elif grid[new_y, new_x] == '#':
                grid[mid_y, mid_x] = ' '
                create_complex_maze(new_x, new_y, loop_chance)

def create_maze_kruskal():
    # Initialize each cell as its own set
    sets = {}
    edges = []
    
    # Create list of all possible edges between cells
    for y in range(1, grid_height-1, 2):
        for x in range(1, grid_width-1, 2):
            sets[(y,x)] = (y,x)  # Each cell points to itself initially
            grid[y,x] = ' '  # Mark cells as paths
            
            # Add horizontal edges
            if x < grid_width-2:
                edges.append((y,x,y,x+2))
                
            # Add vertical edges
            if y < grid_height-2:
                edges.append((y,x,y+2,x))
    
    # Randomly shuffle edges            
    random.shuffle(edges)
    
    def find_set(pos):
        # Find the root of the set containing pos
        if sets[pos] != pos:
            sets[pos] = find_set(sets[pos])  # Path compression
        return sets[pos]
    
    def union_sets(pos1, pos2):
        # Merge the sets containing pos1 and pos2
        sets[find_set(pos1)] = find_set(pos2)
    
    # Process edges
    for y1,x1,y2,x2 in edges:
        set1 = find_set((y1,x1))
        set2 = find_set((y2,x2))
        
        if set1 != set2:
            # Connect the cells by removing the wall between them
            grid[y1+(y2-y1)//2, x1+(x2-x1)//2] = ' '
            union_sets((y1,x1), (y2,x2))


# Generate maze (choose one)
create_maze_kruskal()  # Kruskal's algorithm
#create_complex_maze(start[0], start[1])  # Complex maze
#create_maze(start[0], start[1])  # Simple maze


# Create initial state with start position
initial_state = ai.state(start, None, 0, 0, grid, end)  # Using state class from ai.py
initial_state.check()

# Assign solututions to grid
if(len(ai.all_solutions) > 0):
    for y, x in ai.all_solutions[0]:
        if 0 <= y < grid_width and 0 <= x < grid_height:  # Bounds check
            grid[y, x] = '@'
else:
    print('No solution')




# Ensure start and end are paths
grid[start[1], start[0]] = 'S'
grid[end[1], end[0]] = 'E'

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Clear screen
    screen.fill(WHITE)
    
    # Draw maze
    for y in range(grid_height):
        for x in range(grid_width):
            rect = pygame.Rect(x * cell_size - 0.25 * cell_size, y * cell_size - 0.25 * cell_size, cell_size, cell_size)
            path = pygame.Rect(x * cell_size, y * cell_size, cell_size/2, cell_size/2)
            if grid[y, x] == '#':
                pygame.draw.rect(screen, BLACK, rect)
            elif len(ai.all_solutions) > 0 and grid[y, x] == '@':
                pygame.draw.rect(screen, (5, 152, 206), path)
            elif grid[y, x] == 'S':
                pygame.draw.rect(screen, (0, 255, 0), rect)
            elif grid[y, x] == 'E':
                pygame.draw.rect(screen, (255, 0, 0), rect)
    
    # Update display
    pygame.display.flip()

pygame.quit()
