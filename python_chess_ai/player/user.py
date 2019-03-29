#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Implementation of player interface for user given input
#

from player.interface import PlayerInterface
from player.user_input import terminal, gui
import misc.ai_evaluation_lib  as EvaluationLib

import chess

class Player(PlayerInterface):
    def __init__(self, num, name, ui_status, difficulty=None):
        super().__init__(num, name, ui_status, difficulty)
        self.ui=self.get_ui_type(ui_status).UserInput()

    def print_board(self, player_name, board):
        super().print_board(player_name, board)
        self.ui.print_board(player_name, board)

    def get_move(self, board):
        super().get_move(board)
        # Todo: Check for surrender
        legal_moves = list(map(board.uci, board.legal_moves))
        move = None
        while move not in legal_moves:
            move = self.ui.get_move(legal_moves)
        return chess.Move.from_uci(move)

    def submit_move(self, move):
        super().submit_move(move)
