import sys, math
from copy import deepcopy, copy

### IMPORTANT: Remove any print() functions or rename any print functions/variables/string when submitting on CodePost
### The autograder will not run if it detects any print function.

# ------- Global Variables -------
# In the format: (dy, dx) - No longer need empress/princess, they will be a combination of knight and rook/bishop
piece_steps = {"King": [(1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1), (0, 1)],
            "Rook": [(1, 0), (0, -1), (-1, 0), (0, 1)],
            "Bishop": [(1, 1), (1, -1), (-1, -1), (-1, 1)],
            "Queen": [(1, 0), (0, -1), (-1, 0), (0, 1), (1, 1), (1, -1), (-1, -1), (-1, 1)],
            "Knight": [(2, 1), (2, -1), (1, 2), (1, -2), (-2, 1), (-2, -1), (-1, 2), (-1, -2)],
            "Ferz": [(1, 1), (1, -1), (-1, -1), (-1, 1)]}
allletters = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
# As stated in the pdf:
initial_board = {('a', 1): ('Ferz', 'White'), ('a', 5): ('Ferz', 'Black'), ('g', 1): ('Ferz', 'White'), ('g', 5): ('Ferz', 'Black'), ('b', 1): ('Pawn', 'White'), ('b', 5): ('Pawn', 'Black'), ('c', 1): ('Pawn', 'White'), ('c', 5): ('Pawn', 'Black'), ('d', 1): ('Pawn', 'White'), ('d', 5): ('Pawn', 'Black'), ('e', 1): ('Pawn', 'White'), ('e', 5): ('Pawn', 'Black'), ('f', 1): ('Pawn', 'White'), ('f', 5): ('Pawn', 'Black'), ('a', 0): ('Knight', 'White'), ('a', 6): ('Knight', 'Black'), ('b', 0): ('Bishop', 'White'), ('b', 6): ('Bishop', 'Black'), ('c', 0): ('Queen', 'White'), ('c', 6): ('Queen', 'Black'), ('d', 0): ('King', 'White'), ('d', 6): ('King', 'Black'), ('e', 0): ('Princess', 'White'), ('e', 6): ('Princess', 'Black'), ('f', 0): ('Empress', 'White'), ('f', 6):  ('Empress', 'Black'), ('g', 0):  ('Rook', 'White'), ('g', 6):  ('Rook', 'Black')}

# Helper functions to aid in your implementation. Can edit/remove
#############################################################################
######## Piece class
#############################################################################
class Piece:
    def __init__(self, name, colour): # Both name and colours are strings
        self.name = name
        self.colour = colour
        self.value = 0 # Each piece will have a value assigned to it according to traditional chess rules

    def getValue(self): # Value of piece, following traditional chess values + an educated guess for fairy pieces
        if self.name == "King":
            return 999 # Maximum value
        elif self.name == "Queen":
            return 9
        elif self.name == "Empress":
            return 8
        elif self.name == "Princess":
            return 7
        elif self.name == "Rook":
            return 5
        elif self.name == "Bishop":
            return 3
        elif self.name == "Knight":
            return 3
        elif self.name == "Pawn":
            return 1
        elif self.name == "Ferz":
            return 2
    
