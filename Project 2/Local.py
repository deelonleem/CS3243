import sys, random

# GLOBAL VARIABLES:
allletters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']

#############################################################################
######## Board
#############################################################################
class Board:
    def __init__(self, rows, cols, grid, pieces, k):
        self.rows = rows # Int
        self.cols = cols # Int
        self.grid = grid # 2D matrix, -1 = Obstacle, Else 0
        self.pieces = pieces # Dict {"Piece": (y,x)}
        self.k = k # Int
        
        self.board = [[None for j in range(cols)] for i in range(rows)] # 2D Matrix for board [y][x]
        self.setBoard(rows, cols, grid, pieces)

    def setBoard(self, rows, cols, grid, pieces): # Sets the board with obstacles and pieces
        # 1) Putting obstacles on the board
        for y in range(rows):
            for x in range(cols):
                if grid[y][x] == -1:
                    self.board[y][x] = "Obstacle"
        # 3) Putting enemy pieces on the board
        for pos in pieces:
            name = pieces[pos]
            self.board[pos[0]][pos[1]] = Piece(pos, rows, cols, name)

#############################################################################
######## Piece class
#############################################################################
class Piece: # Superclass for all pieces
    def __init__(self, pos, rows, cols, name):
        self.pos = pos #(y,x) Both Int
        self.rows = rows
        self.cols = cols
        self.name = name
        self.y = pos[0]
        self.x = pos[1]        


