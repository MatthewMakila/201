"""
File:    phone.py
Author:  Matthew Makila
Date:    11/25/2020
Section: 44
E-mail:  mmakila1@umbc.edu
Description:
  This code hosts the phone object. Each phone object is attached to its host switchboard and retains a particular
  number. The phone may be connected to another phone either locally or through various switchboards (through a
  recursive call) so long as the connection exists. The phone also has a method to disconnect itself and the other
  phone by altering an attribute of its class.

    Phone Class Starter Code

    This code defines the basic functionality that you need from a phone.
    When these functions are called they should communicate with the
    switchboards to find a path
"""


class Phone:
    def __init__(self, number, switchboard):
        """
        :param number: the phone number without area code
        :param switchboard: the switchboard to which the number is attached.
        """
        self.number = number
        self.switchboard = switchboard
        # var to track which phone this one is connected to
        self.other_phone_call = None

    def connect(self, other_phone):
        """
        :param other_phone: the other phone object to connect to
        :return: True/False depending on if call can connect
        """

        other_area_code = other_phone.switchboard.area_code
        other_phone_number = other_phone.number

        # check if either of the two phones is on a call already, if either is, do not let connect
        if self.other_phone_call or other_phone.other_phone_call:
            print('One of these phones is in a call!')
            return False

        # then check if both phones have the same area code (IF they do, they can connect LOCALLY)
        if self.switchboard.area_code == other_area_code:

            if self.number == other_phone_number:
                # exact same phone nums, cannot connect
                print('These are the exact same numbers, no connection available')
                return False
            else:
                # connect call locally
                # self.is_connected = True
                self.other_phone_call = other_phone
                other_phone.other_phone_call = self
                print('Phones connected locally!')
                return True

        else:
            # call must connect through other switchboards (Recursive function is called)
            non_local_call = self.switchboard.connect_call(other_area_code, [], [])

            if non_local_call:  # if we can make a non-local call, connect the phones
                self.other_phone_call = other_phone
                other_phone.other_phone_call = self
                return True
            else:
                return False

    def disconnect(self):
        """
        This function should return the connection status to disconnected.  You need
        to use new members of this class to determine how the phone is connected to
        the other phone.

        You should also make sure to disconnect the other phone on the other end of the line.
        :return: **depends on your implementation**
        """
        if self.other_phone_call:
            # This will clear the other phone's line and then this phone's line: they will be available to call again
            self.other_phone_call.other_phone_call = None
            self.other_phone_call = None
            print('Hanging up...\nConnection Terminated.')
        # if this phone does not have another call, print failure to disconnect (since nothing to disconnect from)
        else:
            print("Unable to disconnect.")
