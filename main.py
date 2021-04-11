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
    clickedPiece = None
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
        self.game.printTextBoard()
        self.printBoard = self.game.printTextBoard
        self.loop()

    def updateDisplay(self):
        ''' Updates the display with the latest blits.
        '''
        # Blit board
        self.screen.blit(self.game.board.image, self.game.board.rect)
        # Blit pieces
        for piece in Piece.register:
            self.screen.blit(piece.image, piece.rect)
        # Blit the clicked piece.
        if State.clickedPiece is not None: # If we have a piece in hand
            self.screen.blit(State.clickedPiece.image, State.clickedPiece.rect)

            
        # Post the updates to the display
        pygame.display.flip()

    def updateClickedPieceLocation(self):
        ''' If there is a clicked piece, keep it under the cursor.
        '''
        if State.clickedPiece is not None:
            mousePosition = pygame.mouse.get_pos()
            State.clickedPiece.rect.center = mousePosition

    def findClickedPiece(self, position):
        ''' Finds the piece under the cursor at the position given.
                -> Piece object of the chosen game piece.
        '''
        for piece in Piece.register:
            if piece.rect.collidepoint(position):
                return piece

    def findDropSquare(self, piece):
        ''' Find the square a piece is dropped on.
        '''
        centerOfPiece = piece.rect.center
        for square in State.game.board.grid.values():
            if square.rect.collidepoint(centerOfPiece):
                return square.address

    def placeClickedPiece(self, address):
        ''' Places the clicked piece into the center of the square at the given address.
        '''
        State.clickedPiece.place(address)

    def setClickedPiece(self, piece):
        ''' Sets the State.clickedPiece attribute to the clicked piece.
        '''
        State.clickedPiece = piece

    def mouseClick(self):
        ''' Checks if something interesting was clicked on, and does the thing needed.
        '''
        self.printBoard()
        clickPosition = pygame.mouse.get_pos()
        possibleChosenPiece = self.findClickedPiece(clickPosition)
        if possibleChosenPiece is not None:
            chosenPiece = possibleChosenPiece
            self.setClickedPiece(chosenPiece)

    def mouseRelease(self):
        ''' Does the actions required when the mouse button is released.
        '''
        self.printBoard()
        if State.clickedPiece is not None:
            newAddress = self.findDropSquare(State.clickedPiece)
            self.placeClickedPiece(newAddress)
            State.clickedPiece = None
            self.printBoard()

    def loop(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouseClick()
                if event.type == pygame.MOUSEBUTTONUP:
                    self.mouseRelease()
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.K_q:
                    sys.exit()
            self.updateClickedPieceLocation()
            self.updateDisplay()


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

    def printTextBoard(self):
        textBoard = []
        allSquares = [ f"{row}{col}"for col in range(1, 9) for row in "abcdefgh" ] # Handy list comprehention from IRC#python:disi
        header = '| - - - - - - - - '
        footer = '|\n| - - - - - - - - |'
        textBoard.append(header)
        for num, squareAddress in enumerate(allSquares):
            if num % 8 == 0:
                textBoard.append('|\n| ')
            occupant = self.board.grid[squareAddress].occupant
            if occupant is None:
                code = '.'
            elif issubclass(type(occupant), Piece):
                color = occupant.color
                if type(occupant) is Rook:
                    code = 'R' if color == 'white' else 'r'
                elif type(occupant) is Bishop:
                    code = 'B' if color == 'white' else 'b'
                elif type(occupant) is Knight:
                    code = 'N' if color == 'white' else 'n'
                elif type(occupant) is Queen:
                    code = 'Q' if color == 'white' else 'q'
                elif type(occupant) is King:
                    code = 'K' if color == 'white' else 'k'
                elif type(occupant) is Pawn:
                    code = 'P' if color == 'white' else 'p'
                elif type(occupant) is Piece:
                    code = 'X' if color == 'white' else 'x'
            else:
                return False
            textBoard.append(code)
            textBoard.append(' ')
        textBoard.append(footer)
        stringBoard = ''.join(textBoard)
        rowList = stringBoard.split('\n')
        board = '\n'.join(reversed(rowList))
        print(board)


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
                    self.grid[address].occupant = Rook('white', 'rook', address = address); continue
                if address[1] == '8':
                    self.grid[address].occupant = Rook('black', 'rook', address = address); continue
            # Add the knights
            if address[0] == 'b' or address[0] == 'g':
                if address[1] == '1':
                    self.grid[address].occupant = Piece('white', 'knight', address = address); continue
                if address[1] == '8':
                    self.grid[address].occupant = Piece('black', 'knight', address = address); continue
            # Add the bishops
            if address[0] == 'c' or address[0] == 'f':
                if address[1] == '1':
                    self.grid[address].occupant = Bishop('white', 'bishop', address = address); continue
                if address[1] == '8':
                    self.grid[address].occupant = Bishop('black', 'bishop', address = address); continue
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

    def removeOccupant(self, address):
        ''' Removes the occupant from the square at the address given.
        '''
        self.grid[address].removeOccupant()

    def addOccupant(self, address, occupant):
        ''' Adds the occupant to the square at the address given.
        '''
        self.grid[address].addOccupant(occupant)

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
        self.address = f"{column}{row}"
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

    def isEmpty(self):
        ''' Checks to see if this location is empty or not.
        '''
        if self.occupant is None:
            return True
        return False

    def removeOccupant(self):
        ''' Remove the occupant from this address.
        '''
        self.occupant = None

    def addOccupant(self, occupant):
        self.occupant = occupant

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
    
    def __init__(self, color, typeOfPiece, address=None, subtypeInst = None):
        ''' Set the type of piece, the color, and what image it will use.
        '''
        if subtypeInst is not None:
            self.register.append(subtypeInst) # Add's this new instance to the register kept in the class-atribute, "register". 
        else:
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
        if hasattr(self, 'address'):
            State.game.board.removeOccupant(self.address)
        self.address = address
        self.column = address[0]
        self.row = address[1]
        addressCenter = State.game.board.grid[address].rect.center
        self.rect.center = addressCenter
        State.game.board.addOccupant(address, self)

    def moveTo(self, newCenter):
        ''' Moves the piece (rect of the piece) to the new center newCenter.
        '''
        self.rect.center = newCenter

    def amIHere(self, address):
        ''' Check if the given address is the same as the current address.
        '''
        if self.address == address:
            return True
        return False

    def isSquareLegal(self, address):
        ''' Uses several sub-methods to anser the question of legit-ness by checking:
                * Is it a move that this peice could ever do (on an empty board).
                * Is this move obstructed?
        '''
        if self.isSquareOnPath(address) and self.isSquareReachable(address):
            return True
        return False

    def __str__(self):
        ''' Returns a string describing the object.
        '''
        return f"A {self.typeOfPiece} on {self.address}."


class Rook(Piece):
    ''' A subclass of Piece, that holds the restrictions related to a rook.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, subtypeInst = self, **kwargs)

    def place(self, address, *args, **kwargs):
        ''' Does the checking for validity of the requested placement, then runs the super().place.
        '''
        if hasattr(self, 'address'):
            if self.isSquareLegal(address):
                super().place(address, *args, **kwargs) # It's all good. Go to the square at the new address.
            else:
                super().place(self.address, *args, **kwargs) # Go back to where you started, because the move is illegal.
        else:
            super().place(address, *args, **kwargs) # It is the first time the piece is on the board, so it is where it is; there is nothing to check.


    def isSquareOnPath(self, address):
        ''' Checks if address of target square is a square that lies on a primitive movement path of a rook.
        '''
        if address[0] == self.address[0] or address[1] == self.address[1]:
            return True
        return False

    def isSquareReachable(self, address):
        ''' Check to see if the squares the piece must travel through are clear.
        '''
        columns = ['x', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        if address[0] == self.address[0]: # It is a vertical movement.
            currentRow = int(self.row)
            targetRow = int(address[1])
            if currentRow < targetRow:
                rowsToCheck = range(currentRow + 1, targetRow)
            else:
                rowsToCheck = range(targetRow + 1, currentRow)
            for row in rowsToCheck:
                if State.game.board.grid[f"{self.column}{row}"].isEmpty():
                    continue
                return False # Path is blocked.
        if address[1] == self.address[1]: # It is a horizontal movement. We need to check columns
            targetColumn = address[0]
            currentColumnNumber = columns.index(self.column)
            targetColumnNumber = columns.index(targetColumn)
            if currentColumnNumber < targetColumnNumber:
                columnsToCheck = range(currentColumnNumber + 1, targetColumnNumber)
            else:
                columnsToCheck = range(targetColumnNumber + 1, currentColumnNumber)
            for columnNumber in columnsToCheck:
                column = columns[columnNumber]
                if State.game.board.grid[f"{column}{self.row}"].isEmpty():
                    continue
                return False # Path is blocked.


class Bishop(Piece):
    ''' A subclass of Piece, that holds the restrictions related to a rook.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, subtypeInst = self, **kwargs)

    def place(self, address, *args, **kwargs):
        ''' Does the checking for validity of the requested placement, then runs the super().place.
        '''
        if hasattr(self, 'address'):
            if self.isSquareLegal(address):
                super().place(address, *args, **kwargs) # It's all good. Go to the square at the new address.
            else:
                super().place(self.address, *args, **kwargs) # Go back to where you started, because the move is illegal.
        else:
            super().place(address, *args, **kwargs) # It is the first time the piece is on the board, so it is where it is; there is nothing to check.

    def isSquareOnPath(self, address):
        ''' Returns bool dependant on whether address is on movement path of a bishop.
        '''
        allSquares = [f"{col}{row}" for row in range(1, 9) for col in "abcdefgh" ] # Handy list comprehention from IRC#python:disi
        delta = (allSquares.index(address) - allSquares.index(self.address))
        if delta % 7 == 0 or delta % 9 == 0:
            return True
        return False

    def isSquareReachable(self, address):
        ''' Checks the squares that could block the movement for existance of a piece on the square. 
                It does this by serializing the board, and using simple arithmatic to find the next square on the diagonal.
        '''
        allSquares = [f"{column}{row}" for row in range(1, 9) for column in "abcdefgh"] # Handy list comprehention from IRC#python:disi
        current = allSquares.index(self.address)
        target =  allSquares.index(address)
        delta = target - current
        sign = int(delta / abs(delta)) # Handy function from boejiden on #math on Freenode.

        if delta % 9 == 0: # Positive slope diagonal
            delta = 9 * sign
        elif delta % 7 == 0: # Negative slope diagonal
            delta = 7 * sign
        else:
            return False

        def test(current, target, delta):
            if State.game.board.grid[allSquares[current]].occupant is None:
                if current != target:
                    return test(current + delta, target, delta)
                else:
                    return True
            else:
                return False
        return test(current + delta, target, delta) # Check the next square, since we are still "on" the "current" square.


