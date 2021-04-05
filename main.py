'''
This module is a simple chess program as a starting project for working with pygame.
'''

import pygame
import pygame.locals as pl
import sys
import time



class ChessGame():
    ''' A game that holds the move history, time clocks, etc.
    '''
    def __init__(self, p1 = '', p2 = ''):
        '''Setup the clocks and the equipment for a new game. 
        '''
        board = Board()
        p1 = Player(name=p1)
        p2 = Player(name=p2)
        clock1 = Clock()
        clock2 = Clock()
        

class Clock():
    ''' A time keeping device.
    '''

    def __init__(self, length):
        self.length = length

    def start(self):
        '''Starts the clock.
        '''
        pass
        self.startTime = time.time()

    def timeLeft(self):
        ''' Returns a string representation of the time remaining.


class Player():
    ''' A player with a game history and such.
    '''
    pass


class Board():
    ''' A chessboard that holds peices.
    '''

    def __init__(self, orientation = 'white'):
        '''Loads the board image, and creates the pygame objects for it.
        '''
        self.image = self.loadImage(image)
        self.rect = self.image.get_rect()
        self.orientation = orientation
        self.createBoxOfPieces()
        self.createGrid()

    def flipBoard(self):
        '''Flips the board to view it from the other side.
        '''
        pass

    def reset(self):
        ''' Resets the pieces to the starting position.
        '''
        pass

    def createBoxOfPieces(self):
        ''' Creates the box of pieces.
        '''
        self.box = set()
        for color in 'white', 'black':
            for piece in ('knight', 'bishop', 'rook', 'queen', 'king'):
                self.box.add(Piece(color, piece))
            for pawnNumber in range(8):
                self.box.add(Piece(color, 'pawn'))

    def createGrid(self):
        ''' Create the grid of squares that make up the board, setting them as attributes of this instance.
        '''
        self.grid = []
        for column in 'abcdefgh':
            for row in (1,2,3,4,5,6,7,8):
                loc = Location(column, row)
                self.grid.append(loc)
                setattr(self, f"{column}{row}", loc)


class Location():
    ''' A square on the chess board.
    '''
    def __init__(self, column, row):
        ''' Setup the properties of the location.
        '''
        self.row = row
        self.column = column
        self.color = self.calculateColor()
        self.occupant = None

    def calculateColor(self):
        ''' Calculates the color of the square.
        '''
        columns = ['x', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        if self.row % 2 == 1 and columns.index(self.column) % 2 == 1:
            return 'black'
        else:
            return 'white'

    def __str__(self):
        ''' Returns the string of the address.
        '''
        column = self.column.upper()
        row = self.row
        return f"{column}{row}"

class Piece():
    ''' A chess piece.
    '''
    
    def __init__(self, color, typeOfPiece):
        ''' Set the type of piece, the color, and what image it will use.
        '''
        self.typeOfPiece = typeOfPiece
        self.color = color
        self.image = self.loadImage(image)
        self.rect = self.image.get_rect() # A call to a pygame method of the pygame.image object.
        self.location = None # I think this needs to be a class Location, which are squares on the chess board.

    @property
    def width(self):
        ''' Retrieves the width of the rect which is the width of the piece.
        '''
        return self.rect.width
        
    @property
    def height(self):
        ''' Retrieves the height of the rect which is the height of the piece.
        '''
        return self.rect.height

    def loadImage(self):
        '''Loads an image for the piece based on the type of piece it is. Right now it uses PyGame.

        :returns: A pygame.image object.
        '''
        # Set the color code.
        if self.color == 'white':
            colorCode = 'w'
        elif self.color == 'black':
            colorCode = 'b'

        rv = pygame.image.load(f"{colorCode}-{self.typeOfPiece}.png") # load the image
        return rv




#########################################################################################
# FUNCTIONAL STYLE 
#########################################################################################



def createBoxOfPieces():
    '''
    Creates a nested dictionary holding the 32 chess pieces, both images (loaded once each) and rects for each descrete piece.

    Returns the dictionary.
    '''
    boxOfPieces = {'w': {}, 'b': {}}
    for color in 'w', 'b':
        for piece in ('pawn', 'knight', 'bishop', 'rook', 'queen', 'king'):
            boxOfPieces[color][piece] = {'image': pygame.image.load(f"{color}-{piece}.png")} # load the image
            boxOfPieces[color][piece]['rects'] = [boxOfPieces[color][piece]['image'].get_rect()] # get a rect for the image just loaded.
        for pawnNumber in range(8):
            boxOfPieces[color]['pawn']['rects'].append( boxOfPieces[color]['pawn']['image'].get_rect() )
    return boxOfPieces

def placePawns(boxOfPieces, color):
    '''
    Places the white pawns on the bottom of the board for the start of a game.
    '''
    screenHeight = 888
    squareWidth = 111
    squareHeight = 111
    pawnWidth = boxOfPieces[color]['pawn']['rects'][0].width 
    pawnHeight = boxOfPieces[color]['pawn']['rects'][0].height
    topOfPawnRow = screenHeight - pawnHeight - squareHeight
    startingX = squareWidth / 2 - pawnWidth / 2
    for pawnNumber in range(8):
        boxOfPieces[color]['pawn']['rects'][pawnNumber].update(startingX + squareWidth * pawnNumber + 1, topOfPawnRow, pawnWidth, pawnHeight)

def placeKnights(boxOfPieces, color):
    '''
    Places the knights of the color <color> in their starting positions for the game.
    '''
    pass

def placeBishops(boxOfPieces, color):
    '''
    Places the Bishops of the color <color> in their starting positions for the game.
    '''
    pass

def placeRooks(boxOfPieces, color):
    '''
    Places the Rooks of the color <color> in their starting positions for the game.
    '''
    pass

def placeQueen(boxOfPieces, color):
    '''
    Places the Queen of the color <color> in their starting positions for the game.
    '''
    pass

def placeKing(boxOfPieces, color):
    '''
    Places the King of the color <color> in their starting positions for the game.
    '''
    pass

def placePieces(boxOfPieces):
    '''
    Manipulates the box of pieces in place, arranging the rects of the pieces across the board.
    '''
    for color in ('w', 'b'):
        placePawns(boxOfPieces, color)
        placeKnights(boxOfPieces, color)
        placeBishops(boxOfPieces, color)
        placeRooks(boxOfPieces, color)
        placeQueen(boxOfPieces, color)
        placeKing(boxOfPieces, color)

def blitThePieces(screen, boxOfPieces):
    '''
    Blits all the rects of the pieces in the box to the screen.
    '''
    for color in boxOfPieces.keys():
        for piece in boxOfPieces[color].keys():
            for rect in boxOfPieces[color][piece]['rects']:
                screen.blit(boxOfPieces[color][piece]['image'], rect)
                
def blitTheBoard(screen, board):
    '''
    Blits the board image onto the screen.
    '''
    screen.blit(board, board.get_rect())

        
def main():
    pygame.init()

    screenSize = screenWidth, screenHeight = 888, 888
    black = 0,0,0

    screen = pygame.display.set_mode(screenSize)

    board = pygame.image.load("chessboard-888x888.gif")

    boxOfPieces = createBoxOfPieces()

    placePieces(boxOfPieces) # in place manipulation

    blitTheBoard(screen, board)
    blitThePieces(screen, boxOfPieces)
    
    pygame.display.flip()

    # Watch for a quit action.
    while 1:
        for event in pygame.event.get():
            if event .type == pygame.QUIT: sys.exit()


if __name__ == '__main__':
    main()
