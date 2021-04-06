'''
This module is a simple chess program as a starting project for working with pygame.
'''

import pygame
import pygame.locals as pl
import sys
import time

class State():
    ''' This is the class that will hold refferences to all common state as class atributes.
            Why? Because FOOP.
            It will recieve attributes dynamicly as things are changed.
    '''
    pass


class Engine(State):
    ''' This class runs pygame at large.
    '''

    def __init__(self, game, screenWidth = 888, screenHeight = 888):
        State.engine = self
        pygame.init()
        self.game = game
        self.screenWidth = screenWidth
        self.screenHeight = screenHeight
        self.screenSize = (self.screenWidth, self.screenHeight)
        self.screen = pygame.display.set_mode(self.screenSize)
        self.updateDisplay()
        #self.loop()

    def updateDisplay(self):
        ''' Updates the display with the latest blits.
        '''
        # Blit board
        self.screen.blit(self.game.board.image, self.game.board.rect)
        # Blit pieces
        for location in self.game.board.grid.values():
            if location.occupant is not None:
                self.screen.blit(location.occupant.image, location.occupant.rect)
            
        # Post the updates to the display
        pygame.display.flip()


    def loop(self):
        # Watch for a quit action
        while 1:
            for event in pygame.event.get():
                if event .type == pygame.QUIT: sys.exit()


class ChessGame(State):
    ''' A game that holds the move history, time clocks, etc.
    '''
    register = [] # The list of all instances.
    def __init__(self, p1 = '', p2 = ''):
        '''Setup the clocks and the equipment for a new game. 
        '''
        State.game = self
        self.register.append(self) # Add's this new instance to the register kept in the class-atribute, "register". 
        board = Board()
        p1 = Player(name=p1)
        p2 = Player(name=p2)
        clock1 = Clock('60:00')
        clock2 = Clock('60:00')
        

class Clock(State):
    ''' A time keeping device.
    '''

    def __init__(self, timeLimmit):
        if type(timeLimmit) not in (int, float):
            timeLimmit = self.convertStrTimeToSeconds(timeLimmit)
        self.timeLimmit = timeLimmit 

    def convertStrTimeToSeconds(self, timeString):
        ''' Converts a colon-delimited time string hours:minutes:seconds.mentissa to float.

        Possible input formats:
            23:59:59.99 -> hour:minute:second.metissa
            59:59.99 -> minute:seconds.mentissa
            59.99 or 59 -> seconds.metissa or seconds
        -> float
        '''
        rv = 0
        if ':' in timeString:
            timeElements = timeString.split(':')
            while len(timeElements) > 0:
                if len(timeElements) == 3:
                    rv += int(timeElements[0]) * 3600 # convert string hours to seconds.
                    timeElements = timeElements[1:]
                    continue
                if len(timeElements) == 2:
                    rv += int(timeElements[0]) * 60 # convert string minutes to seconds.
                    timeElements = timeElements[1:]
                    continue
                if len(timeElements) == 1:
                    rv += int(timeElements[0]) # Add the seconds.
                    break
        else: # There are no delimiters.
            rv = float(timeString)
        return rv

    def start(self):
        '''Starts the clock.
        '''
        self.startTime = time.time()
    
    @property
    def rawTimeElapsed(self):
        ''' Returns the time elapsed in seconds and fractions of a second.
        -> float
        '''
        now = time.time()
        delta = now - self.startTime
        return delta

    @property
    def rawTimeRemaining(self):
        ''' Returns the time remaining in seconds.
        -> float
        '''
        return self.timeLimmit - self.rawTimeElapsed

    @property
    def timeRemaining(self):
        ''' Returns a string with time broken into hours minutes seconds.
        -> str
        '''
        hours, remainder = divmod(self.rawTimeRemaining, 60)
        hours = f"{str(int(hours))}:" if hours > 0 else ''
        minutes, remainder = divmod(remainder, 60)
        minutes = f"{str(int(minutes))}:" if minutes > 0 else ''
        seconds, mentissa = str(remainder).split('.') 
        seconds = str(int(seconds)) if int(seconds) > 0 else ''
        mentissa = mentissa[:3] # Get the first 3 decimal digits and chop the rest.
        seconds = f"{seconds}.{mentissa}"
        return f"{hours}{minutes}{seconds}"


class Player(State):
    ''' A player with a game history and such.
    '''
    def __init__(self, name, rank=400):
        self.name = name
        self.rank = rank


