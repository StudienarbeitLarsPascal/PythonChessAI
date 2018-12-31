#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Implementation of player interface for user given input
#

from python_chess_ai.player.interface import PlayerInterface
from python_chess_ai.player.user_input import terminal, gui
import python_chess_ai.misc.chess_tools  as chess_tools

import chess


class Player(PlayerInterface):
    def __init__(self, num, name, ui_status, difficulty=None):
        super().__init__(num, name, ui_status, difficulty)
        self.ui=self.uiSwitcher.get(ui_status).UserInput()

    def print_board(self, player_name, board):
        super().print_board(player_name, board)
        self.ui.print_board(player_name, board)

    def get_move(self, board):
        super().get_move(board)
        legal_moves = chess_tools.get_legal_moves_uci(board)
        move = None
        while move not in legal_moves:
            move = self.ui.get_move(legal_moves)
        return chess.Move.from_uci(move)

    def submit_move(self, move):
        super().submit_move(move)

    uiSwitcher = {
        0: terminal,
        1: gui
    }
