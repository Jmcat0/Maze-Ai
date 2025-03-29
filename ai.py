import numpy as np

all_solutions = []

class state:
    def __init__(self, position, parent, cost, heuristic, grid, target):
        self.position = position
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.grid = grid
        self.target = target

        self.current_value = self.grid[self.position[1], self.position[0]]
        self.futures = []
        #print('i am number', self.cost, 'at', self.position)

    def up(self):
        return (self.position[0] - 1, self.position[1])
    
    def down(self):
        return (self.position[0] + 1, self.position[1])
    
    def left(self):
        return (self.position[0], self.position[1] - 1)
    
    def right(self):
        return (self.position[0], self.position[1] + 1)
    
    def was_parent_here(self, coords):
        if(self.cost == 0):
            return True
        
        y, x = coords

        current = self.parent
        for i in range(self.cost):
            #print(current.position,'is my parent')
            if current.position == (y,x):
                return False
            current = current.parent
            
        return True

    # Sets avail_moves to true if it can move there
    def check(self):
        
        #print(self.cost, 'is checking val:',self.position)
        #print(self.position,'up:', self.grid[self.up()], 'down:', self.grid[self.down()], 'left:', self.grid[self.left()], 'right:', self.grid[self.right()])

        if(self.grid[self.up()] == ' ' and self.was_parent_here(self.up())):
            self.futures.append((self.position[0] - 1, self.position[1]))
            #print(self.position,'found up')

        if(self.grid[self.down()] == ' '  and self.was_parent_here(self.down())):
            self.futures.append((self.position[0] + 1, self.position[1]))
            #print(self.position,'found down')

        if(self.grid[self.left()] == ' ' and self.was_parent_here(self.left())):
            self.futures.append((self.position[0], self.position[1] - 1))
            #print(self.position,'found left')

        if(self.grid[self.right()] == ' ' and self.was_parent_here(self.right())):
            self.futures.append((self.position[0], self.position[1] + 1))
            #print(self.position,'found right')

        self.move()

    def add_solution(self):
        solution = []

        current = self
        for i in range(self.cost):
            solution.append(current.position)
            current = current.parent

        all_solutions.append(solution)
        print(all_solutions)

    def get_solution():
        return all_solutions

        
    def move(self):
        
        if(self.position == self.target):
            solution = []

            current = self
            for i in range(self.cost + 1):
                solution.append(current.position)
                current = current.parent

            all_solutions.append(solution)
            #print(all_solutions)

        '''print('i am number', self.cost, 'futures', len(self.futures))
        for i in range(len(self.futures)):
            print(self.futures[i])'''

        #self.grid[self.position] = '#'
        for i in range(len(self.futures)):
            new_state = state(self.futures[i], self, self.cost + 1, 0, self.grid, self.target)
            #print(new_state.position,new_state.parent,new_state.cost,new_state.target)
            new_state.check()

    
    