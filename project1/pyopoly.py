"""
File:         pyopoly.py
Author:       Matthew Makila
Date:         10/19/2020
Section:      44
E-mail:       mmakila1@umbc.edu
Description:  Coding game of Monopoly with Python.
              Uses many dictionaries, function definitions, lists, file imports
              for loops, etc to compile game design and player turns.
"""
from sys import argv
from random import seed, randint
from board_methods import load_map, display_board

# possibly a lot more code here.
# this code can be anywhere from right under the imports to right # above if __name__ == '__main__':
if len(argv) >= 2:
    seed(argv[1])


def play_game(pass_go_money, starting_money, board_file):
    """
    :param starting_money: Take in constant of start money (1500)
    :param board_file: Take in csv board file
    :param pass_go_money: Take in pass go constant of 200
    :return:
    """
    # Makes the two characters, each with unique uppercase symbol
    symbols_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M',
                    'N', 'O', 'P', 'Q', 'Q', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    name_1 = input("First player, what is your name? ")
    player1_symbol = input("First player, what symbol do you want your character to use? ")
    while player1_symbol not in symbols_list:
        player1_symbol = input("First player, what symbol do you want your character to use? ")

    name_2 = input("Second player, what is your name? ")
    player2_symbol = input("Second player, what symbol do you want your character to use? ")
    while player2_symbol not in symbols_list or player2_symbol == player1_symbol:
        player2_symbol = input("Second player, what symbol do you want your character to use? ")
    current_pos = 0
    current_money = starting_money
    # Initialize player attributes in dictionary
    players = {'play1': {'name': name_1, 'symbol': player1_symbol, 'position': current_pos, 'money': current_money,
                         'properties': [], 'properties_abbrev': []},
               'play2': {'name': name_2, 'symbol': player2_symbol, 'position': current_pos, 'money': current_money,
                         'properties': [], 'properties_abbrev': []}}
    # parse the board to extract info for separate dictionaries
    the_board = load_map(board_file)
    x = 0
    for line in the_board:
        name = line['Place']
        abbrev_dict[name] = line['Abbrev']
        color_dict[name] = line['Color']
        who_owns_dict[name] = 'BANK'
        has_building_dict[name] = 'No'
        pos_dict[x] = name
        price_dict[name] = int(line['Price'])
        rent_dict[name] = int(line['Rent'])
        building_rent_dict[name] = int(line['BuildingRent'])
        building_cost_dict[name] = int(line['BuildingCost'])
        x += 1
    monopoly_board = []
    # assemble the monopoly board
    for abbrev in abbrev_dict:
        monopoly_board.append((abbrev_dict[abbrev])[0:5].ljust(5) + '\n      ')
    # initialize terminating condition for loser and turn
    loser = False
    turn = 1
    while not loser:
        take_turn(turn, players, monopoly_board, pass_go_money)
        turn += 1
        if players['play1']['money'] < 0 or players['play2']['money'] < 0:
            loser = True
            if players['play1']['money'] < 0:
                print('{} has gone Bankrupt! {} is the winner, the Game is finally over, and we can all go home!'.
                      format(players['play1']['name'], players['play2']['name']))
            else:
                print('{} has gone Bankrupt! {} is the winner, the Game is finally over, and we can all go home!'.
                      format(players['play2']['name'], players['play1']['name']))