class Knight(Piece):
    ''' A subclass of Piece, that holds the restrictions related to a rook.
    '''
    def __init__(self, *args, **kwargs):
        super().__init__(*args, subtypeInst = self, **kwargs)

    def place(self, address, *args, **kwargs):
        ''' Does the checking for validity of the requested placement, then runs the super().place.
        '''
        if hasattr(self, 'address'):
            if self.isSquareLegal(address):
                super().place(address, *args, **kwargs) # It's all good. Go to the square at the new address.
            else:
                super().place(self.address, *args, **kwargs) # Go back to where you started, because the move is illegal.
        else:
            super().place(address, *args, **kwargs) # It is the first time the piece is on the board, so it is where it is; there is nothing to check.

    def isSquareOnPath(self, address):
        ''' Returns bool dependant on whether address is on movement path of a bishop.
        '''
        allSquares = [f"{row}{col}" for row in "abcdefgh" for col in range(1, 9)] # Handy list comprehention from IRC#python:disi
        delta = (allSquares.index(address) - allSquares.index(self.address))
        if delta % 7 == 0 or delta % 9 == 0:
            return True
        return False

    def isSquareReachable(self, address):
        ''' Checks the squares that could block the movement for existance of a piece on the square. 
                It does this by serializing the board, and using simple arithmatic to find the next square on the diagonal.
        '''
        allSquares = [f"{column}{row}" for row in range(1, 9) for column in "abcdefgh"] # Handy list comprehention from IRC#python:disi
        current = allSquares.index(self.address)
        target =  allSquares.index(address)
        delta = target - current
        sign = delta ** 0 # To the zero power, maintains the sign of the number. Cool!

        if delta % 9 == 0: # Positive slope diagonal
            delta = 9 * sign
        elif delta % 7 == 0: # Negative slope diagonal
            delta = 7 * sign
        else:
            return False

        def test(current, target, delta):
            if current != target:
                if State.game.board.grid[allSquares[current]].occupant is None:
                    test(current + delta, target, delta)
                    return True
                else:
                    return False
            else:
                return False
        return test(current + delta, target, delta) # Check the next square, since we are still "on" the "current" square.


class Queen(Piece):
    pass

class King(Piece):
    pass

class Pawn(Piece):
    pass

def main():
    game = ChessGame('john', 'paul')
    engine = Engine(game)



if __name__ == '__main__':
    main()
