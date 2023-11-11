"""
File:    board_square.py
Author:  Matthew Makila
Date:    11/4/2020
Section: 44
E-mail:  mmakila1@umbc.edu
Description:
  This code takes an objects from UrPiece and BoardSquare
  and tests whether the UrPiece instance can move to particular board squares (bs_n's)
  through the can_move method. The UrPiece object can access the attributes of the BoardSquare
  class to determine whether a move is plausible or not.

  Rules 1-5:
  1)    If you are on the board, and you can move to the next position num_moves times,
        then you can move, if the position is unoccupied or occupied by an opponent's piece (except rule 5).
  2)    If you are off the board, and you can move onto the board at the white starting position,
        and you can move num_moves - 1 additional times (moving onto the board counts as a move), then you can move.
        You can move there as long as it's unoccupied or occupied by an opponent's piece (except rule 5).
  3)    If you are on or off the board, and you would land on your own piece by moving, then you cannot move.
  4)    If you can move to the end position and have one move left, then you can move
        (and you would then leave the board, that piece would have completed its course.)
  5)    If you try to move onto a piece of opposing color, but that position is on a rosette,
        then you cannot move there.

  Technically 4/5 tests work for this ... but I am still confused
  and have no idea what to do with exit
"""
WHITE = 'White'
BLACK = 'Black'

"""

    VISION: basically as players move, check:
    
    do we want a dict to tract every player's pieces, their positions, whether or a rosette or not, etc ?
    
    if piece.can_move:
        display possible move options and let them select one
        choice = input("choose piece to move")  # from the options given, of course
        
        use the method to move the piece through the board they chose and redraw and reroll again. 

"""


class UrPiece:
    def __init__(self, color, symbol):
        self.color = color
        self.start = None
        self.position = None
        # when piece done moving set True
        self.complete = False
        self.symbol = symbol

    def set_start(self, begin):
        self.start = begin

    def can_move(self, num_moves):
        # if you roll 0 on die, can't move
        if num_moves == 0:
            return False
        # if you are starting and try to move a piece on the board, you only have num_moves - 1
        piece_pos = self.position
        if self.start:
            num_moves -= 1
            piece_pos = self.start
        if piece_pos:
            # keep checking if it can move for the num_moves given
            for i in range(num_moves):
                if piece_pos.exit and (num_moves - i) > 2:
                    return False
                elif piece_pos.exit and (num_moves - i) == 1: # (1)
                    return True
                # This keeps updating the piece's position (based on their color: i.e., updating to next_color)
                if self.color == WHITE:
                    piece_pos = piece_pos.next_white
                elif self.color == BLACK:
                    piece_pos = piece_pos.next_black
                # check if the next piece_pos of the piece is off the board and moves is exactly one or
                # more as it iterates through the total num of moves.
                if not piece_pos and (num_moves - i) > 1:
                    return False
                elif not piece_pos and (num_moves - i) == 1:
                    return True
            # if there isn't a piece (default to false when no piece there) at the desired position, can move
            if not piece_pos.piece:
                return True
            # don't land on your own piece (same color)!
            elif piece_pos.piece.color == self.color:
                return False
            elif piece_pos.piece.color != self.color:  # land on another guy's piece
                if piece_pos.rosette:  # if they're on a rosette
                    return False  # cannot move
                else:
                    return True   # piece wasn't a rosette (rosette still false)


class BoardSquare:
    def __init__(self, x, y, entrance=False, _exit=False, rosette=False, forbidden=False):
        self.piece = None
        self.position = (x, y)
        self.next_white = None
        self.next_black = None
        self.exit = _exit
        self.entrance = entrance
        self.rosette = rosette
        self.forbidden = forbidden

    def load_from_json(self, json_string):
        import json
        loaded_position = json.loads(json_string)
        self.piece = None
        self.position = loaded_position['position']
        self.next_white = loaded_position['next_white']
        self.next_black = loaded_position['next_black']
        self.exit = loaded_position['exit']
        self.entrance = loaded_position['entrance']
        self.rosette = loaded_position['rosette']
        self.forbidden = loaded_position['forbidden']

    def jsonify(self):
        next_white = self.next_white.position if self.next_white else None
        next_black = self.next_black.position if self.next_black else None
        return {'position': self.position, 'next_white': next_white, 'next_black': next_black,
                'exit': self.exit, 'entrance': self.entrance, 'rosette': self.rosette, 'forbidden': self.forbidden}