#############################################################################
######## Helper Functions
#############################################################################
def loadThreats(Piece, Game, rows, cols): # When given a piece and a game, return a list of positions that the piece threatens
    board = Game.board
    threats = []
    y = Piece.pos[0]
    x = Piece.pos[1]

    if Piece.name == "King":
        if inBounds((y-1, x), rows, cols): # Check Up
            threats.append((y-1, x))
        if inBounds((y-1, x-1), rows, cols): # Check UpLeft
            threats.append((y-1, x-1))
        if inBounds((y, x-1), rows, cols): # Check Left
            threats.append((y, x-1))
        if inBounds((y+1, x-1), rows, cols): # Check DownLeft
            threats.append((y+1, x-1))
        if inBounds((y+1, x), rows, cols): # Check Down
            threats.append((y+1, x))
        if inBounds((y+1, x+1), rows, cols): # Check DownRight
            threats.append((y+1, x+1))
        if inBounds((y, x+1), rows, cols): # Check Right
            threats.append((y, x+1))
        if inBounds((y-1, x+1), rows, cols): # Check UpRight
            threats.append((y-1, x+1))

    elif Piece.name == "Rook":
        ytemp = y
        xtemp = x
        while (True): # Check Up
            if inBounds((ytemp-1, x), rows, cols): # It is in bounds
                if board[ytemp-1][x] == "Obstacle": # We've hit an obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp-1, x))
                    ytemp -= 1
            else: # Out of bounds
                break 
        ytemp = y # Reset
        while (True): # Check Left
            if inBounds((y, xtemp-1), rows, cols): # It is in bounds
                if board[y][xtemp-1] == "Obstacle": # We've hit an obstacle
                    break
                else: # No obstacle
                    threats.append((y, xtemp-1))
                    xtemp -= 1
            else: # Out of bounds
                break 
        xtemp = x # Reset
        while (True): # Check Down
            if inBounds((ytemp+1, x), rows, cols): # It is in bounds
                if board[ytemp+1][x] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp+1, x))
                    ytemp += 1
            else: # Out of bounds
                break 
        ytemp = y # Reset
        while (True): # Check Right
            if inBounds((y, xtemp+1), rows, cols): # It is in bounds
                if board[y][xtemp+1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((y, xtemp+1))
                    xtemp += 1
            else: # Out of bounds
                break 

    elif Piece.name == "Bishop":
        ytemp = y
        xtemp = x
        while (True): # Check UpLeft
            if inBounds((ytemp-1, xtemp-1), rows, cols): # It is in bounds
                if board[ytemp-1][xtemp-1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp-1, xtemp-1))
                    ytemp -= 1
                    xtemp -= 1
            else: # Out of bounds
                break 
        ytemp = y
        xtemp = x
        while (True): # Check DownLeft
            if inBounds((ytemp+1, xtemp-1), rows, cols): # It is in bounds
                if board[ytemp+1][xtemp-1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp+1, xtemp-1))
                    ytemp += 1
                    xtemp -= 1
            else: # Out of bounds
                break 
        ytemp = y
        xtemp = x
        while (True): # Check DownRight
            if inBounds((ytemp+1, xtemp+1), rows, cols): # It is in bounds
                if board[ytemp+1][xtemp+1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp+1, xtemp+1))
                    ytemp += 1
                    xtemp += 1
            else: # Out of bounds
                break 
        ytemp = y
        xtemp = x
        while (True): # Hit an obstacle
            if inBounds((ytemp-1, xtemp+1), rows, cols): # It is in bounds
                if board[ytemp-1][xtemp+1] == "Obstacle": # There is no obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp-1, xtemp+1))
                    ytemp -= 1
                    xtemp += 1
            else: # Out of bounds
                break 

    elif Piece.name == "Queen":
        ytemp = y
        xtemp = x
        while (True): # Check Up
            if inBounds((ytemp-1, x), rows, cols): # It is in bounds
                if board[ytemp-1][x] == "Obstacle": # We've hit an obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp-1, x))
                    ytemp -= 1
            else: # Out of bounds
                break 
        ytemp = y # Reset
        while (True): # Check Left
            if inBounds((y, xtemp-1), rows, cols): # It is in bounds
                if board[y][xtemp-1] == "Obstacle": # We've hit an obstacle
                    break
                else: # No obstacle
                    threats.append((y, xtemp-1))
                    xtemp -= 1
            else: # Out of bounds
                break 
        xtemp = x # Reset
        while (True): # Check Down
            if inBounds((ytemp+1, x), rows, cols): # It is in bounds
                if board[ytemp+1][x] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp+1, x))
                    ytemp += 1
            else: # Out of bounds
                break 
        ytemp = y # Reset
        while (True): # Check Right
            if inBounds((y, xtemp+1), rows, cols): # It is in bounds
                if board[y][xtemp+1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((y, xtemp+1))
                    xtemp += 1
            else: # Out of bounds
                break 
        xtemp = x
        while (True): # Check UpLeft
            if inBounds((ytemp-1, xtemp-1), rows, cols): # It is in bounds
                if board[ytemp-1][xtemp-1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp-1, xtemp-1))
                    ytemp -= 1
                    xtemp -= 1
            else: # Out of bounds
                break 
        ytemp = y
        xtemp = x
        while (True): # Check DownLeft
            if inBounds((ytemp+1, xtemp-1), rows, cols): # It is in bounds
                if board[ytemp+1][xtemp-1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp+1, xtemp-1))
                    ytemp += 1
                    xtemp -= 1
            else: # Out of bounds
                break 
        ytemp = y
        xtemp = x
        while (True): # Check DownRight
            if inBounds((ytemp+1, xtemp+1), rows, cols): # It is in bounds
                if board[ytemp+1][xtemp+1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp+1, xtemp+1))
                    ytemp += 1
                    xtemp += 1
            else: # Out of bounds
                break 
        ytemp = y
        xtemp = x
        while (True): # Hit an obstacle
            if inBounds((ytemp-1, xtemp+1), rows, cols): # It is in bounds
                if board[ytemp-1][xtemp+1] == "Obstacle": # There is no obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp-1, xtemp+1))
                    ytemp -= 1
                    xtemp += 1
            else: # Out of bounds
                break 
    
    elif Piece.name == "Knight":
        l_lim = 0
        r_lim = cols-1
        d_lim = rows-1
        u_lim = 0
        # R2U1 Square
        if ((x+2) <= r_lim and (y-1) >= u_lim):
            threats.append((y-1, x+2))
        # R1U2 Square
        if ((x+1) <= r_lim and (y-2) >= u_lim):
            threats.append((y-2, x+1))
        # L1U2 Square
        if ((x-1) >= l_lim and (y-2) >= u_lim):
            threats.append((y-2, x-1))
        # L2U1 Square
        if ((x-2) >= l_lim and (y-1) >= u_lim):
            threats.append((y-1, x-2))
        # L2D1 Square
        if ((x-2) >= l_lim and (y+1) <= d_lim):
            threats.append((y+1, x-2))
        # L1D2 Square
        if ((x-1) >= l_lim and (y+2) <= d_lim):
            threats.append((y+2, x-1))
        # R1D2 Square
        if ((x+1) <= r_lim and (y+2) <= d_lim):
            threats.append((y+2, x+1))
        # R2D1 Square
        if ((x+2) <= r_lim and (y+1) <= d_lim):
            threats.append((y+1, x+2))

    elif Piece.name == "Ferz":
        if inBounds((y-1, x-1), rows, cols): # Check UpLeft
            threats.append((y-1, x-1))
        if inBounds((y+1, x-1), rows, cols): # Check DownLeft
            threats.append((y+1, x-1))
        if inBounds((y+1, x+1), rows, cols): # Check DownRight
            threats.append((y+1, x+1))
        if inBounds((y-1, x+1), rows, cols): # Check UpRight
            threats.append((y-1, x+1))

    elif Piece.name == "Princess":
        ytemp = y
        xtemp = x
        while (True): # Check UpLeft
            if inBounds((ytemp-1, xtemp-1), rows, cols): # It is in bounds
                if board[ytemp-1][xtemp-1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp-1, xtemp-1))
                    ytemp -= 1
                    xtemp -= 1
            else: # Out of bounds
                break 
        ytemp = y
        xtemp = x
        while (True): # Check DownLeft
            if inBounds((ytemp+1, xtemp-1), rows, cols): # It is in bounds
                if board[ytemp+1][xtemp-1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp+1, xtemp-1))
                    ytemp += 1
                    xtemp -= 1
            else: # Out of bounds
                break 
        ytemp = y
        xtemp = x
        while (True): # Check DownRight
            if inBounds((ytemp+1, xtemp+1), rows, cols): # It is in bounds
                if board[ytemp+1][xtemp+1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp+1, xtemp+1))
                    ytemp += 1
                    xtemp += 1
            else: # Out of bounds
                break 
        ytemp = y
        xtemp = x
        while (True): # Hit an obstacle
            if inBounds((ytemp-1, xtemp+1), rows, cols): # It is in bounds
                if board[ytemp-1][xtemp+1] == "Obstacle": # There is no obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp-1, xtemp+1))
                    ytemp -= 1
                    xtemp += 1
            else: # Out of bounds
                break 
        l_lim = 0
        r_lim = cols-1
        d_lim = rows-1
        u_lim = 0
        # R2U1 Square
        if ((x+2) <= r_lim and (y-1) >= u_lim):
            threats.append((y-1, x+2))
        # R1U2 Square
        if ((x+1) <= r_lim and (y-2) >= u_lim):
            threats.append((y-2, x+1))
        # L1U2 Square
        if ((x-1) >= l_lim and (y-2) >= u_lim):
            threats.append((y-2, x-1))
        # L2U1 Square
        if ((x-2) >= l_lim and (y-1) >= u_lim):
            threats.append((y-1, x-2))
        # L2D1 Square
        if ((x-2) >= l_lim and (y+1) <= d_lim):
            threats.append((y+1, x-2))
        # L1D2 Square
        if ((x-1) >= l_lim and (y+2) <= d_lim):
            threats.append((y+2, x-1))
        # R1D2 Square
        if ((x+1) <= r_lim and (y+2) <= d_lim):
            threats.append((y+2, x+1))
        # R2D1 Square
        if ((x+2) <= r_lim and (y+1) <= d_lim):
            threats.append((y+1, x+2))

    elif Piece.name == "Empress":
        ytemp = y
        xtemp = x
        while (True): # Check Up
            if inBounds((ytemp-1, x), rows, cols): # It is in bounds
                if board[ytemp-1][x] == "Obstacle": # We've hit an obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp-1, x))
                    ytemp -= 1
            else: # Out of bounds
                break 
        ytemp = y # Reset
        while (True): # Check Left
            if inBounds((y, xtemp-1), rows, cols): # It is in bounds
                if board[y][xtemp-1] == "Obstacle": # We've hit an obstacle
                    break
                else: # No obstacle
                    threats.append((y, xtemp-1))
                    xtemp -= 1
            else: # Out of bounds
                break 
        xtemp = x # Reset
        while (True): # Check Down
            if inBounds((ytemp+1, x), rows, cols): # It is in bounds
                if board[ytemp+1][x] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((ytemp+1, x))
                    ytemp += 1
            else: # Out of bounds
                break 
        ytemp = y # Reset
        while (True): # Check Right
            if inBounds((y, xtemp+1), rows, cols): # It is in bounds
                if board[y][xtemp+1] == "Obstacle": # Hit obstacle
                    break
                else: # No obstacle
                    threats.append((y, xtemp+1))
                    xtemp += 1
            else: # Out of bounds
                break 
        l_lim = 0
        r_lim = cols-1
        d_lim = rows-1
        u_lim = 0
        # R2U1 Square
        if ((x+2) <= r_lim and (y-1) >= u_lim):
            threats.append((y-1, x+2))
        # R1U2 Square
        if ((x+1) <= r_lim and (y-2) >= u_lim):
            threats.append((y-2, x+1))
        # L1U2 Square
        if ((x-1) >= l_lim and (y-2) >= u_lim):
            threats.append((y-2, x-1))
        # L2U1 Square
        if ((x-2) >= l_lim and (y-1) >= u_lim):
            threats.append((y-1, x-2))
        # L2D1 Square
        if ((x-2) >= l_lim and (y+1) <= d_lim):
            threats.append((y+1, x-2))
        # L1D2 Square
        if ((x-1) >= l_lim and (y+2) <= d_lim):
            threats.append((y+2, x-1))
        # R1D2 Square
        if ((x+1) <= r_lim and (y+2) <= d_lim):
            threats.append((y+2, x+1))
        # R2D1 Square
        if ((x+2) <= r_lim and (y+1) <= d_lim):
            threats.append((y+1, x+2))

    return threats # List of threats

