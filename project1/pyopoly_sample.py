from board_methods import load_map, display_board


QUIT_STRING = 'quit'

if __name__ == '__main__':
    for line in load_map('p.csv'):
        print(line)

    the_board = []
    for i in range(8):
        the_board.append(
            input('What is the name of position {}? '.format(i))[0:5].ljust(5) + '\n     ')
        # the_board.append((str(i) * 5)[0:5] + '\n' + (str(i) * 5)[0:5])
        print(the_board[i])
        # format for display is this:
        # "xxxxx\nxxxxx"

    # ljust(5) pads your string with spaces to ensure it's length 5.
    display_board(the_board)

    print('hello world'.ljust(5))
    position = 0
    s = input('How many? ')
    while s != QUIT_STRING:
        position += int(s)
        position %= len(the_board)
        copy_board = list(the_board)
        copy_board[position] = copy_board[position][0:6] + "Play "
        display_board(copy_board)
        s = input('How many? ')
