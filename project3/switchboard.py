"""
File:    switchboard.py
Author:  Matthew Makila
Date:    11/25/2020
Section: 44
E-mail:  mmakila1@umbc.edu
Description:
  This code creates hosts the switchboard object. The switchboard may have multiple phones added to it and may be
  connected to other switchboards via its trunk_connection method and list. Calls that are not local may
  be routed through a particular source switchboard with the recursive call connect_call.

    Switchboard class

"""

from phone import Phone


class Switchboard:
    def __init__(self, area_code):
        """
        :param area_code: the area code to which the switchboard will be associated.
        """
        self.area_code = area_code
        self.trunk_lines = []  # make a list or dict for these?
        # actual list of phone objects attached to each switchboard
        self.phones = []
        # just a list to check the actual numbers passed from network driver
        self.phone_nums = []

    def add_phone(self, phone_number):
        """
        This function should add a local phone connection by creating a phone object
        and storing it in this class.  How you do that is up to you.

        :param phone_number: phone number without area code
        :return: depends on implementation / None
        """
        if phone_number not in self.phone_nums:
            # create phone object and adds to the phones connected to this particular board
            self.phone_nums.append(phone_number)
            self.phones.append(Phone(phone_number, self))

        else:
            print('That number is already attached to that area code!')

    def add_trunk_connection(self, switchboard):
        """
        Connect the switchboard (self) to the switchboard (switchboard)

        :param switchboard: should be either the area code or switchboard object to connect.
        :return: success/failure, None, or it's up to you
        """
        # add the new switchboard as a trunk-line for this switchboard
        if switchboard not in self.trunk_lines:
            self.trunk_lines.append(switchboard)

        else:
            print('{} is already connected to {}'.format(self.area_code, switchboard.area_code))

    def connect_call(self, dest_code, new_switches, previous_codes):
        """
        This must be a recursive function.

        :param dest_code: the area code to which the destination phone belongs
        :para dest_number: the phone number of the destination phone without area code.
        :param new_switches: By default, the source area code. Keeps track of new area codes searched recursively
        :param previous_codes: you must keep track of the previously tracked codes
        :return: Depends on your implementation, possibly the path to the destination phone.
        """
        # NEW CODES IS REALLY NEW SWITCHBOARDS
        
        """print('searching ...')
        print('new switches:', new_switches)
        print('prev codes:', previous_codes)
        print('dest:', dest_code)"""

        # base cases
        if not previous_codes:
            for i in range(len(self.trunk_lines)):
                new_switch = self.trunk_lines[i]
                new_switches.append(new_switch)
                previous_codes.append(new_switches[i].area_code)

            # prevent new switches from searching back for the source switchboard
            previous_codes.append(self.area_code)
            # call function again: updated switches to check for more trunk lines & more previous area codes
            self.connect_call(dest_code, new_switches, previous_codes)

        # if the destination code is found in any of the previously checked area codes, connection can be made
        if dest_code in previous_codes:
            return True

        if not new_switches:  # no more connections, no dest_code found, returns false
            return False

        # recursive cases
        if new_switches:
            # old_switches tracks which switches were in the list before more are added
            old_switches = len(new_switches)

            for i in range(len(new_switches)):
                a_switch = new_switches[i]

                for j in range(len(a_switch.trunk_lines)):
                    # do not put duplicates into previously checked area codes (prevents infinite recur)
                    if a_switch.trunk_lines[j].area_code not in previous_codes:  
                        previous_codes.append(a_switch.trunk_lines[j].area_code)
                        new_switches.append(a_switch.trunk_lines[j])
            # remove all but new switches to clean out list & allow list to become empty if no more paths exist
            for i in range(old_switches):
                new_switches.remove(new_switches[0])

            self.connect_call(dest_code, new_switches, previous_codes)
