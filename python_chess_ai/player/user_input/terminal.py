#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Terminal implementation for user_input interface
#

from python_chess_ai.player.user_input.interface import UserInputInterface
from python_chess_ai.misc.tools import Tools

ASK_FOR_MOVE_MESSAGE = "Possible Moves: {}\nEnter your move: "
WRONG_INPUT_MESSAGE = "Given move not in legal moves. Please repeat"
PLAYER_TURN_MESSAGE = "\n\nIt's {}'s turn: "


class UserInput(UserInputInterface):
    def __init__(self):
        super().__init__()

    def print_board(self, player_name, board):
        super().print_board(player_name, board)
        print(PLAYER_TURN_MESSAGE.format(player_name))
        print("\n---------------")
        print(board)
        print("---------------\n")

    def get_move(self, legal_moves):
        super().get_move(legal_moves)
        input_msg = ASK_FOR_MOVE_MESSAGE.format(legal_moves)
        move = Tools.check_legal_input_string(legal_moves,input_msg, WRONG_INPUT_MESSAGE)
        return move
