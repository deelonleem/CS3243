import sys

# GLOBAL VARIABLES:
allletters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
piece_types = ["King", "Queen", "Bishop", "Rook", "Knight", "Ferz", "Princess", "Empress"]
# In the format: (dy, dx, max step)
piece_steps = {"King": [(1, 1, 1), (1, 0, 1), (1, -1, 1), (0, -1, 1), (-1, -1, 1), (-1, 0, 1), (-1, 1, 1), (0, 1, 1)],
            "Rook": [(1, 0, 0), (0, -1, 0), (-1, 0, 0), (0, 1, 0)],
            "Bishop": [(1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)],
            "Queen": [(1, 0, 0), (0, -1, 0), (-1, 0, 0), (0, 1, 0), (1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)],
            "Knight": [(2, 1, 1), (2, -1, 1), (1, 2, 1), (1, -2, 1), (-2, 1, 1), (-2, -1, 1), (-1, 2, 1), (-1, -2, 1)],
            "Ferz": [(1, 1, 1), (1, -1, 1), (-1, -1, 1), (-1, 1, 1)],
            "Empress": [(1, 0, 0), (0, -1, 0), (-1, 0, 0), (0, 1, 0), (2, 1, 1), (2, -1, 1), (1, 2, 1), (1, -2, 1), (-2, 1, 1), (-2, -1, 1), (-1, 2, 1), (-1, -2, 1)],
            "Princess": [(1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0), (2, 1, 1), (2, -1, 1), (1, 2, 1), (1, -2, 1), (-2, 1, 1), (-2, -1, 1), (-1, 2, 1), (-1, -2, 1)]}

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Classes - Board, State, Assignment, ThreatFinding
#############################################################################
class Board:
    def __init__(self, rows, cols, obstaclelist, max_pieces):
        self.rows = rows
        self.cols = cols
        self.max_pieces = max_pieces
        self.pieces = {}  # Key: Pos, Value: Name of piece
        self.piece_count = {"King": 0, "Queen": 0, "Bishop": 0, "Rook": 0, "Knight": 0, "Ferz": 0, "Princess": 0, "Empress": 0} # Count of number of each piece type
        self.possible_pieces = [] # 2D Array that stores possible enemies for a square
        dict = {}
        for piece in piece_types:
            if max_pieces[piece] > 0:
                dict[piece] = True
        for y in range(rows):
            self.possible_pieces.append([])
            for x in range(cols):
                self.possible_pieces[y].append(dict.copy()) 
        
        self.obstacles = [] # Contains positions of obstacles
        for pos in obstaclelist: # Add obstacles to self.obstacles
            self.obstacles.append((pos[0],pos[1]))
            self.possible_pieces[pos[0]][pos[1]] = {}

    def addPiece(self, name, y, x): # Add a piece at position (y,x)
        self.pieces[(y, x)] = name # Update self.pieces
        self.possible_pieces[y][x] = {name: True} # Update possible enemies
        self.piece_count[name] += 1 # Update piece count
        
        # Find threats of the piece, and empty its possible enemies
        threatFinder = ThreatFinding(self, y, x, name) # ThreatFinding class
        def fn(y, x):
            self.possible_pieces[y][x] = {}
        threatFinder.loadThreats(fn)

        # Update for all other pieces as well
        for others in piece_types:
            if others == name:
                continue
            threatFinder = ThreatFinding(self, y, x, others)
            def fn(y, x):
                if others in self.possible_pieces[y][x]:
                    del self.possible_pieces[y][x][others]
            threatFinder.loadThreats(fn)      

    def isThreatened(self, y, x): # Is a position threatened by a piece or there is an obstacle?
        if ((y,x) in self.obstacles) or ((y,x) in self.pieces):
            return True
        else: 
            return False

    def inBounds(self, y, x): # Is a position (y,x) in bounds of the board?
        if (0 > y or y >= self.rows) or (0 > x or x >= self.cols):
            return False
        else:
            return True