def take_turn(turn, players, board, pass_go_money):
    """
    :param turn: Which player's turn it is
    :param players: Take in the dictionary of player info
    :param board: Take in the board template
    :param pass_go_money: Take in the pass_go constant of 200
    :return: None
    """
    if turn % 2 == 1:
        # player 1 gets the move
        last_pos = players['play1']['position']
        # update their position with roll of two random die
        roll_dice = randint(1, 6) + randint(1, 6)
        players['play1']['position'] += int(roll_dice)
        distance_traveled = players['play1']['position']
        players['play1']['position'] %= len(board)
        copy_board = list(board)
        # add pass go money when passing go
        if players['play1']['position'] < last_pos or players['play1']['position'] == 0 \
                or (distance_traveled / len(board)) > 1:
            players['play1']['money'] += pass_go_money
            if distance_traveled/len(board) > 2:
                players['play1']['money'] += pass_go_money
        # update the board
        format_display(players, copy_board)
        print('{} you have rolled'.format(players['play1']['name']), roll_dice)
        print('{} you have landed on {}\n'.format(players['play1']['name'], pos_dict[players['play1']['position']]))
        # if they land on other player's property, get the rent
        loser = False
        if who_owns_dict[pos_dict[players['play1']['position']]] == players['play2']['name']:
            print("You have landed on {}'s property, you must pay the rent".format(players['play2']['name']))
            get_rent(players['play1'], players['play2'], pos_dict[players['play1']['position']])
            if players['play1']['money'] < 0:
                loser = True
                print("You have been knocked out of the game")
        # show the player menu, terminate menu when 5 entered or if someone lost
        if not loser:
            player_choice = show_menu()
            while player_choice != '5':
                if player_choice == '1':
                    buy_property(players, turn, pos_dict[players['play1']['position']])
                elif player_choice == '2':
                    get_prop_info()
                elif player_choice == '3':
                    get_player_info(players['play1'], players['play2'])
                elif player_choice == '4':
                    build_building(players['play1'])
                player_choice = show_menu()
            turn += 1
    else:
        # player 2 go
        last_pos = players['play2']['position']
        roll_dice = randint(1, 6) + randint(1, 6)
        players['play2']['position'] += int(roll_dice)
        distance_traveled = players['play2']['position']
        players['play2']['position'] %= len(board)
        copy_board = list(board)
        if players['play2']['position'] < last_pos or players['play2']['position'] == 0 \
                or (distance_traveled / len(board)) > 1:
            players['play2']['money'] += pass_go_money
            if distance_traveled/len(board) > 2:
                players['play2']['money'] += pass_go_money
        format_display(players, copy_board)
        print('{} you have rolled'.format(players['play2']['name']), roll_dice)
        print('{} you have landed on {}\n'.format(players['play2']['name'], pos_dict[players['play2']['position']]))
        loser = False
        if who_owns_dict[pos_dict[players['play2']['position']]] == players['play1']['name']:
            print("You have landed on {}'s property. You must pay the rent".format(players['play1']['name']))
            get_rent(players['play2'], players['play1'], pos_dict[players['play2']['position']])
            if players['play1']['money'] < 0:
                loser = True
                print("You have been knocked out of the game")
        if not loser:
            player_choice = show_menu()
            while player_choice != '5':
                if player_choice == '1':
                    buy_property(players, turn, pos_dict[players['play2']['position']])
                elif player_choice == '2':
                    get_prop_info()
                elif player_choice == '3':
                    get_player_info(players['play1'], players['play2'])
                elif player_choice == '4':
                    build_building(players['play2'])
                player_choice = show_menu()
            turn += 1


def get_rent(player_who_owes, player_getting_paid, the_property):
    """
    :param player_who_owes: The player who landed on another player's property
    :param player_getting_paid: The player receiving rent compensation
    :param the_property: The property landed on
    :return: None
    """
    # take basic rent if no building, otherwise, take bigger rent with building
    if has_building_dict[the_property] == 'No':
        print('You have paid {} to {}\n'.format(rent_dict[the_property], player_getting_paid['name']))
        player_who_owes['money'] -= rent_dict[the_property]
        player_getting_paid['money'] += rent_dict[the_property]
    else:
        print('You have paid {} to {}\n'.format(building_rent_dict[the_property], player_getting_paid['name']))
        player_who_owes['money'] -= building_rent_dict[the_property]
        player_getting_paid['money'] += building_rent_dict[the_property]


