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
TIME_LIMIT = 1
first_moves_flag = 0

class Player(PlayerInterface):

    def __init__(self, num, name, ui_status, difficulty):
        super().__init__(num, name, ui_status, difficulty)
        self.evaluation_funcs_dict = self.get_evaluation_funcs_by_dif(difficulty)
        self.import_opening_book()

    def get_move(self, board):
        print(first_moves_flag)
        if first_moves_flag == 0:
            move = Player.get_opening_move(self, board)
            if not(type(move) is bool):
                print("return move")
                return move
            else:
                globals()["first_moves_flag"] = 1
                print("set flag")
                Player.get_move(self, board)
        else:
            super().get_move(board)
            depth = 2
            best_move_val = float('-inf')
            for move in board.legal_moves:
                tmp_board = chess.Board(str(board.fen()))
                tmp_board.push(move)
                value = self.alpha_beta_pruning(tmp_board, depth, True)
                if value >= best_move_val:
                    best_move_val = value
                    best_move = move
            print(type(best_move))
            print("best_move: ", best_move)
            return best_move

            # todo: highest or lowest val dependent on color
            # return Tools.get_key_with_max_val(board_evaluations)

    def submit_move(self, move):
        super().submit_move(move)

    def print_board(self, player_name, board):
        super().print_board(player_name, board)

    # def iterative_deepening_search(self, board):
    #     start_time = time.time()
    #     end_time = start_time + TIME_LIMIT
    #     depth = 1
    #
    #     while(True):
    #         current_time = time.time()
    #         if(current_time >= end_time):
    #             break
    #
    #         print(f"depth {depth}")
    #         evaluation = self.evaluate_board_by_depth(board, depth, float('-inf'), current_time, end_time - current_time)
    #         depth+=1
    #
    #     return evaluation


    def alpha_beta_pruning(self, board, depth, player, alpha = float('-inf'), beta = float('inf')):
        if depth == 0:
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

    def get_board_value(self, board):
        return ChessTools.get_board_value(board)

    def get_attacked_figures_val(self, board):
        return ChessTools.get_attacked_pieces_value(board)

    # todo: find better name
    def compare_board_history(self, board):
        dataset = pd.read_csv(HISTORY_FILE_LOC)
        row = dataset.loc[dataset['board'] == board.fen().split(" ")[0]]
        value = row['value'].item() if len(row['value'])==1 else 0
        return value

    '''
    load an opening book in class variable `opening_book`
    raise an error if system cannot find the opening-book file
    '''
    def import_opening_book(self):
        if os.path.isfile(OPENING_BOOK_LOC):
            Player.opening_book = chess.polyglot.open_reader(OPENING_BOOK_LOC)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), OPENING_BOOK_LOC)

    '''
    get the current board and return move, as string, for this situation
    '''
    def get_opening_move(self, board):
        if not (Player.opening_book is None):
            try:
                main_entry = Player.opening_book.find(board)
                move = main_entry.move()
                return move
            except IndexError:
                return False
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), OPENING_BOOK_LOC)
