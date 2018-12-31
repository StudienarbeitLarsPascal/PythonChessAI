#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Implementation of player interface for random moves (dummy)
#

from python_chess_ai.player.interface import PlayerInterface

import random


class Player(PlayerInterface):
    def __init__(self, num, name, ui_status, difficulty=None):
        super().__init__(num, name, ui_status, difficulty)

    def get_move(self, board):
        super().get_move(board)
        return random.choice(list(board.legal_moves))

    def submit_move(self, turn):
        super().submit_move(turn)

    def print_board(self, player_name, board):
        super().print_board(player_name, board)
        print(board)