def buy_property(players, turn, the_property):
    """
    :param players: Take in the list of player attributes
    :param turn: Take in player's turn
    :param the_property: Take in property landed on
    :return: None
    """
    if turn % 2 == 1:
        # player 1 goes: if owned by bank, buyable, and player has enough money, buy building and subtract cost
        if who_owns_dict[the_property] == 'BANK' and price_dict[the_property] != -1:
            decision = input('This property is unowned, would you like to buy it? ')
            if (decision.lower() == 'y' or decision.lower() == 'yes') and players['play1']['money'] >= \
                    price_dict[the_property]:
                print('You have bought {}\n'.format(the_property))
                players['play1']['money'] -= price_dict[the_property]
                who_owns_dict[the_property] = players['play1']['name']
                players['play1']['properties'].append(the_property)
                players['play1']['properties_abbrev'].append(abbrev_dict[the_property])
            elif decision.lower() == 'n' or decision.lower() == 'no':
                print('You have decided not to buy Susquehanna Hall\n')
            elif players['play1']['money'] < price_dict[the_property]:
                print('You cannot afford to buy this property\n')
        elif who_owns_dict[the_property] != 'BANK' and price_dict[the_property] != -1:
            print("{} owns this property. You cannot buy it.\n".format(who_owns_dict[the_property]))
        else:
            print("You cannot buy this property. It cannot be bought or sold\n")
    else:
        if who_owns_dict[the_property] == 'BANK' and price_dict[the_property] != -1:
            decision = input('This property is unowned, would you like to buy it? ')
            if (decision.lower() == 'y' or decision.lower() == 'yes') and players['play2']['money'] >= \
                    price_dict[the_property]:
                print('You have bought {}\n'.format(the_property))
                players['play2']['money'] -= price_dict[the_property]
                who_owns_dict[the_property] = players['play2']['name']
                players['play2']['properties'].append(the_property)
                players['play2']['properties_abbrev'].append(abbrev_dict[the_property])
            elif decision.lower() == 'n' or decision.lower() == 'no':
                print('You have decided not to buy Susquehanna Hall\n')
            elif players['play2']['money'] < price_dict[the_property]:
                print('You cannot afford to buy this property\n')
        elif who_owns_dict[the_property] != 'BANK' and price_dict[the_property] != -1:
            print("{} owns this property. You cannot buy it.\n".format(who_owns_dict[the_property]))
        else:
            print("You cannot buy this property. It cannot be bought or sold\n")


def get_prop_info():
    """
    :return: None (displays property info upon call)
    """
    # when property is searched for by name or by abbrev, display price, owner, if has building, and rent(s)
    property_search = input('For which property do you want to get the information? ')
    # if search is a key
    if property_search in abbrev_dict:
        print("\n\t\t{}".format(property_search))
        print("\t\tPrice: {}\n\t\tOwner: {}\n\t\tBuilding: {}\n\t\tRent: {}, {} (with building)\n".format(
            price_dict[property_search], who_owns_dict[property_search], has_building_dict[property_search],
            rent_dict[property_search], building_rent_dict[property_search]))
    else:  # if search is the val
        for name in abbrev_dict:
            if abbrev_dict[name] == property_search:
                print("\n\t\t{}".format(name))
                print("\t\tPrice: {}\n\t\tOwner: {}\n\t\tBuilding: {}\n\t\tRent: {}, {} (with building)\n".
                      format(price_dict[name], who_owns_dict[name], has_building_dict[name], rent_dict[name],
                             building_rent_dict[name]))


