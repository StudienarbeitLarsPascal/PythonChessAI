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
from player.user_input import terminal, gui
import chess
import chess.polyglot
import pandas as pd
import time
import os
import errno

HISTORY_FILE_LOC = "res/history.csv"
OPENING_BOOK_LOC = "res/polyglot/Performance.bin"


class Player(PlayerInterface):

    def __init__(self, num, name, ui_status, difficulty):
        super().__init__(num, name, ui_status, difficulty)
        self.evaluation_funcs_dict = self.get_evaluation_funcs_by_dif(difficulty)
        self.time_limit = self.get_timeout_by_dif(difficulty)
        self.ui=self.get_ui_type(ui_status).UserInput()

    def get_move(self, board):
        super().get_move(board)

        try:
            opening_book = self.import_opening_book()
            move = self.get_opening_move(board, opening_book)
            if type(move) == chess.Move:
                return move
            else:
                start_time = int(time.time())
                end_time = start_time + self.time_limit
                return self.iterative_deepening(board, start_time, end_time)
        except (FileNotFoundError, IndexError):
            return self.iterative_deepening(board, start_time, end_time)

    def submit_move(self, move):
        super().submit_move(move)

    def print_board(self, player_name, board):
        super().print_board(player_name, board)
        self.ui.print_board(player_name, board)
        
    def import_opening_book(self):
        '''
        load an opening book in class variable `opening_book`
        raise an error if system cannot find the opening-book file
        '''
        if os.path.isfile(OPENING_BOOK_LOC):
            return chess.polyglot.open_reader(OPENING_BOOK_LOC)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), OPENING_BOOK_LOC)

    def get_opening_move(self, board, opening_book):
        '''
        get the current board and return move, as string, for this situation
        '''
        if not (opening_book is None):
            try:
                main_entry = opening_book.find(board)
                move = main_entry.move()
                opening_book.close()
                return move
            except IndexError:
                return False
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), OPENING_BOOK_LOC)


    def iterative_deepening(self, board, start_time, end_time):
        depth = 1

        player = bool(board.turn)
        print(player)
        current_time = start_time
        overall_best_move = list(board.legal_moves)[0]

        while current_time < end_time:
            best_value = float('-inf')
            for move in board.legal_moves:
                tmp_board = chess.Board(str(board.fen()))
                tmp_board.push(move)
                value = self.min_value(tmp_board, player, float('-inf'), float('inf'), depth - 1)
                if value >= best_value:
                    best_value = value
                    best_move = move
            overall_best_move = best_move
            depth += 1
            current_time = int(time.time())

        return overall_best_move

    def min_value(self, board, player, alpha, beta, depth):
        #todo: cutoff_test
        if depth == 0:
            return self.evaluate_board(board, player)

        v = float('inf')
        for move in board.legal_moves:
            tmp_board = chess.Board(str(board.fen()))
            tmp_board.push(move)
            v = min(v, self.max_value(tmp_board, player, alpha, beta, depth -1))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    def max_value(self, board, player, alpha, beta, depth):
        #todo: cutoff_test
        if depth == 0:
            return self.evaluate_board(board, player)

        v = float('-inf')
        for move in board.legal_moves:
            tmp_board = chess.Board(str(board.fen()))
            tmp_board.push(move)
            v = max(v, self.min_value(tmp_board, player, alpha, beta, depth -1))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def evaluate_board(self, board, player):
        evaluation_val = 0
        for func, value in self.evaluation_funcs_dict.items():
            evaluation_val += value * func(board)
        return evaluation_val if player else -1*evaluation_val

    def get_evaluation_funcs_by_dif(self, difficulty):
        funcs_by_deg_of_dif = {
            1: {self.get_board_value: 1},
            2: {self.get_board_value: 1, self.get_attacked_figures_val: 1/4},
            3: {self.get_board_value: 1, self.get_attacked_figures_val: 1/4, self.compare_board_history: 3}
        }
        return funcs_by_deg_of_dif.get(difficulty)

    @staticmethod
    def get_timeout_by_dif(difficulty):
        time_limit = {
            1: 5,
            2: 10,
            3: 20
        }
        return time_limit.get(difficulty)

    @staticmethod
    def get_board_value(board):
        return ChessTools.get_board_value(board)

    @staticmethod
    def get_attacked_figures_val(board):
        return ChessTools.get_attacked_pieces_value(board)

    @staticmethod
    def compare_board_history(board):
        dataset = pd.read_csv(HISTORY_FILE_LOC)
        row = dataset.loc[dataset['board'] == board.fen().split(" ")[0]]
        value = row['value'].item() if len(row['value']) == 1 else 0
        return value

    def get_ui_type(self, ui_status):
        return {
            0: terminal,
            1: gui
        }[ui_status]