def inBounds(pos, rows, cols): # Checks that a position is in bounds
    x = pos[1]
    y = pos[0]
    # If cell is out of bounds
    if (x<0 or x>=cols or y<0 or y>=rows):
        return False
    else: 
        return True

def enoughPieces(board, rows, cols, k): # Checks if number of pieces left >= k
    num = 0
    for i in range(rows):
        for j in range(cols):
            if (board[i][j] != None) and (board[i][j] != "Obstacle"):
                num += 1
    if num > k-1:
        return True 
    else:
        return False

def goalTest(game, rows, cols): # Checks if a current board state is a Goal state
    for i in range(rows):
        for j in range(cols): # Iterate through entire board 
            if (game.board[i][j] == None) or (game.board[i][j] == "Obstacle"):
                continue # Skip if the square is empty, or if it contains an obstacle
            else: 
                piece = game.board[i][j] # Piece that is currently occupying the square
                threats = loadThreats(piece, game, rows, cols)
                # Now iterate through the threats
                for pos in threats:
                    if (type(game.board[pos[0]][pos[1]])==Piece): # If it threatens another piece
                        return False
    return True

# For a given piece and board state, return how many pieces our piece is threatening and how many pieces are threatening it
def heuristic(piece, game, rows, cols): 
    pos = piece.pos
    h = 0
    threats = loadThreats(piece, game, rows, cols) # List of positions our piece is threatening
    for i in range(rows):
        for j in range(cols): # Iterate through entire board 
            if (game.board[i][j] == None) or (game.board[i][j] == "Obstacle"):
                continue # Skip if the square is empty, or if it contains an obstacle
            else:
                enemy = game.board[i][j] # Enemy piece that is occupying the square
                if (i,j) in threats:
                    h += 1 # If this enemy is threatened by our piece
                enemy_threats = loadThreats(enemy, game, rows, cols) 
                if pos in enemy_threats:
                    h += 1 # If our piece is threatened by the enemy
    return h



