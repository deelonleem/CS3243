import sys, math

# GLOBAL VARIABLES:
allletters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#############################################################################
######## Board
#############################################################################
class Board:
    def __init__(self, rows, cols, grid, enemies, king, goals):
        self.rows = rows
        self.cols = cols
        self.grid = grid # 2D matrix, 1 = empty, -1 = Obstacle, Z = cost
        self.enemies = enemies # ["Piece", (y,x)]
        self.king = king # [("King", (y,x))]
        self.goals = goals #[(y,x)]
        self.board = [[None for j in range(cols)] for i in range(rows)] # 2D Matrix for board [y][x]
        self.setBoard(grid, enemies, king, goals, rows, cols)
        
    def makeBoard(self):
        for letter in self.horz:
            for num in self.vert:
                self.board[(letter, num)] = None

    def setBoard(self, grid, enemies, king, goals, rows, cols): # Sets the board with puzzle pieces
        # 1) Putting obstacles on the board
        for y in range(rows):
            for x in range(cols):
                if grid[y][x] == -1:
                    self.board[y][x] = "Obstacle"
        # 2) Putting enemy pieces on the board + their threats
        for pair in enemies:
            self.board[pair[1][0]][pair[1][1]] = pair[0]
            if pair[0] == "King":
                enemy = King(pair[1], self.board, rows, cols)
            elif pair[0] == "Rook":
                enemy = Rook(pair[1], self.board, rows, cols)
            elif pair[0] == "Bishop":
                enemy = Bishop(pair[1], self.board, rows, cols)
            elif pair[0] == "Queen":
                enemy = Queen(pair[1], self.board, rows, cols)
            elif pair[0] == "Knight":
                enemy = Knight(pair[1], self.board, rows, cols)
            elif pair[0] == "Ferz":
                enemy = Ferz(pair[1], self.board, rows, cols)
            elif pair[0] == "Princess":
                enemy = Princess(pair[1], self.board, rows, cols)
            elif pair[0] == "Empress":
                enemy = Empress(pair[1], self.board, rows, cols)
            for pos in enemy.threats:
                self.board[pos[0]][pos[1]] = "Threat"
        # 3) Putting goals on board
        for goal in goals:
            if self.board[goal[0]][goal[1]] == None:
                self.board[goal[0]][goal[1]] = "Goal"

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Pieces
#############################################################################
class Piece: # Superclass for all pieces
    def __init__(self, pos, board, rows, cols): # pos is a string of letter followed by number
        self.pos = pos #(y,x) Both Int
        self.start = pos # Keep the original position
        self.rows = rows
        self.cols = cols
        self.y = pos[0]
        self.x = pos[1]
        self.threats = [self.pos] # List of threatened positions
        self.board = board # Keeps board (2D matrix) info to check for presence of other entities

    def moveUp(self):
        if (self.y == 0 or self.board[self.y-1][self.x] != None):
            return None
        else: 
            self.y -= 1
            self.pos = (self.y, self.x)
            return self.pos

    def moveDown(self):
        if (self.y == self.rows-1 or self.board[self.y+1][self.x] != None):
            return None
        else: 
            self.y += 1
            self.pos = (self.y, self.x)
            return self.pos

    def moveLeft(self):
        if (self.x == 0 or self.board[self.y][self.x-1] != None):
            return None
        else:
            self.x -= 1
            self.pos = (self.y, self.x)
            return self.pos

    def moveRight(self):
        if (self.x == self.cols-1 or self.board[self.y][self.x+1] != None):
            return None
        else: 
            self.x += 1
            self.pos = (self.y, self.x)
            return self.pos

    def moveUpLeft(self):
        if (self.x == 0 or self.y == 0 or self.board[self.y-1][self.x-1] != None):
            return None
        else: 
            self.y -= 1
            self.x -= 1
            self.pos = (self.y, self.x)
            return self.pos

    def moveUpRight(self):
        if (self.x == self.cols-1 or self.y == 0 or self.board[self.y-1][self.x+1] != None):
            return None
        else: 
            self.y -= 1
            self.x += 1
            self.pos = (self.y, self.x)
            return self.pos

    def moveDownLeft(self):
        if (self.x == 0 or self.y == self.rows-1 or self.board[self.y+1][self.x-1] != None):
            return None
        else: 
            self.y += 1
            self.x -= 1
            self.pos = (self.y, self.x)
            return self.pos

    def moveDownRight(self):
        if (self.x == self.cols-1 or self.y == self.rows-1 or self.board[self.y+1][self.x+1] != None):
            return None
        else: 
            self.y += 1
            self.x += 1
            self.pos = (self.y, self.x)
            return self.pos
        
    def resetPos(self):
        self.pos = self.start
        self.y = self.start[0]
        self.x = self.start[1]
        

