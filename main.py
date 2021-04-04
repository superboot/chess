'''
This module is a simple chess program as a starting project for working with pygame.
'''

import pygame
import pygame.locals as pl
import sys
from time import sleep


class ChessGame():
    '''
    A game that holds the move history, time clocks, etc.
    '''
    pass


class Board():
    '''
    A chessboard that holds peices.
    '''
    pass


class Piece():
    '''
    A chess piece.
    '''
    
    def __init__(self, color, typeOfPiece):
        ''' Set the type of piece, the color, and what image it will use.
        '''
        self.typeOfPiece = typeOfPiece
        self.color = color
        self.image = self.loadImage(image)
        self.rect = self.image.get_rect() # A call to a pygame method of the pygame.image object.

    def loadImage(self):
        '''Loads an image for the piece based on the type of piece it is. Right now it uses PyGame.

        :returns: A pygame.image object.
        '''
        # Set the color code.
        if self.color == 'white':
            colorCode = 'w'
        elif self.color == 'black':
            colorCode = 'b'

        rv = pygame.image.load(f"{colorCode}-{self.typeOfPiece}.png")} # load the image
        return rv







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