def get_player_info(player1, player2):
    """
    :param player1: Take in the first player
    :param player2: Take in the second player
    :return: None
    """
    # display the two players and chooses who to examine. Once player selected, display name, symbol, money, properties
    print("The players are:\n\t\t{}\n\t\t{}".format(player1['name'], player2['name']))
    which_user = input("Which player do you wish to know about? ")
    if which_user == player1['name']:
        print("\nPlayer name: {}\nPlayer Symbol: {}\nCurrent Money: {}\n".format(player1['name'],
                                                                                 player1['symbol'], player1['money']))
        print("Properties Owned:")
        if not player1['properties']:
            print("\n\t\t\tNo properties yet.\n")
        else:
            for place in player1['properties']:
                is_building = False
                if has_building_dict[place] == "Yes":
                    is_building = True
                print("\t\t\t{} with a building: {}".format(place, is_building))
            print()
    elif which_user == player2['name']:
        print("\nPlayer name: {}\nPlayer Symbol: {}\nCurrent Money: {}\n".format(player2['name'],
                                                                                 player2['symbol'], player2['money']))
        print("Properties Owned:")
        if not player2['properties']:
            print("\n\t\t\tNo properties yet.\n")
        else:
            for place in player2['properties']:
                is_building = False
                if has_building_dict[place] == "Yes":
                    is_building = True
                print("\t\t\t{} with a building: {}".format(place, is_building))
            print()


def build_building(player):
    """
    :param player: Take in the player who wants to build a building
    :return: None
    """
    # if given player owns any properties, list them
    if player['properties']:
        for place in player['properties']:
            if has_building_dict[place] == 'No':
                print("{} {} {}".format(place, abbrev_dict[place], building_cost_dict[place]))
    # if property owned by player, not already building, and affordable, make building and subtract cost
    which_property = input("Which property do you want to build a building on? ")
    if which_property in player['properties'] and has_building_dict[which_property] == 'No':
        if player['money'] >= building_cost_dict[which_property]:
            print("You have built the building for {}".format(which_property))
            player['money'] -= building_cost_dict[which_property]
            has_building_dict[which_property] = 'Yes'
        else:
            print("You don't have enough to build there")
    elif which_property in player['properties_abbrev']:
        for name in abbrev_dict:
            if abbrev_dict[name] == which_property:
                if player['money'] >= building_cost_dict[name] and has_building_dict[name] == 'No':
                    if abbrev_dict[name] == which_property:
                        print("You have built the building for {}".format(name))
                        player['money'] -= building_cost_dict[name]
                        has_building_dict[name] = 'Yes'
                elif player['money'] < price_dict[name]:
                    print("You don't have enough to build there")
                else:
                    print("The property either has a building, isn't yours, is not affordable, or doesn't exist")
    else:
        print("The property either has a building, isn't yours, or doesn't exist")


def format_display(players, c_board):
    """
    :param c_board: Take in the compiled board updated with the latest turn
    :param players: Take in the two players on the board
    :return: None
    """
    # When players land on same spot, draw them together
    if players['play1']['position'] == players['play2']['position']:
        c_board[players['play1']['position']] = c_board[players['play1']['position']][0:6] + "{}{}".format(
            players['play1']['symbol'], players['play2']['symbol'])
        c_board[players['play2']['position']] = c_board[players['play2']['position']][0:6] + "{}{}".format(
            players['play1']['symbol'], players['play2']['symbol'])
    # (most typically) just draw characters where they are on board
    else:
        c_board[players['play2']['position']] = c_board[players['play2']['position']][0:6] + \
                                                "{}".format(players['play2']['symbol'])
        c_board[players['play1']['position']] = c_board[players['play1']['position']][0:6] + \
                                                "{}".format(players['play1']['symbol'])
    display_board(c_board)


def show_menu():
    """
    :return: menu_choice
    """
    # displays menu options and awaits proper input from menu options constant
    menu_choice = ''
    while menu_choice not in MENU_OPTIONS:
        print("\t1) Buy Property\n\t2) Get Property Info\n\t3) Get Player Info\n\t"
              "4) Build a Building\n\t5) End Turn\n")
        menu_choice = input('\tWhat do you want to do?\n\t')
    return menu_choice


PASS_GO = 200
STARTER_MONEY = 1500
MENU_OPTIONS = ['1', '2', '3', '4', '5']

abbrev_dict = {}
color_dict = {}
pos_dict = {}
price_dict = {}
rent_dict = {}
building_rent_dict = {}
building_cost_dict = {}
who_owns_dict = {}
has_building_dict = {}

if __name__ == "__main__":
    play_game(PASS_GO, STARTER_MONEY, 'proj1_board1.csv')