class King(Piece): # Enemy kings, not your own king
    def __init__(self, pos, board, rows, cols):
        super().__init__(pos, board, rows, cols)
        self.loadThreats()
        
    def loadThreats(self):
        temp = []
        temp.append(self.moveUp())
        self.resetPos()
        temp.append(self.moveDown())
        self.resetPos()
        temp.append(self.moveLeft())
        self.resetPos()
        temp.append(self.moveRight())
        self.resetPos()
        temp.append(self.moveUpLeft())
        self.resetPos()
        temp.append(self.moveUpRight())
        self.resetPos()
        temp.append(self.moveDownLeft())
        self.resetPos()
        temp.append(self.moveDownRight())
        self.resetPos()
        for item in temp:
            if item != None:
                self.threats.append(item)   
                
                
class Rook(Piece):
    def __init__(self, pos, board, rows, cols):
        super().__init__(pos, board, rows, cols)
        self.loadThreats()
        
    def loadThreats(self):
        temp = []
        while(self.moveUp() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveDown() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveLeft() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveRight() != None):
            temp.append(self.pos)
        self.resetPos()
        for item in temp:
            if item != None:
                self.threats.append(item)
                
                
class Bishop(Piece):
    def __init__(self, pos, board, rows, cols):
        super().__init__(pos, board, rows, cols)
        self.loadThreats()
        
    def loadThreats(self):
        temp = []
        while(self.moveUpRight() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveUpLeft() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveDownRight() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveDownLeft() != None):
            temp.append(self.pos)
        self.resetPos()   
        for item in temp:
            if item != None:
                self.threats.append(item)
           
        
class Queen(Piece):
    def __init__(self, pos, board, rows, cols):
        super().__init__(pos, board, rows, cols)
        self.loadThreats()
        
    def loadThreats(self):
        temp = []
        # Rook Portion
        while(self.moveUp() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveDown() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveLeft() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveRight() != None):
            temp.append(self.pos)
        self.resetPos()
        # Bishop Portion
        while (self.moveUpRight() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveUpLeft() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveDownRight() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveDownLeft() != None):
            temp.append(self.pos)
        self.resetPos()
        for item in temp:
            if item != None:
                self.threats.append(item)
                
                
class Knight(Piece):
    def __init__(self, pos, board, rows, cols):
        super().__init__(pos, board, rows, cols)
        self.loadThreats()
        
    def loadThreats(self): # Manually check the 8 possible locations
        l_lim = 0
        r_lim = self.cols-1
        d_lim = self.rows-1
        u_lim = 0
        x = self.x
        y = self.y
        temp = []
        # R2U1 Square
        if ((x+2) <= r_lim and (y-1) >= u_lim):
            temp.append((y-1, x+2))
        # R1U2 Square
        if ((x+1) <= r_lim and (y-2) >= u_lim):
            temp.append((y-2, x+1))
        # L1U2 Square
        if ((x-1) >= l_lim and (y-2) >= u_lim):
            temp.append((y-2, x-1))
        # L2U1 Square
        if ((x-2) >= l_lim and (y-1) >= u_lim):
            temp.append((y-1, x-2))
        # L2D1 Square
        if ((x-2) >= l_lim and (y+1) <= d_lim):
            temp.append((y+1, x-2))
        # L1D2 Square
        if ((x-1) >= l_lim and (y+2) <= d_lim):
            temp.append((y+2, x-1))
        # R1D2 Square
        if ((x+1) <= r_lim and (y+2) <= d_lim):
            temp.append((y+2, x+1))
        # R2D1 Square
        if ((x+2) <= r_lim and (y+1) <= d_lim):
            temp.append((y+1, x+2))
        for item in temp:
            self.threats.append(item)
           
        