class Board(State):
    ''' A chessboard that holds peices.
    '''

    def __init__(self, orientation = 'white'):
        '''Loads the board image, and creates the pygame objects for it.
        '''
        State.game.board = self # Give a refferance to all sibling classes to this instance.
        self.image = self.loadImage()
        self.rect = self.image.get_rect()
        self.orientation = orientation
        self.createGrid()
        self.reset()
        self.whiteCaptures = []
        self.blackCaptures = []


    def flipBoard(self):
        '''Flips the board to view it from the other side.
        '''
        pass

    def reset(self):
        ''' Resets the pieces to the starting position.
        '''
        for address in self.grid.keys():
            # Add the pawns
            if address[1] == '2': # If we are looking at a row two cell.
                self.grid[address].occupant = Piece('white', 'pawn', address = address); continue
            if address[1] == '7':
                self.grid[address].occupant = Piece('black', 'pawn', address = address); continue
            # Add the rooks
            if address[0] == 'a' or address[0] == 'h':
                if address[1] == '1':
                    self.grid[address].occupant = Piece('white', 'rook', address = address); continue
                if address[1] == '8':
                    self.grid[address].occupant = Piece('black', 'rook', address = address); continue
            # Add the knights
            if address[0] == 'b' or address[0] == 'g':
                if address[1] == '1':
                    self.grid[address].occupant = Piece('white', 'knight', address = address); continue
                if address[1] == '8':
                    self.grid[address].occupant = Piece('black', 'knight', address = address); continue
            # Add the bishops
            if address[0] == 'c' or address[0] == 'f':
                if address[1] == '1':
                    self.grid[address].occupant = Piece('white', 'bishop', address = address); continue
                if address[1] == '8':
                    self.grid[address].occupant = Piece('black', 'bishop', address = address); continue
            # Add the queens
            if address[0] == 'd':
                if address[1] == '1':
                    self.grid[address].occupant = Piece('white', 'queen', address = address); continue
                if address[1] == '8':
                    self.grid[address].occupant = Piece('black', 'queen', address = address); continue
            # Add the kings
            if address[0] == 'e':
                if address[1] == '1':
                    self.grid[address].occupant = Piece('white', 'king', address = address); continue
                if address[1] == '8':
                    self.grid[address].occupant = Piece('black', 'king', address = address); continue
            else:
                # Clear all other sqares.
                self.grid[address].occupant = None

    def createGrid(self):
        ''' Create the grid of squares that make up the board, setting them as attributes of this instance.
        '''
        self.grid = {}
        squareWidth = State.game.board.rect.width / 8
        squareHeight = State.game.board.rect.height / 8
        columns = 'abcdefgh'
        for column in columns:
            xOffset = squareWidth * columns.find(column) # Calculate the pixle position of this column.
            for row in (1,2,3,4,5,6,7,8):
                yOffset = squareHeight * (8 - row) # Calculate the pixle position of this row.
                rect = pygame.Rect(xOffset, yOffset, squareWidth, squareHeight)
                loc = Location(column, row, rect)
                self.grid[f"{column}{row}"] = loc
                setattr(self, f"{column}{row}", loc)

    def loadImage(self):
        '''Loads an image for the piece based on the type of piece it is. Right now it uses PyGame.

        :returns: A pygame.image object.
        '''
        rv = pygame.image.load("chessboard-888x888.gif") # load the image
        return rv

    @property
    def width(self):
        rv = self.rect.width
        return rv

    @property
    def height(self):
        rv = self.rect.height
        return rv


class Location(State):
    ''' A square on the chess board.
    '''
    def __init__(self, column, row, rect):
        ''' Setup the properties of the location.
        '''
        self.row = row
        self.column = column
        self.rect = rect
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
        return f"Address: {column}{row}\nOccupant: {self.occupant}"

    def __repr__(self):
        ''' Returns the representation of the object.
        '''
        return str(self)


class Piece(State):
    ''' A chess piece.
    '''
    register = [] # The register of instances of this class.
    
    def __init__(self, color, typeOfPiece, address=None):
        ''' Set the type of piece, the color, and what image it will use.
        '''
        self.register.append(self) # Add's this new instance to the register kept in the class-atribute, "register". 
        self.typeOfPiece = typeOfPiece
        self.color = color
        self.image = self.loadImage()
        self.rect = self.image.get_rect() # A call to a pygame method of the pygame.image object.
        if address is not None:
            self.place(address)

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

    def place(self, address):
        ''' Places piece on the square given by address eg. E4.
        '''
        self.address = address
        addressCenter = State.game.board.grid[address].rect.center
        newCenter = (int(addressCenter[0] - (self.width / 2)), int(addressCenter[1] - (self.height / 2)))
        self.rect.move_ip(*newCenter)

    def __str__(self):
        ''' Returns a string describing the object.
        '''
        return f"A {self.typeOfPiece} on {self.address}."




def main():
    game = ChessGame('john', 'paul')
    engine = Engine(game)



if __name__ == '__main__':
    main()
