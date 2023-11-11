"""
File:    network.py
Author:  Matthew Makila
Date:    11/25/2020
Section: 44
E-mail:  mmakila1@umbc.edu
Description:
  This code creates a network and allows for the creation of switchboard objects which may create various phone
  objects. The network hosts the switchboards in a list and allows for them to be created and connected to one another.
  The network has methods to save and load itself.


network.py is both the definition file for the Network class as well as the driver for the program.

In network you need to implement the functions which the driver will call for the all the different commands.
"""

from switchboard import Switchboard
import csv

"""
import json
import csv (you can do either if you choose, or just use the regular file io)

Some constants below are for the driver, don't remove them unless you mean to.  
"""

HYPHEN = "-"
QUIT = 'quit'
SWITCH_CONNECT = 'switch-connect'
SWITCH_ADD = 'switch-add'
PHONE_ADD = 'phone-add'
NETWORK_SAVE = 'network-save'
NETWORK_LOAD = 'network-load'
START_CALL = 'start-call'
END_CALL = 'end-call'
DISPLAY = 'display'


class Network:
    def __init__(self):
        """
            Construct a network by creating the switchboard container object

            You are free to create any additional data/members necessary to maintain this class.
        """
        self.area_codes = []
        self.switchboards = []

    def load_network(self, filename):
        """
        :param filename: the name of the file to be loaded.  Assume it exists and is in the right format.
                If not, it's ok if your program fails.
        :return: success?
        """
        the_network.switchboards = []
        with open('{}.csv'.format(filename), 'r') as load_file:
            # clear the previous network
            the_network.switchboards = []
            # load file into the reader
            my_reader = csv.DictReader(load_file)

            for line in my_reader:
                # cast the area code of the switchboard as int
                area = int(line['Area Code'])

                # put all of the trunk lines for one switchboard into a list from str
                trunks = line['Trunk Connected Areas']
                trunks = trunks.strip('][').split(', ')
                # put all of the phones for one switchboard into a list from str
                phones = line['Phones']
                phones = phones.strip('][').split(', ')

                # make the area code saved into a switchboard if it does not already exist
                if area not in the_network.area_codes:
                    the_network.add_switchboard(area)

                # find specific switchboard we refer to for trunk lines and phones
                for i in range(len(the_network.switchboards)):
                    if the_network.switchboards[i].area_code == area:
                        switchboard = the_network.switchboards[i]

                # if the list of trunk lines has any boards, make that board an int and add to list if it doesn't exist
                for k in range(len(trunks)):
                    if trunks[k]:
                        if int(trunks[k]) not in the_network.area_codes:
                            the_network.add_switchboard(int(trunks[k]))

                        for j in range(len(the_network.switchboards)):
                            if the_network.switchboards[j].area_code == int(trunks[k]):
                                trunk = the_network.switchboards[j]
                                switchboard.trunk_lines.append(trunk)

                # if the list of phones has any phones, make that phone an int and add to list if it doesn't exist
                for p in range(len(phones)):
                    if phones[p]:
                        if int(phones[p]) not in switchboard.phones:
                            switchboard.add_phone(int(phones[p]))

    def save_network(self, filename):
        """
        :param filename: the name of your file to save the network.  Remember that you need to save all the
            connections, but not the active phone calls (they can be forgotten between save and load).
            You must invent the format of the file, but if you wish you can use either json or csv libraries.
        :return: success?
        """
        with open('{}.csv'.format(filename), 'w', newline='') as save_file:
            # create header for save document
            header = ['Area Code', 'Trunk Connected Areas', 'Phones']
            # create writer to save network data into file
            my_writer = csv.DictWriter(save_file, fieldnames=header)
            my_writer.writeheader()

            # for every switchboard, save area code, trunk lines (codes), and phones (nums) to be reloaded in future.
            for i in range(len(the_network.switchboards)):
                row = {'Area Code': None, 'Trunk Connected Areas': [],
                       'Phones': []}
                switchboard = the_network.switchboards[i]
                row['Area Code'] = switchboard.area_code

                for j in range(len(switchboard.trunk_lines)):
                    trunk_line = switchboard.trunk_lines[j]
                    row['Trunk Connected Areas'].append(trunk_line.area_code)
                for k in range(len(switchboard.phones)):
                    phone = switchboard.phones[k]
                    row['Phones'].append(phone.number)

                my_writer.writerow(row)

    def add_switchboard(self, area_code):
        """
        add switchboard should create a switchboard and add it to your network.

        By default it is not connected to any other boards and has no phone lines attached.
        :param area_code: the area code for the new switchboard
        :return:
        """
        if area_code not in self.area_codes:
            self.area_codes.append(area_code)
            self.switchboards.append(Switchboard(area_code))
        else:
            print('The code {} is already in use with another switchboard'.format(area_code))

    def connect_switchboards(self, area_1, area_2):
        """
            Connect switchboards should connect the two switchboards (creates a trunk line between them)
            so that long distance calls can be made.
        :param area_1: area-code 1
        :param area_2: area-code 2
        :return: success/failure
        """
        # if both switchboards have been created, connect them via .add_trunk_connection
        # if both switchboards exist, we know the boards have potential to connect, without fail.
        if area_1 in self.area_codes and area_2 in self.area_codes:
            switchboard_1 = None
            switchboard_2 = None
            for i in range(len(self.switchboards)):

                switchboard = self.switchboards[i]

                if switchboard.area_code == area_1:
                    switchboard_1 = switchboard

                if switchboard.area_code == area_2:
                    switchboard_2 = switchboard

            if switchboard_1 and switchboard_2:
                switchboard_1.add_trunk_connection(switchboard_2)
                switchboard_2.add_trunk_connection(switchboard_1)
        else:
            print('One or more of the switchboards attempted to connect does not exist.')

    def display(self):
        """
            Display should output the status of the phone network as described in the project.
        """
        for i in range(len(self.switchboards)):
            switchboard = self.switchboards[i]

            print('Switchboard with area code: {}'.format(switchboard.area_code))

            print('\tTrunk lines are: ')

            for j in range(len(switchboard.trunk_lines)):
                print('\t\tTrunk line connection to: {}'.format(switchboard.trunk_lines[j].area_code))

            print('\tLocal phone numbers are: ')

            for k in range(len(switchboard.phones)):
                # check if phone.is_connected:
                if switchboard.phones[k].other_phone_call:
                    print('\t\tPhone with number: {} is connected to {}-{}'.format(switchboard.phones[k].number,
                            switchboard.phones[k].other_phone_call.switchboard.area_code,
                            switchboard.phones[k].other_phone_call.number))
                else:
                    print('\t\tPhone with number: {} is not in use'.format(switchboard.phones[k].number))