class Ferz(Piece):
    def __init__(self, pos, board, rows, cols):
        super().__init__(pos, board, rows, cols)
        self.loadThreats()
        
    def loadThreats(self):
        temp = []
        temp.append(self.moveUpLeft())
        self.resetPos()
        temp.append(self.moveUpRight())
        self.resetPos()
        temp.append(self.moveDownLeft())
        self.resetPos()
        temp.append(self.moveDownRight())
        self.resetPos()
        for item in temp:
            if item != None:
                self.threats.append(item) 
                
                
class Princess(Piece):
    def __init__(self, pos, board, rows, cols):
        super().__init__(pos, board, rows, cols)
        self.loadThreats()
        
    def loadThreats(self):
        temp = []
        # Bishop Portion
        while (self.moveUpRight() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveUpLeft() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveDownRight() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveDownLeft() != None):
            temp.append(self.pos)
        self.resetPos()  
        # Knight Portion
        l_lim = 0
        r_lim = self.cols-1
        d_lim = self.rows-1
        u_lim = 0
        x = self.x
        y = self.y
        # R2U1 Square
        if ((x+2) <= r_lim and (y-1) >= u_lim):
            temp.append((y-1, x+2))
        # R1U2 Square
        if ((x+1) <= r_lim and (y-2) >= u_lim):
            temp.append((y-2, x+1))
        # L1U2 Square
        if ((x-1) >= l_lim and (y-2) >= u_lim):
            temp.append((y-2, x-1))
        # L2U1 Square
        if ((x-2) >= l_lim and (y-1) >= u_lim):
            temp.append((y-1, x-2))
        # L2D1 Square
        if ((x-2) >= l_lim and (y+1) <= d_lim):
            temp.append((y+1, x-2))
        # L1D2 Square
        if ((x-1) >= l_lim and (y+2) <= d_lim):
            temp.append((y+2, x-1))
        # R1D2 Square
        if ((x+1) <= r_lim and (y+2) <= d_lim):
            temp.append((y+2, x+1))
        # R2D1 Square
        if ((x+2) <= r_lim and (y+1) <= d_lim):
            temp.append((y+1, x+2))
        for item in temp:
            self.threats.append(item)
            
class Empress(Piece):
    def __init__(self, pos, board, rows, cols):
        super().__init__(pos, board, rows, cols)
        self.loadThreats()
        
    def loadThreats(self):
        temp = []
        # Rook Portion
        while(self.moveUp() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveDown() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveLeft() != None):
            temp.append(self.pos)
        self.resetPos()
        while(self.moveRight() != None):
            temp.append(self.pos)
        self.resetPos()
        # Knight Portion
        l_lim = 0
        r_lim = self.cols-1
        d_lim = self.rows-1
        u_lim = 0
        x = self.x
        y = self.y
        # R2U1 Square
        if ((x+2) <= r_lim and (y-1) >= u_lim):
            temp.append((y-1, x+2))
        # R1U2 Square
        if ((x+1) <= r_lim and (y-2) >= u_lim):
            temp.append((y-2, x+1))
        # L1U2 Square
        if ((x-1) >= l_lim and (y-2) >= u_lim):
            temp.append((y-2, x-1))
        # L2U1 Square
        if ((x-2) >= l_lim and (y-1) >= u_lim):
            temp.append((y-1, x-2))
        # L2D1 Square
        if ((x-2) >= l_lim and (y+1) <= d_lim):
            temp.append((y+1, x-2))
        # L1D2 Square
        if ((x-1) >= l_lim and (y+2) <= d_lim):
            temp.append((y+2, x-1))
        # R1D2 Square
        if ((x+1) <= r_lim and (y+2) <= d_lim):
            temp.append((y+2, x+1))
        # R2D1 Square
        if ((x+2) <= r_lim and (y+1) <= d_lim):
            temp.append((y+1, x+2))
        for item in temp:
            self.threats.append(item)


#############################################################################
######## Implement Search Algorithm
#############################################################################
# Priority queue class to be used for ucs 
class PQ():
    def __init__(self):
        self.list = []

    def isEmpty(self):
        return (len(self.list) == 0)

    def enqueue(self, pos, cost): 
        self.list.append((pos, cost))

    def dequeue(self): # Dequeue based on lowest cost
        if self.isEmpty():
            return None
        min_cost = math.inf
        min_item = ()
        for item in self.list: # Item is (pos, cost)
            if item[1] < min_cost:
                min_cost = item[1]
                min_item = item
        self.list.remove(min_item)
        return min_item

