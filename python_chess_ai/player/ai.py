#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Implementation of player interface for calculated moves through AI
#

from player.interface import PlayerInterface
import misc.tools as Tools
import misc.chess_tools as ChessTools
import chess


class Player(PlayerInterface):
    def __init__(self, num, name, ui_status, difficulty):
        super().__init__(num, name, ui_status, difficulty)
        self.evaluation_funcs = self.get_evaluation_funcs_by_dif(difficulty)

    def get_move(self, board):
        super().get_move(board)

        board_evaluations = dict()
        for move in board.legal_moves:
            board_evaluations[move] = self.evaluate_move(board, move)

        print(board_evaluations)
        print(board_evaluations.values())

        # todo: highest or lowest val dependent on color
        return Tools.get_key_with_max_val(board_evaluations)

    def submit_move(self, move):
        super().submit_move(move)

    def print_board(self, player_name, board):
        super().print_board(player_name, board)

    def evaluate_move(self, board, move):
        # todo: implement iterative deepening for possibles move

        tmp_board = chess.Board(str(board.fen()))
        tmp_board.push(move)

        return self.evaluate_board(tmp_board)

    def evaluate_board(self, board):
        evaluation_val = 0
        for func in self.evaluation_funcs:
            evaluation_val += func(board)
        return evaluation_val

    def get_evaluation_funcs_by_dif(self, difficulty):
        funcs_by_deg_of_dif = {
            1: [self.get_board_value],
            2: [self.get_board_value, self.get_attacked_figures_val],
            3: [self.get_board_value, self.get_attacked_figures_val, self.compare_board_history]
        }
        return funcs_by_deg_of_dif.get(difficulty)

    def get_board_value(self, board):
        return ChessTools.get_board_value(board)

    def get_attacked_figures_val(self, board):
        return ChessTools.get_attacked_pieces_value(board)

    # todo: find better name
    def compare_board_history(self, board):
        # todo: implement
        return 0