#############################################################################
######## Board
#############################################################################
class Board:
    def __init__(self):
        self.board = [[None for y in range(7)] for x in range(7)] # 7x7 2D matrix [row, col]
        self.pieces = {} # Key: (row, col), Value: Piece

    def __copy__(self):
        temp = Board()
        temp.board = deepcopy(self.board)
        temp.pieces = deepcopy(self.pieces)
        return temp

    def addPiece(self, piece, row, col): # Add a piece to (row, col)
        self.board[row][col] = piece
        self.pieces[(row, col)] = piece   

    def loadMoves(self, row, col): # What are the possible moves for a piece at [row, col] in the board?
        piece = self.board[row][col]
        colour = piece.colour
        name = piece.name
        moves = [] # Coord, value of moving to that square

        # King or Knight or Ferz - non iterables
        if (name == "King") or (name == "Knight") or (name == "Ferz"):
            steps = piece_steps[name]
            for dy, dx in steps:
                new_y = row + dy
                new_x = col + dx
                if (0 <= new_y < 7) and (0 <= new_x < 7): #Check that its in bounds
                    enemy = self.board[new_y][new_x]
                    if enemy == None: # If there is no piece there
                        moves.append(((new_y, new_x), 0))
                    elif enemy.colour != colour: # If there is an enemy there
                        moves.append(((new_y, new_x), enemy.getValue()))
            return moves

        # Rook or Bishop or Queen - Iterables
        elif (name == "Rook") or (name == "Queen") or (name == "Bishop"):
            steps = piece_steps[name]
            for dy, dx in steps:
                n = 1 # Counter for iterating
                flag = False # bool flag to signal obstacles
                while (0 <= row+(n*dy) < 7) and (0 <= col+(n*dx) < 7) and (flag == False): # In bounds and obstacle not encountered yet
                    enemy = self.board[row+(n*dy)][col+(n*dx)]
                    if enemy != None: # If there is a piece there
                        flag = True 
                        if enemy.colour != colour: # If it is an enemy piece
                            moves.append(((row+(n*dy), col+(n*dx)), enemy.getValue()))
                    else:
                        moves.append(((row+(n*dy), col+(n*dx)), 0))
                    n += 1
            return moves

        # Princess - Combination of knight and bishop
        elif (name == "Princess"):
            k_steps = piece_steps["Knight"]
            b_steps = piece_steps["Bishop"]
            # Knight portion
            for dy, dx in k_steps:
                new_y = row + dy
                new_x = col + dx
                if (0 <= new_y < 7) and (0 <= new_x < 7): #Check that its in bounds
                    enemy = self.board[new_y][new_x]
                    if enemy == None: # If there is no piece there
                        moves.append(((new_y, new_x), 0))
                    elif enemy.colour != colour: # If there is an enemy there
                        moves.append(((new_y, new_x), enemy.getValue()))
            # Bishop portion
            for dy, dx in b_steps:
                n = 1 # Counter for iterating
                flag = False # bool flag to signal obstacles
                while (0 <= row+(n*dy) < 7) and (0 <= col+(n*dx) < 7) and (flag == False): # In bounds and obstacle not encountered yet
                    enemy = self.board[row+(n*dy)][col+(n*dx)]
                    if enemy != None: # If there is a piece there
                        flag = True 
                        if enemy.colour != colour: # If it is an enemy piece
                            moves.append(((row+(n*dy), col+(n*dx)), enemy.getValue()))
                    else:
                        moves.append(((row+(n*dy), col+(n*dx)), 0))
                    n += 1
            return moves 

        # Empress - Combination of knight and rook
        elif (name == "Empress"):
            k_steps = piece_steps["Knight"]
            r_steps = piece_steps["Rook"]
            # Knight portion
            for dy, dx in k_steps:
                new_y = row + dy
                new_x = col + dx
                if (0 <= new_y < 7) and (0 <= new_x < 7): #Check that its in bounds
                    enemy = self.board[new_y][new_x]
                    if enemy == None: # If there is no piece there
                        moves.append(((new_y, new_x), 0))
                    elif enemy.colour != colour: # If there is an enemy there
                        moves.append(((new_y, new_x), enemy.getValue()))
            # Rook portion
            for dy, dx in r_steps:
                n = 1 # Counter for iterating
                flag = False # bool flag to signal obstacles
                while (0 <= row+(n*dy) < 7) and (0 <= col+(n*dx) < 7) and (flag == False): # In bounds and obstacle not encountered yet
                    enemy = self.board[row+(n*dy)][col+(n*dx)]
                    if enemy != None: # If there is a piece there
                        flag = True 
                        if enemy.colour != colour: # If it is an enemy piece
                            moves.append(((row+(n*dy), col+(n*dx)), enemy.getValue()))
                    else:
                        moves.append(((row+(n*dy), col+(n*dx)), 0))
                    n += 1
            return moves 

        # Pawn 
        elif (name == "Pawn"):
            if colour == "Black": # If the pawn is black it moves down
                vert = -1 
            else: # If the pawn is white it moves up
                vert = +1
            new_y = row + vert
            if (0 <= new_y < 7):
                enemy = self.board[new_y][col]
                if enemy == None: # If there is no piece directly ahead
                    moves.append(((new_y, col), 0))
            if (col-1 >= 0) and (0 <= new_y < 7): # Checking ahead left
                enemy = self.board[new_y][col-1] 
                if enemy != None and enemy.colour != colour: # If there is an enemy there
                    moves.append(((new_y, col-1), enemy.getValue()))
            if (col+1 < 7) and (0 <= new_y < 7): # Checking ahead right
                enemy = self.board[new_y][col+1] 
                if enemy != None and enemy.colour != colour: # If there is an enemy there
                    moves.append(((new_y, col+1), enemy.getValue()))
            return moves 

    def movePiece(self, oldy, oldx, newy, newx): # Move piece on (oldy, oldx) to (newy, newx)
        if self.board[oldy][oldx] == None:
            return None # Just a foolproof check
        enemy = self.board[newy][newx]
        if enemy != None: # If there is an enemy piece there
            self.pieces.pop((newy, newx)) # Remove it from the dictionary
        piece = self.board[oldy][oldx]
        # Updating the board and the pieces dictionary 
        self.pieces[(newy, newx)] = piece
        self.board[newy][newx] = piece
        self.pieces.pop((oldy, oldx))
        self.board[oldy][oldx] = None

    def getHeuristic(self): # Determining value of a certain state of the game
        result = 0
        for pos, piece in self.pieces.items(): # Iterate through pieces
            if piece.colour == "White": # If piece is white we add
                result += piece.getValue()
            else: # If piece is black we subtract
                result -= piece.getValue()
        return result

    def boardLoader(self, dict): # Load a board which is a dictionary of type {('a', 1):("Ferz", "White")}
        for x_letter, y in dict.keys():
            x = ord(x_letter) - ord("a")
            name, colour = dict[(x_letter, y)]
            piece = Piece(name, colour)
            self.addPiece(piece, y, x)