def search(rows, cols, grid, enemy_pieces, own_pieces, goals):
    game = Board(rows, cols, grid, enemy_pieces, own_pieces, goals) # 2D matrix of the whole game
    frontier = PQ() # Frontier for UCS, priority queue is used ((y,x), cost)
    parents = {} # Dictionary to keep track of parents k:v = pos:parent pos
    costs = {} # Dictionary to keep track of shortest cost from start node to any node k:v= pos:cost
    for y in range(rows): # Initialising all initial costs to be infinity
        for x in range(cols):
            costs[(y, x)] = math.inf
    start = game.king[0][1] # (y,x) starting position
    costs[start] = 0
    frontier.enqueue(start, 0)
    visited = [start] # List for visited coordinates
    
    goal = ()

    # Just check for trivial case: start = goal
    if (start in goals):
        return [], 0

    while (True): # Keep running till exit condition is satisfied
        if frontier.isEmpty(): # If no more possible moves
            return [], 0
        curr = frontier.dequeue() # Early goal test, curr is ((y,x), cost)
        y = curr[0][0]
        x = curr[0][1]
        if game.board[y][x] == "Goal":
            visited.append(curr)
            goal = ((y,x), curr[1])
            break
        up = (y-1, x)
        upLeft = (y-1, x-1)
        left = (y, x-1)
        downLeft = (y+1, x-1)
        down = (y+1, x)
        downRight = (y+1, x+1)
        right = (y, x+1)
        upRight = (y-1, x+1)

        if (isValid(visited, up, rows, cols) and (game.board[up[0]][up[1]] == None or game.board[up[0]][up[1]] == "Goal")) and (costs[up] > costs[curr[0]] + grid[up[0]][up[1]]):
            cost = costs[curr[0]] + grid[up[0]][up[1]]
            costs[up] = cost
            frontier.enqueue(up, cost)
            visited.append(up)
            parents[up] = curr[0]

        if (isValid(visited, upLeft, rows, cols) and (game.board[upLeft[0]][upLeft[1]] == None or game.board[upLeft[0]][upLeft[1]] == "Goal")) and (costs[upLeft] > costs[curr[0]] + grid[upLeft[0]][upLeft[1]]):
            cost = costs[curr[0]] + grid[upLeft[0]][upLeft[1]]
            costs[upLeft] = cost
            frontier.enqueue(upLeft, cost)
            visited.append(upLeft)
            parents[upLeft] = curr[0]

        if (isValid(visited, left, rows, cols) and (game.board[left[0]][left[1]] == None or game.board[left[0]][left[1]] == "Goal")) and (costs[left] > costs[curr[0]] + grid[left[0]][left[1]]):
            cost = costs[curr[0]] + grid[left[0]][left[1]]
            costs[left] = cost
            frontier.enqueue(left, cost)
            visited.append(left)
            parents[left] = curr[0]

        if (isValid(visited, downLeft, rows, cols) and (game.board[downLeft[0]][downLeft[1]] == None or game.board[downLeft[0]][downLeft[1]] == "Goal")) and (costs[downLeft] > costs[curr[0]] + grid[downLeft[0]][downLeft[1]]):
            cost = costs[curr[0]] + grid[downLeft[0]][downLeft[1]]
            costs[downLeft] = cost
            frontier.enqueue(downLeft, cost)
            visited.append(downLeft)
            parents[downLeft] = curr[0]

        if (isValid(visited, down, rows, cols) and (game.board[down[0]][down[1]] == None or game.board[down[0]][down[1]] == "Goal")) and (costs[down] > costs[curr[0]] + grid[down[0]][down[1]]):
            cost = costs[curr[0]] + grid[down[0]][down[1]]
            costs[down] = cost
            frontier.enqueue(down, cost)
            visited.append(down)
            parents[down] = curr[0]

        if (isValid(visited, downRight, rows, cols) and (game.board[downRight[0]][downRight[1]] == None or game.board[downRight[0]][downRight[1]] == "Goal")) and (costs[downRight] > costs[curr[0]] + grid[downRight[0]][downRight[1]]):
            cost = costs[curr[0]] + grid[downRight[0]][downRight[1]]
            costs[downRight] = cost
            frontier.enqueue(downRight, cost)
            visited.append(downRight)
            parents[downRight] = curr[0]

        if (isValid(visited, right, rows, cols) and (game.board[right[0]][right[1]] == None or game.board[right[0]][right[1]] == "Goal")) and (costs[right] > costs[curr[0]] + grid[right[0]][right[1]]):
            cost = costs[curr[0]] + grid[right[0]][right[1]]
            costs[right] = cost
            frontier.enqueue(right, cost)
            visited.append(right)
            parents[right] = curr[0]

        if (isValid(visited, upRight, rows, cols) and (game.board[upRight[0]][upRight[1]] == None or game.board[upRight[0]][upRight[1]] == "Goal")) and (costs[upRight] > costs[curr[0]] + grid[upRight[0]][upRight[1]]):
            cost = costs[curr[0]] + grid[upRight[0]][upRight[1]]
            costs[upRight] = cost
            frontier.enqueue(upRight, cost)
            visited.append(upRight)
            parents[upRight] = curr[0]
            
    # Post processing here, then return moves
    # We want final result in the form of [[(x1, y1),(x2,y2)], [(x2,y2)(x3,y3)]...] 
    # x now becomes string and not int anymore

    # curr currently holds (goal, cost)
    path = [curr[0]] # List of (y,x) from start to goal
    moves = []
    temp = curr[0] # temp starts from the goal

    while True:
        parent = parents[temp]
        path.insert(0, parent)
        if parent == start: # End of the back tracking
            break
        temp = parent
    for i in range(len(path)-1):
        x1 = allletters[path[i][1]]
        y1 = path[i][0]
        x2 = allletters[path[i+1][1]]
        y2 = path[i+1][0]
        moves.append([(x1, y1), (x2, y2)])
    return moves, costs[goal[0]]
    