if __name__ == '__main__':
    the_network = Network()
    s = input('Enter command: ')
    while s.strip().lower() != QUIT:
        split_command = s.split()
        if len(split_command) == 3 and split_command[0].lower() == SWITCH_CONNECT:
            area_1 = int(split_command[1])
            area_2 = int(split_command[2])
            the_network.connect_switchboards(area_1, area_2)
        elif len(split_command) == 2 and split_command[0].lower() == SWITCH_ADD:
            the_network.add_switchboard(int(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == PHONE_ADD:
            number_parts = split_command[1].split(HYPHEN)
            area_code = int(number_parts[0])
            phone_number = int(''.join(number_parts[1:]))

            phone_finder = False
            for i in range(len(the_network.switchboards)):
                if the_network.switchboards[i].area_code == area_code:
                    # print('we found the phone to add')
                    the_network.switchboards[i].add_phone(phone_number)
                    phone_finder = True
            if not phone_finder:
                print('That number could not be added')

        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_SAVE:
            the_network.save_network(split_command[1])
            print('Network saved to {}.'.format(split_command[1]))
        elif len(split_command) == 2 and split_command[0].lower() == NETWORK_LOAD:
            the_network.load_network(split_command[1])
            print('Network loaded from {}.'.format(split_command[1]))
        elif len(split_command) == 3 and split_command[0].lower() == START_CALL:
            src_number_parts = split_command[1].split(HYPHEN)
            src_area_code = int(src_number_parts[0])
            src_number = int(''.join(src_number_parts[1:]))

            dest_number_parts = split_command[2].split(HYPHEN)
            dest_area_code = int(dest_number_parts[0])
            dest_number = int(''.join(dest_number_parts[1:]))

            # makes sure both the source and destination area codes exist
            if src_area_code in the_network.area_codes and dest_area_code in the_network.area_codes:
                # first check if the destination phone number is real
                dest_phone = None

                for i in range(len(the_network.switchboards)):
                    dest_switch = the_network.switchboards[i]

                    for j in range(len(dest_switch.phones)):
                        # locate the dest switchboard number to verify it exists

                        if dest_switch.phones[j].number == dest_number and dest_switch.phones[j].switchboard.area_code \
                                == dest_area_code:
                            dest_phone = dest_switch.phones[j]
                # if the destination number exists, check if the source number exists
                if dest_phone:
                    src_phone = None

                    for i in range(len(the_network.switchboards)):
                        a_switchboard = the_network.switchboards[i]

                        for j in range(len(a_switchboard.phones)):
                            # locate the switchboard whose number matches the given source number

                            if a_switchboard.phones[j].number == src_number and a_switchboard.phones[j].switchboard. \
                                    area_code == src_area_code:
                                # calls function to connect source phone to dest phone
                                src_phone = a_switchboard.phones[j]
                                can_connect = src_phone.connect(dest_phone)

                                if can_connect:
                                    print('Success, {}-{} is now connected with {}-{}'.format(src_area_code, src_number,
                                                                                              dest_area_code,
                                                                                              dest_number))
                                else:
                                    print('The phones could not be connected.')

                    if not src_phone:
                        print('{}-{} is not a valid number'.format(src_area_code, src_number))
                if not dest_phone:
                    print('{}-{} is not a valid number'.format(dest_area_code, dest_number))

            else:
                print('One or more of the given area codes is invalid'.format(src_area_code))

        elif len(split_command) == 2 and split_command[0].lower() == END_CALL:
            number_parts = split_command[1].split('-')
            area_code = int(number_parts[0])
            number = int(''.join(number_parts[1:]))

            if area_code in the_network.area_codes:
                phone = None
                for i in range(len(the_network.switchboards)):
                    a_switchboard = the_network.switchboards[i]

                    for j in range(len(a_switchboard.phones)):
                        # locate the switchboard whose number matches the given source number

                        if a_switchboard.phones[j].number == number and a_switchboard.phones[j].switchboard. \
                                area_code == area_code:
                            # calls function to connect source phone to dest phone
                            phone = a_switchboard.phones[j]
                            phone.disconnect()

                if not phone:
                    print('This number is invalid')

            else:
                print('The given area code is invalid')

        elif len(split_command) >= 1 and split_command[0].lower() == DISPLAY:
            the_network.display()

        s = input('Enter command: ')
