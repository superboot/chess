
    def setupPieces(self):
        ''' Sets up the peices on the board in the start position.
        '''
        layout = [{'color':'white', 'rank': 'rook', 'square': 'a1'},
                {'color': 'white', 'rank': 'knight', 'square': 'b1'},
                {'color': 'white', 'rank': 'bishop', 'square': 'c1'},
                {'color': 'white', 'rank': 'queen', 'square': 'd1'},
                {'color': 'white', 'rank': 'king', 'square': 'e1'},
                {'color': 'white', 'rank': 'bishop', 'square': 'f1'},
                {'color': 'white', 'rank': 'knight', 'square': 'g1'},
                {'color': 'white', 'rank': 'rook', 'square': 'h1'},
                {'color': 'white', 'rank': 'pawn', 'square': 'a2'},
                {'color': 'white', 'rank': 'pawn', 'square': 'b2'},
                {'color': 'white', 'rank': 'pawn', 'square': 'c2'},
                {'color': 'white', 'rank': 'pawn', 'square': 'd2'},
                {'color': 'white', 'rank': 'pawn', 'square': 'e2'},
                {'color': 'white', 'rank': 'pawn', 'square': 'f2'},
                {'color': 'white', 'rank': 'pawn', 'square': 'g2'},
                {'color': 'white', 'rank': 'pawn', 'square': 'h2'},
                {'color': 'black', 'rank': 'rook', 'square': 'a8'},
                {'color': 'black', 'rank': 'knight', 'square': 'b8'},
                {'color': 'black', 'rank': 'bishop', 'square': 'c8'},
                {'color': 'black', 'rank': 'queen', 'square': 'd8'},
                {'color': 'black', 'rank': 'king', 'square': 'f8'},
                {'color': 'black', 'rank': 'bishop', 'square': 'g8'},
                {'color': 'black', 'rank': 'knight', 'square': 'h8'},
                {'color': 'black', 'rank': 'rook', 'square': 'a7'},
                {'color': 'black', 'rank': 'pawn', 'square': 'b7'},
                {'color': 'black', 'rank': 'pawn', 'square': 'c7'},
                {'color': 'black', 'rank': 'pawn', 'square': 'd7'},
                {'color': 'black', 'rank': 'pawn', 'square': 'e7'},
                {'color': 'black', 'rank': 'pawn', 'square': 'f7'},
                {'color': 'black', 'rank': 'pawn', 'square': 'g7'},
                {'color': 'black', 'rank': 'pawn', 'square': 'h7'}]
        for spot in layout:
            setattr(self, spot['square'], Piece()

    def createBoxOfPieces(self):
        ''' Creates the box of pieces.
        '''
        self.box = set()
        for color in 'white', 'black':
            for piece in ('knight', 'bishop', 'rook', 'queen', 'king'):
                self.box.add(Piece(color, piece))
            for pawnNumber in range(8):
                self.box.add(Piece(color, 'pawn'))

