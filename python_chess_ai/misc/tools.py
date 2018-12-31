#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# This file provides different basic functions needed in several parts of this program
#

WRONG_INPUT_MESSAGE = "Wrong input given. Please repeat."


class Tools():
    @staticmethod
    def check_legal_input_string(legal_array, ask_for_input_msg, wrong_input_msg=WRONG_INPUT_MESSAGE):
        user_input = input(ask_for_input_msg)
        while user_input not in legal_array:
            print(wrong_input_msg)
            user_input = input(ask_for_input_msg)
        return user_input

    @staticmethod
    def check_legal_input_int(legal_array, ask_for_input_msg, wrong_input_msg=WRONG_INPUT_MESSAGE):
        user_input = input(ask_for_input_msg)
        while not (user_input.isdigit() and int(user_input) in legal_array):
            print(wrong_input_msg)
            user_input = input(ask_for_input_msg)
        return int(user_input)