#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Terminal implementation for settings interface
#
PLAYER_TYPE_INPUT_MESSAGE = "\nPlease enter Player Type for Player {}. \n (1 for User, 2 for AI, 3 for API, 4 for Dummy) \n"
PLAYER_NAME_INPUT_MESSAGE = "\nPlease enter Player Name for Player {}. \n"
DIFFICULTY_INPUT_MESSAGE = "\nPlease enter difficulty for Player {}. \n (1 for easy, 2 for normal, 3 for hard) \n"

PLAYER_TYPE_MIN = 1
PLAYER_TYPE_MAX = 4
DIFFICULTY_MIN = 1
DIFFICULTY_MAX = 3

from python_chess_ai.player import ai, api, dummy, user
from python_chess_ai.settings.interface import SettingsInterface
from python_chess_ai.misc.tools import Tools


class Settings(SettingsInterface):

    def get_player_type(self, player_num):
        super().get_player_type(player_num)
        legal_range = range(PLAYER_TYPE_MIN, PLAYER_TYPE_MAX + 1)
        input_msg = PLAYER_TYPE_INPUT_MESSAGE.format(player_num)
        input_player_type = Tools.check_legal_input_int(legal_range, input_msg)
        return input_player_type

    def get_player_name(self, player_num):
        super().get_player_name(player_num)
        return input(PLAYER_NAME_INPUT_MESSAGE.format(player_num))

    def get_difficulty(self, player_num):
        super().get_difficulty(player_num)
        legal_range = range(DIFFICULTY_MIN, DIFFICULTY_MAX + 1)
        input_msg = DIFFICULTY_INPUT_MESSAGE.format(player_num)
        input_difficulty = Tools.check_legal_input_int(legal_range, input_msg)
        return input_difficulty
