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
import misc.ai_evaluation_lib as EvaluationLib
from functools import lru_cache
from player.user_input import terminal, gui
import chess
import chess.polyglot
import time
import os
import errno

OPENING_BOOK_LOC = "res/polyglot/Performance.bin"

BOARD_VALUE_FACTOR = 50
ATTACKED_PIECES_FACTOR = 10
BOARD_POSITIONS_FACTOR = 10
KING_SAFETY_FACTOR = 10
OPP_KING_SAFETY_FACTOR = 4
MOBILITY_FACTOR = 4
HISTORY_FACTOR = 2

class Player(PlayerInterface):

    def __init__(self, num, name, ui_status, difficulty, board_value_fact = BOARD_VALUE_FACTOR, attacked_pieces_fact = ATTACKED_PIECES_FACTOR, board_positions_fact = BOARD_POSITIONS_FACTOR, king_safety_fact = KING_SAFETY_FACTOR, opp_king_safety_fact = OPP_KING_SAFETY_FACTOR, mobility_fact = MOBILITY_FACTOR, history_fact = HISTORY_FACTOR):
        super().__init__(num, name, ui_status, difficulty)
        
        self.board_value_fact = board_value_fact
        self.attacked_pieces_fact = attacked_pieces_fact
        self.board_positions_fact = board_positions_fact
        self.king_safety_fact = king_safety_fact
        self.opp_king_safety_fact = opp_king_safety_fact
        self.mobility_fact = mobility_fact
        self.history_fact = history_fact

        self.opening_book = self.import_opening_book(OPENING_BOOK_LOC)
        self.evaluation_funcs_dict = self.get_evaluation_funcs_by_dif(difficulty)
        self.time_limit = self.get_timeout_by_dif(difficulty)
        
        self.ui=self.get_ui_type(ui_status).UserInput()

    def get_move(self, board):
        super().get_move(board)
        
        if board.fullmove_number <= 14:
            move = self.get_opening_move(board, self.opening_book)
            if not move is None:
                return move
        
        white_material = EvaluationLib.get_value_by_color(board, chess.WHITE, False)
        black_material = EvaluationLib.get_value_by_color(board, chess.BLACK, False)
        if white_material <= 13 and black_material <= 13:
            # Todo: return Finishing strategy
            pass
            
        return self.iterative_deepening(board)

    def submit_move(self, move):
        super().submit_move(move)

    def print_board(self, player_name, board):
        super().print_board(player_name, board)
        self.ui.print_board(player_name, board)


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
                return None
        else:
            return None


    def iterative_deepening(self, board):
        depth = 1

        start_time = int(time.time())
        end_time = start_time + self.time_limit
        current_time = start_time

        player = bool(board.turn)

        legal_moves = list(board.legal_moves)

        while current_time < end_time:
            print(depth)
            move_val_dict = {}

            best_value = float('-inf')
            best_move = legal_moves[0]

            for move in legal_moves:
                tmp_board = chess.Board(str(board.fen()))
                tmp_board.push(move)
                value = self.min_value(str(tmp_board.fen()), player, float('-inf'), float('inf'), depth - 1, end_time)
                move_val_dict[move] = value
                if value >= best_value:
                    best_value = value
                    best_move = move
            
            legal_moves.sort(key=move_val_dict.get, reverse=True)
            depth += 1
            current_time = int(time.time())

        tmp_board = chess.Board(str(board.fen()))
        tmp_board.push(move)

        print("Material: {} * {} = {}".format(EvaluationLib.get_board_value(tmp_board, player), self.board_value_fact, EvaluationLib.get_board_value(tmp_board, player)*self.board_value_fact ))
        print("Attacked: {} * {} = {}".format(EvaluationLib.get_attacked_pieces_value(tmp_board, player), self.attacked_pieces_fact, EvaluationLib.get_attacked_pieces_value(tmp_board, player)*self.attacked_pieces_fact ))
        print("Position: {} * {} = {}".format(EvaluationLib.get_board_positions_value(tmp_board, player), self.board_positions_fact, EvaluationLib.get_board_positions_value(tmp_board, player)*self.board_positions_fact ))
        print("KingZone: {} * {} = {}".format(EvaluationLib.calculate_king_zone_safety(tmp_board, player), self.king_safety_fact, EvaluationLib.calculate_king_zone_safety(tmp_board, player)*self.king_safety_fact ))
        print("OppKZone: {} * {} = {}".format(EvaluationLib.calculate_opp_king_zone_safety(tmp_board, player), self.opp_king_safety_fact, EvaluationLib.calculate_opp_king_zone_safety(tmp_board, player)*self.opp_king_safety_fact ))
        print("Mobility: {} * {} = {}".format(EvaluationLib.calculate_mobility_value(tmp_board, player), self.mobility_fact, EvaluationLib.calculate_mobility_value(tmp_board, player)*self.mobility_fact ))
        print("History:  {} * {} = {}".format(EvaluationLib.get_board_value_by_history(tmp_board, player), self.history_fact, EvaluationLib.get_board_value_by_history(tmp_board, player)*self.history_fact ))
        
        print(self.evaluate_board(tmp_board, player))
        print(best_move)
        return best_move

    @lru_cache(maxsize=256)
    def min_value(self, board_fen, player, alpha, beta, depth, time_limit):
        board = chess.Board(board_fen)
        v = float('inf')

        if board.is_game_over() or depth == 0:
            return self.evaluate_board(board, player)
        if int(time.time()) >= time_limit:
            return float("-inf")

        for move in board.legal_moves:
            tmp_board = chess.Board(board_fen)
            tmp_board.push(move)
            v = min(v, self.max_value(str(tmp_board.fen()), player, alpha, beta, depth -1, time_limit))
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    @lru_cache(maxsize=256)
    def max_value(self, board_fen, player, alpha, beta, depth, time_limit):
        board = chess.Board(board_fen)
        v = float('-inf')

        if board.is_game_over() or depth == 0:
            return self.evaluate_board(board, player)
        if int(time.time()) >= time_limit:
            return float("inf")

        for move in board.legal_moves:
            tmp_board = chess.Board(board_fen)
            tmp_board.push(move)
            v = max(v, self.min_value(str(tmp_board.fen()), player, alpha, beta, depth -1, time_limit))
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def evaluate_board(self, board, player):
        player_color = chess.WHITE if player else chess.BLACK
        evaluation_val = 0
        for func, value in self.evaluation_funcs_dict.items():
            evaluation_val = evaluation_val + value * func(board, player_color)
        return evaluation_val

    def get_evaluation_funcs_by_dif(self, difficulty):
        funcs_by_deg_of_dif = {
            1: {EvaluationLib.get_board_value: self.board_value_fact},
            2: {EvaluationLib.get_board_value: self.board_value_fact, EvaluationLib.get_attacked_pieces_value: self.attacked_pieces_fact},
            3: {EvaluationLib.get_board_value: self.board_value_fact, EvaluationLib.get_attacked_pieces_value: self.attacked_pieces_fact, EvaluationLib.get_board_positions_value: self.board_positions_fact, EvaluationLib.calculate_king_zone_safety: self.king_safety_fact, EvaluationLib.calculate_opp_king_zone_safety: self.opp_king_safety_fact, EvaluationLib.calculate_mobility_value: self.mobility_fact, EvaluationLib.get_board_value_by_history: self.history_fact}
        }
        return funcs_by_deg_of_dif.get(difficulty)

    @staticmethod
    def get_timeout_by_dif(difficulty):
        time_limit = {
            1: 5,
            2: 10,
            3: 30
        }
        return time_limit.get(difficulty)

    def import_opening_book(self, book_location):
        '''
        load an opening book in class variable `opening_book`
        raise an error if system cannot find the opening-book file
        '''
        if os.path.isfile(book_location):
            return chess.polyglot.open_reader(OPENING_BOOK_LOC)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), OPENING_BOOK_LOC)