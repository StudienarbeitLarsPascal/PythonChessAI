#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# GUI implementation for user_input interface
#
from player.user_input.interface import UserInputInterface


class UserInput(UserInputInterface):
    def __init__(self):
        super().__init__()

    def print_board(self, player_name, board):
        super().print_board(player_name, board)

    def get_move(self, legal_moves):
        super().get_move(legal_moves)