class State:
    def __init__(self, rows, cols, obstaclelist, max_pieces):
        self.board = Board(rows, cols, obstaclelist, max_pieces)
        self.rows = rows
        self.cols = cols
        self.obstaclelist = obstaclelist
        self.max_pieces = max_pieces
        
    def setAssignment(self, assignment): # Given an assignment, update the attributes of the state
        self.board = Board(self.cols, self.rows, self.obstaclelist, self.max_pieces)
        for pos in assignment:
            self.board.addPiece(assignment[pos], pos[0], pos[1])
    
    def addPiece(self, name, pos): # Add a piece to the state - Call board's addPiece
        self.board.addPiece(name, pos[0], pos[1])

    def inference(self): # Inference function that searches for failure early
        remaining = sum([self.max_pieces[name] for name in piece_types]) - len(self.board.pieces) # Number of pieces to be assigned
        spaces = 0 # Number of available spaces
        for y in range(self.rows):
            for x in range(self.cols):
                if self.board.isThreatened(y, x):
                    continue
                if len(self.board.possible_pieces[y][x]) > 0:
                    spaces += 1
        return (spaces >= remaining) # There should be more spaces than pieces to be assigned


class Assignment:
    def __init__(self, max_pieces):
        self.max_pieces = max_pieces
        self.current_pieces = {} # Key: Name, Values: Number of pieces we have assigned thus far
        self.assignment = {} # Key: (y,x), Values: Name of pieces at that position
        self.done = {} # Key: Pieces, Values: Positions (y,x) that we have tried already
        for name in piece_types: # Init both dictionaries
            self.current_pieces[name] = 0
            self.done[name] = {}

    def goalTest(self): # Goal test! Is our assignment done?
        for name in piece_types:
            if self.current_pieces[name] != self.max_pieces[name]:
                return False
        return True

    def copy(self): # Copy an assignment
        new = Assignment(self.max_pieces)
        for pos in self.assignment:
            new.assign(self.assignment[pos], pos)
        for name in piece_types:
            new.done[name] = self.done[name].copy()
        return new

    def assign(self, name, pos): # Assign a piece to pos (y,x) 
        self.current_pieces[name] += 1
        self.assignment[pos] = name
        self.done[name][pos] = True
    
    def unassign(self, name, pos): # Unassign a piece from a pos (y,x)
        self.current_pieces[name] -= 1
        del self.assignment[pos]


class ThreatFinding():
    def __init__(self, board, y, x, name):
        self.board = board
        self.y = y
        self.x = x
        self.steps = piece_steps[name]

    def move(self, dy, dx): # Move by a distance (dy, dx)
        return (self.y+dy, self.x+dx)

    def loadThreats(self, fn = None):
        if fn == None :
            threats = []
            for step in self.steps:
                dy, dx, max_step = step
                threats.extend(self.recursive_loadThreats(dy, dx, max_step))
            return threats
        else:
            for step in self.steps:
                dy, dx, max_step = step
                self.recursive_loadThreats(dy, dx, max_step, fn)

    def recursive_loadThreats(self, dy, dx, max_step=0, fn = None):
        if max_step == 0:
            max_step = max(self.board.rows, self.board.cols)
        
        if fn == None:
            steps = []
            for i in range(max_step):
                new_pos = self.move((i+1)*dy, (i+1)*dx)
                if self.board.inBounds(new_pos[0], new_pos[1]) == False: # If new position is out of bounds
                    break
                if self.board.isThreatened(new_pos[0], new_pos[1]) == True: # If we encounter an obstacle
                    steps.append(new_pos)
                    break
                steps.append(new_pos)
            return steps
        else:
            for i in range(max_step):
                new_pos = self.move((i+1)*dy, (i+1)*dx)
                if self.board.inBounds(new_pos[0], new_pos[1]) == False: # If new position is out of bounds
                    break
                if self.board.isThreatened(new_pos[0], new_pos[1]) == True: # If we encounter an obstacle
                    fn(new_pos[0], new_pos[1])
                    break
                fn(new_pos[0], new_pos[1])

    def possibleMoves(self):
        num_moves = 0
        for step in self.steps:
            dy, dx, max_step = step
            num_moves += self.recursive_possibleMoves(dy, dx, max_step)
        return num_moves
    
    def recursive_possibleMoves(self, dy, dx, max_step=0):
        if max_step == 0:
            max_step = max(self.board.rows, self.board.cols)
        num_moves = 0
        for i in range(max_step):
            new_pos = self.move((i+1)*dy, (i+1)*dx)
            if self.board.inBounds(new_pos[0], new_pos[1]) == False: # If new position is out of bounds
                break
            if self.board.isThreatened(new_pos[0], new_pos[1]) == True: # If we encounter an obstacle
                num_moves += 1
                break
            num_moves += 1
        return num_moves