#############################################################################
######## Gameboard
#############################################################################
class Gameboard:
    def __init__(self, board):
        self.board = board 
        self.value = 0
        self.heuristic = 0 
        self.depth = 0

    def __copy__(self):
        temp_board = copy(self.board)
        temp = Gameboard(temp_board)
        temp.value = self.value
        temp.heuristic = self.heuristic
        temp.depth = self.depth
        return temp

    def loadMoves(self, colour): # For a colour's turn, what possible moves can be made 
        moves = []
        for (row, col) in self.board.pieces.keys(): # Iterate through the positions with pieces
            if self.board.board[row][col].colour == colour: # If it is your piece
                for (newy, newx), val in self.board.loadMoves(row, col):
                    moves.append(((row, col), (newy, newx), val)) 
        return moves

#Implement your minimax with alpha-beta pruning algorithm here.
def ab(gameboard, turn, a, b): # gameboard is a state. turn is a string, who's turn is it? a and b are current a b values
    if gameboard.depth < 2: 
        if turn == "White": # If its white's turn 
            max = -math.inf
            for (oldy, oldx), (newy, newx), val in gameboard.loadMoves(turn):
                next = copy(gameboard)
                next.depth += 1
                next.heuristic += val
                next.board.movePiece(oldy, oldx, newy, newx)
                ab(next, "Black", a, b)
                if (next.value >= b) or (val == 999): # If king capture is possible
                    gameboard.value = next.value
                    return (oldy, oldx), (newy, newx)
                if (next.value >= max): # Update max value
                    max = next.value 
                    if gameboard.depth == 0: # Reach the root
                        move = ((oldy, oldx), (newy, newx))
                if (next.value > a): # Update alpha value
                    a = next.value 
            gameboard.value = max
            if gameboard.depth == 0:
                return move 
        else: # If it's black's turn 
            min = math.inf 
            for (oldy, oldx), (newy, newx), val in gameboard.loadMoves(turn):
                next = copy(gameboard)
                next.depth += 1
                next.heuristic += val
                next.board.movePiece(oldy, oldx, newy, newx)
                ab(next, "White", a, b) 
                if (next.value <= a):
                    gameboard.value = next.value
                    return 
                if (next.value < min): # Update min value
                    min = next.value 
                if (next.value < b): # Update b value
                    b = next.value
            gameboard.value = min 
        return 
    else:
        gameboard.value = gameboard.heuristic
        return             
   

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
    gameboard = {}
    
    enemy_piece_nums = get_par(handle.readline()).split()
    num_enemy_pieces = 0 # Read Enemy Pieces Positions
    for num in enemy_piece_nums:
        num_enemy_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_enemy_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        gameboard[coords] = (piece, "Black")    

    own_piece_nums = get_par(handle.readline()).split()
    num_own_pieces = 0 # Read Own Pieces Positions
    for num in own_piece_nums:
        num_own_pieces += int(num)

    handle.readline()  # Ignore header
    for i in range(num_own_pieces):
        line = handle.readline()[1:-2]
        coords, piece = add_piece(line)
        gameboard[coords] = (piece, "White")    

    return rows, cols, gameboard