#############################################################################
######## Implement Search Algorithm
#############################################################################
def search(rows, cols, grid, pieces, k):
    found = False # Bool flag to signal that global solution is found
    while (found == False):
        k = int(k) # Turns the str into an int
        game = Board(rows, cols, grid, pieces, k)
        curr = (random.randint(0, rows-1), random.randint(0, cols-1)) # Randomly generated
        while (True):
            x = curr[1]
            y = curr[0]
            game.board[y][x] = None # Remove the current piece
            if goalTest(game, rows, cols): # Found the global solution!
                found = True
                break
            if enoughPieces(game.board, rows, cols, k+1) == False: # Failure
                break 

            max = 0

            # Iterate through the entire board and remove maximum h value
            for i in range(rows):
                for j in range(cols):
                    if type(game.board[i][j]) != Piece:
                        continue #Ignore spaces and obstacles
                    else:
                        piece = game.board[i][j]
                        h = heuristic(piece, game, rows, cols)
                        if h > max: # Looking for the piece with the maximum heuristic
                            max = h 
                            curr = piece.pos

    # Results processing - Turns the final state into the return format
    result = {}
    for i in range(rows):
        for j in range(cols):
            if (game.board[i][j] == None) or (game.board[i][j] == "Obstacle"):
                continue # Skip if the square is empty, or if it contains an obstacle
            else:
                result[(allletters[j], i)] = game.board[i][j].name 
    return result 

