from sys import argv
from random import choice
from board_square import BoardSquare, UrPiece


class RoyalGameOfUr:
    STARTING_PIECES = 7
    NUM_PLAYERS = 2

    def __init__(self, board_file_name):
        self.board = None
        self.load_board(board_file_name)
        self.white_entrance = None
        self.black_entrance = None

    def load_board(self, board_file_name):
        """
        This function takes a file name and loads the map, creating BoardSquare objects in a grid.

        :param board_file_name: the board file name
        :return: sets the self.board object within the class
        """

        import json
        try:
            with open(board_file_name) as board_file:
                board_json = json.loads(board_file.read())
                self.num_pieces = self.STARTING_PIECES
                self.board = []
                for x, row in enumerate(board_json):
                    self.board.append([])
                    for y, square in enumerate(row):
                        self.board[x].append(BoardSquare(x, y, entrance=square['entrance'], _exit=square['exit'],
                                                         rosette=square['rosette'], forbidden=square['forbidden']))

                for i in range(len(self.board)):
                    for j in range(len(self.board[i])):
                        if board_json[i][j]['next_white']:
                            x, y = board_json[i][j]['next_white']
                            self.board[i][j].next_white = self.board[x][y]
                        if board_json[i][j]['next_black']:
                            x, y = board_json[i][j]['next_black']
                            self.board[i][j].next_black = self.board[x][y]
        except OSError:
            print('The file was unable to be opened. ')

    def draw_block(self, output, i, j, square):
        """
        Helper function for the display_board method
        :param output: the 2d output list of strings
        :param i: grid position row = i
        :param j: grid position col = j
        :param square: square information, should be a BoardSquare object
        """
        MAX_X = 8
        MAX_Y = 5
        for y in range(MAX_Y):
            for x in range(MAX_X):
                if x == 0 or y == 0 or x == MAX_X - 1 or y == MAX_Y - 1:
                    output[MAX_Y * i + y][MAX_X * j + x] = '+'
                if square.rosette and (y, x) in [(1, 1), (1, MAX_X - 2), (MAX_Y - 2, 1), (MAX_Y - 2, MAX_X - 2)]:
                    output[MAX_Y * i + y][MAX_X * j + x] = '*'
                if square.piece:
                    # print(square.piece.symbol)
                    output[MAX_Y * i + 2][MAX_X * j + 3: MAX_X * j + 5] = square.piece.symbol

    def display_board(self):
        """
        Draws the board contained in the self.board object

        """
        if self.board:
            output = [[' ' for _ in range(8 * len(self.board[i//5]))] for i in range(5 * len(self.board))]
            for i in range(len(self.board)):
                for j in range(len(self.board[i])):
                    if not self.board[i][j].forbidden:
                        self.draw_block(output, i, j, self.board[i][j])

            print('\n'.join(''.join(output[i]) for i in range(5 * len(self.board))))

    def roll_d4_dice(self, n=4):
        """
        Keep this function as is.  It ensures that we'll have the same runs with different random seeds for rolls.
        :param n: the number of tetrahedral d4 to roll, each with one dot on
        :return: the result of the four rolls.
        """
        dots = 0
        for _ in range(n):
            dots += choice([0, 1])
        return dots

    def play_game(self):
        """
            Your job is to recode this function to play the game.
        """
        # first set players up with names, team color, and arrange their 7 pieces
        # find entrance of board
        self.find_start()
        # return var for player pieces and names
        play1, play2, play1_name, play2_name = self.set_up_players()
        self.display_board()
        roll = self.roll_d4_dice()
        print("You rolled {}".format(roll))
        turn = 1
        winner = False  # loser True when all a player's pieces are "complete"
        while not winner:
            player, name = self.take_turn(turn, play1, play2, play1_name, play2_name)
            possible_moves = self.display_player_moves(player, roll)
            # if no possible moves, skip turn
            if possible_moves:
                # if move possible, select proper piece to move
                move_choice = int(input("Which piece would you like to move? "))  # make a list of 1-7
                invalid_input = True
                while invalid_input:
                    if 0 <= move_choice - 1 < len(possible_moves):
                        invalid_input = False
                    else:
                        move_choice = int(input("Sorry, that's not a valid selection, "
                                                "which move do you wish to make?"))
                piece = possible_moves[move_choice - 1]
                self.move_piece(piece, roll, player)
            num_pieces_complete = 0
            # check if a person has cleared all 7 pieces, if so, they win
            for i in range(self.STARTING_PIECES):
                if player[i].complete:
                    num_pieces_complete += 1
            if num_pieces_complete == self.STARTING_PIECES:
                winner = True
                print("WE HAVE A WINNER! Congratulations to {}!".format(name))
            # if winner, quit
            if not winner:
                self.display_board()
                roll = self.roll_d4_dice()
                print("You rolled {}".format(roll))
                turn += 1

    def find_start(self):
        # find and set the white and black entrance points for the board
        for i in range(len(self.board)):
            for j in range(len(self.board[i])):
                if self.board[i][j].entrance == WHITE:
                    self.white_entrance = self.board[i][j]
                elif self.board[i][j].entrance == BLACK:
                    self.black_entrance = self.board[i][j]

    def take_turn(self, turn, player1, player2, play1_name, play2_name):
        """
        :param play1_name: name of the first player
        :param play2_name: name of second player
        :param turn: which turn number it currently is
        :param player1: first player pieces
        :param player2: second player pieces
        :return: the player whose turn it is
        """
        if turn % 2 == 1:
            return player1, play1_name
        elif turn % 2 == 0:
            return player2, play2_name

    def set_up_players(self):
        # create players with their names and pieces
        player1 = input("What is your name? ")
        print("{} you will play as white.".format(player1))
        player2 = input("What is your name? ")
        print("{} you will play as black.".format(player2))
        player1_pieces = []
        player2_pieces = []
        # make pieces for each player
        for i in range(self.NUM_PLAYERS):
            for j in range(self.STARTING_PIECES):
                if i == 0:
                    player1_pieces.append(UrPiece(WHITE, 'W{}'.format(j + 1)))
                else:
                    player2_pieces.append(UrPiece(BLACK, 'B{}'.format(j + 1)))
        return player1_pieces, player2_pieces, player1, player2

    def display_player_moves(self, player, roll):
        """
        :param roll: The current die roll
        :param player: take in the player's pieces
        :return: return piece moves that are possible
        """
        possibilities = []
        complete_list = []
        choice_list_place = 0
        for i in range(self.STARTING_PIECES):
            piece = player[i]
            # if a piece already on the board and it can move, put it in possible moves
            if piece.position and piece.can_move(roll):
                print(choice_list_place + 1, '{}: {}'.format(piece.symbol, piece.position.position))
                choice_list_place += 1
                possibilities.append(piece)
            # if piece is not on board YET, but can be with the current roll ...
            elif not piece.position and not piece.complete:
                if piece.color == WHITE:
                    # simulate if a piece not on the board yet can enter
                    piece.set_start(self.white_entrance)
                    if piece.can_move(roll):
                        print(choice_list_place + 1, 'Piece {} is currently off the board.'.format(player[i].symbol))
                        choice_list_place += 1
                        piece.set_start(None)
                        possibilities.append(piece)
                    # if piece can't enter board and isn't on board, it's not an option
                    else:
                        piece.position = None
                        piece.set_start(None)
                elif piece.color == BLACK:
                    piece.set_start(self.black_entrance)
                    if piece.can_move(roll):
                        print(choice_list_place + 1, 'Piece {} is currently off the board.'.format(player[i].symbol))
                        choice_list_place += 1
                        piece.set_start(None)
                        possibilities.append(piece)
                    else:
                        piece.position = None
                        piece.set_start(None)
            # if the piece completed journey, add to list of completed pieces
            elif piece.complete:
                complete_list.append(piece)
        for i in range(len(complete_list)):
            print('{} has completed its path'.format(complete_list[i].symbol))
        return possibilities

    def move_piece(self, piece, roll, player):
        """
        :param player: the player pieces (
        :param roll: the roll to move the piece by
        :param piece: take in the piece to move
        :return: the updated move
        """
        # when piece is not on board yet
        if not piece.position:
            if piece.color == WHITE:
                # check if it can enter and if there is a piece already there or not
                piece.position = self.white_entrance
                if not self.white_entrance.piece:
                    self.white_entrance.piece = piece
                for i in range(roll - 1):
                    # Remove a piece from its previous board square
                    if piece.position.piece.symbol == piece.symbol:
                        piece.position.piece = None
                    # move piece pos to next next pos
                    piece.position = piece.position.next_white
                    # if there isn't already a different piece there, we can write our piece on it
                    if not piece.position.piece:
                        piece.position.piece = piece
                # knock off an opponent's piece
                if piece.position.piece:
                    if piece.position.piece.color != piece.color:
                        self.knock_off(piece.position.piece, piece)
                # rosette re-roll to roll another turn for this player
                if piece.position:
                    if piece.position.rosette:
                        piece.position.piece = piece
                        self.rosette_re_roll(player)

            elif piece.color == BLACK:
                piece.position = self.black_entrance
                if not self.black_entrance.piece:
                    self.black_entrance.piece = piece
                for i in range(roll - 1):
                    if piece.position.piece.symbol == piece.symbol:
                        piece.position.piece = None
                    piece.position = piece.position.next_black
                    if not piece.position.piece:
                        piece.position.piece = piece
                if piece.position.piece:
                    if piece.position.piece.color != piece.color:
                        self.knock_off(piece.position.piece, piece)
                if piece.position:
                    if piece.position.rosette:
                        piece.position.piece = piece
                        self.rosette_re_roll(player)

        elif piece.position:  # if pieces are on the board
            if piece.color == WHITE:
                for i in range(roll):
                    # Remove a piece from its previous board square
                    if piece.position.piece.symbol == piece.symbol:
                        piece.position.piece = None
                    # move piece to next_pos
                    piece.position = piece.position.next_white
                    # if the piece exits the board, it's free
                    if not piece.position:
                        piece.complete = True
                        print('{} has completed its path'.format(piece.symbol))
                    # if there isn't already a different piece there, we can write our piece on it
                    elif not piece.position.piece:
                        piece.position.piece = piece
                # knock off an opponent's piece
                if piece.position:
                    if piece.position.piece:
                        if piece.position.piece.color != piece.color:
                            self.knock_off(piece.position.piece, piece)
                # rosette re-roll
                if piece.position:
                    if piece.position.rosette:
                        piece.position.piece = piece
                        self.rosette_re_roll(player)

            elif piece.color == BLACK:
                for i in range(roll):
                    if piece.position.piece.symbol == piece.symbol:
                        piece.position.piece = None
                    piece.position = piece.position.next_black
                    if not piece.position:
                        piece.complete = True
                        print('{} has completed its path'.format(piece.symbol))
                    elif not piece.position.piece:
                        piece.position.piece = piece
                if piece.position:
                    if piece.position.piece:
                        if piece.position.piece.color != piece.color:
                            self.knock_off(piece.position.piece, piece)
                if piece.position:
                    if piece.position.rosette:
                        piece.position.piece = piece
                        self.rosette_re_roll(player)

    def knock_off(self, piece_to_remove, piece_to_keep):
        """
        :param piece_to_remove: the piece getting captured
        :param piece_to_keep: the piece capturing
        :return:
        """
        # set piece that's removed to None again (off board, the start) & bs's piece to piece being kept
        piece_to_remove.position.piece = None
        piece_to_remove.position = None
        piece_to_keep.position.piece = piece_to_keep
        print('{} has been captured and removed from the board'.format(piece_to_remove.symbol))

    def rosette_re_roll(self, player):
        """
        :param player: the player pieces
        :return:
        """
        # give player 1 additional move for rosette landing
        for i in range(1):
            self.display_board()
            print("You landed on a rosette, move again!")
            roll = self.roll_d4_dice()
            print("You rolled {}".format(roll))
            possible_moves = self.display_player_moves(player, roll)
            if possible_moves:
                move_choice = int(input("Which piece would you like to move? "))  # make a list of 1-7
                invalid_input = True
                while invalid_input:
                    if 0 <= move_choice - 1 < len(possible_moves):
                        invalid_input = False
                    else:
                        move_choice = int(input("Sorry, that's not a valid selection, "
                                                "which move do you wish to make?"))
                piece = possible_moves[move_choice - 1]
                self.move_piece(piece, roll, player)


WHITE = 'White'
BLACK = 'Black'

if __name__ == '__main__':
    file_name = input('What is the file name of the board json? ') if len(argv) < 2 else argv[1]
    rgu = RoyalGameOfUr(file_name)
    rgu.play_game()