def add_piece( comma_seperated) -> Piece:
    piece, ch_coord = comma_seperated.split(",")
    r, c = from_chess_coord(ch_coord)
    return [(r,c), piece]

def from_chess_coord( ch_coord):
    return (int(ch_coord[1:]), ord(ch_coord[0]) - 97)

# You may call this function if you need to set up the board
def setUpBoard():
    config = sys.argv[1]
    rows, cols, gameboard = parse(config)

### DO NOT EDIT/REMOVE THE FUNCTION HEADER BELOW###
# Chess Pieces: King, Queen, Knight, Bishop, Rook, Princess, Empress, Ferz, Pawn (First letter capitalized)
# Colours: White, Black (First Letter capitalized)
# Positions: Tuple. (column (String format), row (Int)). Example: ('a', 0)

# Parameters:
# gameboard: Dictionary of positions (Key) to the tuple of piece type and its colour (Value). This represents the current pieces left on the board.
# Key: position is a tuple with the x-axis in String format and the y-axis in integer format.
# Value: tuple of piece type and piece colour with both values being in String format. Note that the first letter for both type and colour are capitalized as well.
# gameboard example: {('a', 0) : ('Queen', 'White'), ('d', 10) : ('Knight', 'Black'), ('g', 25) : ('Rook', 'White')}
#
# Return value:
# move: A tuple containing the starting position of the piece being moved to the new ending position for the piece. x-axis in String format and y-axis in integer format.
# move example: (('a', 0), ('b', 3))

def studentAgent(gameboard): # Input is a dictionary 
    # You can code in here but you cannot remove this function, change its parameter or change the return type
    board = Board()
    board.boardLoader(gameboard)
    game = Gameboard(board)
    game.heuristic = game.board.getHeuristic()
    result = ab(game, "White", -math.inf, math.inf) # in the form ((oldy, oldx), (newy, newx))
    move = ((allletters[result[0][1]], result[0][0]), (allletters[result[1][1]], result[1][0]))
    return move #Format to be returned (('a', 0), ('b', 3))

# Execution statement
# print(studentAgent(initial_board))