#############################################################################
######## Parser function and helper functions
#############################################################################
### DO NOT EDIT/REMOVE THE FUNCTION BELOW###
def parse(testcase):
    handle = open(testcase, "r")

    get_par = lambda x: x.split(":")[1]
    rows = int(get_par(handle.readline()))
    cols = int(get_par(handle.readline()))
    grid = [[0 for j in range(cols)] for i in range(rows)]
    k = 0
    pieces = {}

    num_obstacles = int(get_par(handle.readline()))
    if num_obstacles > 0:
        for ch_coord in get_par(handle.readline()).split():  # Init obstacles
            r, c = from_chess_coord(ch_coord)
            grid[r][c] = -1
    else:
        handle.readline()
    
    k = handle.readline().split(":")[1].strip() # Read in value of k

    piece_nums = get_par(handle.readline()).split()
    num_pieces = 0
    for num in piece_nums:
        num_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        pieces[coords] = piece    

    return rows, cols, grid, pieces, k

def add_piece( comma_seperated):
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r,c), piece]

#Returns row and col index in integers respectively
def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# To return: Goal State which is a dictionary containing a mapping of the position of the grid to the chess piece type.
# Chess Pieces (String): King, Queen, Knight, Bishop, Rook (First letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Goal State to return example: {('a', 0) : Queen, ('d', 10) : Knight, ('g', 25) : Rook}
def run_local():
    testcase = sys.argv[1] #Do not remove. This is your input testfile.
    rows, cols, grid, pieces, k = parse(testcase)
    goalstate = search(rows, cols, grid, pieces, k)
    return goalstate #Format to be returned

# print(run_local())