#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
def choosePiece(state, assignment): # Heuristic to choose which is the next piece to place
    remaining = [] # Pieces that are yet to be assigned
    for name in piece_types:
        if assignment.current_pieces[name] == assignment.max_pieces[name]: # If that piece is done, we skip it
            continue
        remaining.append(name)
    if len(remaining) == 1: # If only one piece type, we just choose it
        return remaining[0]
    min = state.rows * state.cols
    best = None
    for name in remaining: # How many squares on the board contains this piece?
        count = 0
        flag = False
        for y in range(state.rows):
            for x in range(state.cols):
                if name in state.board.possible_pieces[y][x]:
                    count += 1
                    if count > min:
                        flag = True
                        break
        if flag == True:
            continue
        if count == 1:
            return name
        best = name
        min = count
    return best

def orderPositions(state, name, assignment):
    positions = []
    for y in range(state.rows):
        for x in range(state.cols):
            if ((y, x) in state.board.pieces) or (name not in state.board.possible_pieces[y][x]) or ((y, x) in assignment.done[name]):
                continue
            threatFinder = ThreatFinding(state.board, y, x, name)
            positions.append((threatFinder.possibleMoves(), (y, x)))
    positions.sort()
    return positions

def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline()))
    cols = int(get_par(handle.readline()))
    grid = [[0 for j in range(cols)] for i in range(rows)]

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()
    
    piece_nums = get_par(handle.readline()).split()
    num_pieces = [int(x) for x in piece_nums] #List in the order of King, Queen, Bishop, Rook, Knight

    return rows, cols, grid, num_pieces

def add_piece( comma_seperated):
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r,c), piece]

#Returns row and col index in integers respectively
def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)
def letterToX(character) -> int:
    return ord(character) - ord('a')

def backTrack(state, assignment):
    piece = choosePiece(state, assignment) # Choose piece to assign
    positions = orderPositions(state, piece, assignment) # Order positions to consider
    for num, position in positions: # Iterate through the postitions
        assignment.assign(piece, position)
        state.addPiece(piece, position)
        if assignment.goalTest(): # We are done! 
            return assignment.assignment
        bool = state.inference()
        if bool != False:
            result = backTrack(state, assignment.copy())
            if result != False:
                return result
        assignment.unassign(piece, position) # If failure is detected, undo
        state.setAssignment(assignment.assignment)
    return False

def search(rows, cols, grid, num_pieces):
    max_pieces = {"King": int(num_pieces[0]), "Queen": int(num_pieces[1]), "Bishop": int(num_pieces[2]), "Rook": int(num_pieces[3]), "Knight": int(num_pieces[4]), "Ferz": int(num_pieces[5]), "Princess": int(num_pieces[6]), "Empress": int(num_pieces[7])} 
    for name in max_pieces:
        if max_pieces[name] == 0:
            piece_types.remove(name) # If this piece is not in the puzzle, we don't consider it at all

    obstaclelist = [] # Append the list of obstacles
    for y in range(rows):
        for x in range(cols):
            if grid[y][x] == -1:
                obstaclelist.append((y,x))

    initial = State(rows, cols, obstaclelist, max_pieces)
    result = backTrack(initial, Assignment(initial.max_pieces))
    goal = {} 
    for pos in result: # Final data processing to format return dict
        x = allletters[pos[1]]
        y = pos[0]
        goal[(x, y)] = result[pos]
    
    return goal

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces (String): King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_CSP():
    testcase = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, grid, num_pieces = parse(testcase)
    goalstate = search(rows, cols, grid, num_pieces)
    return goalstate #Format to be returned

# Execution statement
# print(run_CSP())