def isValid(visited, pos, rows, cols):
    x = pos[1]
    y = pos[0]
    # If cell is out of bounds
    if (x<0 or x>=cols or y<0 or y>=rows):
        return False
    # If cell is already visited
    if (pos in visited):
        return False
    else: 
        return True


#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
# Return number of rows, cols, grid containing obstacles and step costs of coordinates, enemy pieces, own piece, and goal positions
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline())) # Integer
    cols = int(get_par(handle.readline())) # Integer
    grid = [[1 for j in range(cols)] for i in range(rows)] # Dictionary, label empty spaces as 1 (Default Step Cost)
    enemy_pieces = [] # List
    own_pieces = [] # List
    goals = [] # List

    handle.readline()  # Ignore number of obstacles
    for ch_coord in get_par(handle.readline()).split():  # Init obstacles
        r, c = from_chess_coord(ch_coord)
        grid[r][c] = -1 # Label Obstacle as -1

    handle.readline()  # Ignore Step Cost header
    line = handle.readline()
    while line.startswith("["):
        line = line[1:-2].split(",")
        r, c = from_chess_coord(line[0])
        grid[r][c] = int(line[1]) if grid[r][c] == 1 else grid[r][c] #Reinitialize step cost for coordinates with different costs
        line = handle.readline()
    
    line = handle.readline() # Read Enemy Position
    while line.startswith("["):
        line = line[1:-2]
        piece = add_piece(line)
        enemy_pieces.append(piece)
        line = handle.readline()

    # Read Own King Position
    line = handle.readline()[1:-2]
    piece = add_piece(line)
    own_pieces.append(piece)

    # Read Goal Positions
    for ch_coord in get_par(handle.readline()).split():
        r, c = from_chess_coord(ch_coord)
        goals.append((r, c))
    
    return rows, cols, grid, enemy_pieces, own_pieces, goals

def add_piece( comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [piece, (r,c)]

def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: List of moves and nodes explored
def run_UCS():
    testcase = sys.argv[1]
    rows, cols, grid, enemy_pieces, own_pieces, goals = parse(testcase)
    moves, pathcost = search(rows, cols, grid, enemy_pieces, own_pieces, goals)
    return moves, pathcost

# # Execution
# print(run_UCS())
