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
        self.book = chess.polyglot.open_reader("res/polyglot/Performance.bin")

    def get_move(self, board):
        super().get_move(board)

        try:
            opening_book = chess.polyglot.open_reader(OPENING_BOOK_LOC)
            move = self.get_opening_move(board, opening_book)
            if type(move) == chess.Move:
                print("move: ",move)
                return move
            else:
                start_time = int(time.time())
                end_time = start_time + self.time_limit
                return self.iterative_deepening(board, start_time, end_time)
        except (FileNotFoundError, IndexError):
            print("FileNotFoundError/IndexError")
            return self.iterative_deepening(board, start_time, end_time)

    def submit_move(self, move):
        super().submit_move(move)

    def print_board(self, player_name, board):
        super().print_board(player_name, board)
        
    def import_opening_book(self):
        '''
        load an opening book in class variable `opening_book`
        raise an error if system cannot find the opening-book file
        '''
        if os.path.isfile(OPENING_BOOK_LOC):
            print("in if")
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
                print("closed book")
                return move
            except IndexError:
                return False
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), OPENING_BOOK_LOC)


    def iterative_deepening(self, board, start_time, end_time):
        depth = 1

        overall_best_move = None
        overall_best_move_val = 0

        current_time = start_time

        while current_time < end_time:
            best_move_val = float('-inf')
            for move in board.legal_moves:
                tmp_board = chess.Board(str(board.fen()))
                tmp_board.push(move)
                # Todo: Check if board.turn works
                value = self.alpha_beta_pruning(tmp_board, depth, board.turn, end_time)
                if value >= best_move_val:
                    best_move_val = value
                    best_move = move
            if best_move_val >= overall_best_move_val:
                overall_best_move_val = best_move_val
                overall_best_move = best_move
            depth += 1
            current_time = int(time.time())

        return overall_best_move

    def alpha_beta_pruning(self, board, depth, player, end_time, alpha=float('-inf'), beta=float('inf')):
        if depth == 0 or int(time.time()) >= end_time:
            return self.evaluate_board(board)

        if player:
            best_move = float('-inf')
            for move in board.legal_moves:
                tmp_board = chess.Board(str(board.fen()))
                tmp_board.push(move)
                best_move = max(best_move, self.alpha_beta_pruning(tmp_board, depth - 1, player, alpha, beta))
                alpha = max(alpha, best_move)
                if beta <= alpha:
                    return best_move
            return best_move
        else:
            best_move = float('inf')
            for move in board.legal_moves:
                tmp_board = chess.Board(str(board.fen()))
                tmp_board.push(move)
                best_move = min(best_move, self.alpha_beta_pruning(tmp_board, depth - 1, player, alpha, beta))
                beta = min(beta, best_move)
                if beta <= alpha:
                    return best_move
            return best_move

    def evaluate_board(self, board):
        evaluation_val = 0
        for func, value in self.evaluation_funcs_dict.items():
            evaluation_val += value * func(board)
        return evaluation_val

    def get_evaluation_funcs_by_dif(self, difficulty):
        funcs_by_deg_of_dif = {
            1: {self.get_board_value: 1},
            2: {self.get_board_value: 1, self.get_attacked_figures_val: 1/2},
            3: {self.get_board_value: 1, self.get_attacked_figures_val: 1/2, self.compare_board_history: 5}
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