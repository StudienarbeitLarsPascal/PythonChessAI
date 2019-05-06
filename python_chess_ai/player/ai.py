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
import chess.syzygy
import time
import os
import errno

OPENING_BOOK_LOC = "res/polyglot/Performance.bin"
SYZYGY_LOC = "res/syzygy"

MAX_BOARD_VALUE = float("inf")

MAX_DEPTH_START = 4
BOARD_VALUE_FACTOR_START = 50
ATTACKED_PIECES_FACTOR_START = 10
BOARD_POSITIONS_FACTOR_START = 50
OPP_BOARD_POSITIONS_FACTOR_START = 50
KING_SAFETY_FACTOR_START = 5
OPP_KING_SAFETY_FACTOR_START = 5
MOBILITY_FACTOR_START = 4
HISTORY_FACTOR_START = 1

MAX_DEPTH_MID = 4
BOARD_VALUE_FACTOR_MID = 50
ATTACKED_PIECES_FACTOR_MID = 10
BOARD_POSITIONS_FACTOR_MID = 25
OPP_BOARD_POSITIONS_FACTOR_MID = 25
KING_SAFETY_FACTOR_MID = 5
OPP_KING_SAFETY_FACTOR_MID = 5
MOBILITY_FACTOR_MID = 4
HISTORY_FACTOR_MID = 0

MAX_DEPTH_END = 10
BOARD_VALUE_FACTOR_END = 50
ATTACKED_PIECES_FACTOR_END = 20
BOARD_POSITIONS_FACTOR_END = 10
OPP_BOARD_POSITIONS_FACTOR_END = 10
KING_SAFETY_FACTOR_END = 5
OPP_KING_SAFETY_FACTOR_END = 10
MOBILITY_FACTOR_END = 10
HISTORY_FACTOR_END = 5


OPENING_MAX_FULLMOVE_NUM = 6
FINISHING_MAX_PIECES = 13

class Player(PlayerInterface):

    def __init__(self, num, name, ui_status, difficulty, 
        board_value_fact_start = BOARD_VALUE_FACTOR_START, attacked_pieces_fact_start = ATTACKED_PIECES_FACTOR_START, board_positions_fact_start = BOARD_POSITIONS_FACTOR_START, opp_board_positions_fact_start = OPP_BOARD_POSITIONS_FACTOR_START, king_safety_fact_start = KING_SAFETY_FACTOR_START, opp_king_safety_fact_start = OPP_KING_SAFETY_FACTOR_START, mobility_fact_start = MOBILITY_FACTOR_START, history_fact_start = HISTORY_FACTOR_START, max_depth_start = MAX_DEPTH_START,
        board_value_fact_mid = BOARD_VALUE_FACTOR_MID, attacked_pieces_fact_mid = ATTACKED_PIECES_FACTOR_MID, board_positions_fact_mid = BOARD_POSITIONS_FACTOR_MID, opp_board_positions_fact_mid = OPP_BOARD_POSITIONS_FACTOR_MID, king_safety_fact_mid = KING_SAFETY_FACTOR_MID, opp_king_safety_fact_mid = OPP_KING_SAFETY_FACTOR_MID, mobility_fact_mid = MOBILITY_FACTOR_MID, history_fact_mid = HISTORY_FACTOR_MID, max_depth_mid = MAX_DEPTH_MID,
        board_value_fact_end = BOARD_VALUE_FACTOR_END, attacked_pieces_fact_end = ATTACKED_PIECES_FACTOR_END, board_positions_fact_end = BOARD_POSITIONS_FACTOR_END, opp_board_positions_fact_end = OPP_BOARD_POSITIONS_FACTOR_END, king_safety_fact_end = KING_SAFETY_FACTOR_END, opp_king_safety_fact_end = OPP_KING_SAFETY_FACTOR_END, mobility_fact_end = MOBILITY_FACTOR_END, history_fact_end = HISTORY_FACTOR_END, max_depth_end = MAX_DEPTH_END):
        
        super().__init__(num, name, ui_status, difficulty)
        
        self.board_value_fact_start = board_value_fact_start
        self.attacked_pieces_fact_start = attacked_pieces_fact_start
        self.board_positions_fact_start = board_positions_fact_start
        self.opp_board_positions_fact_start = opp_board_positions_fact_start
        self.king_safety_fact_start = king_safety_fact_start
        self.opp_king_safety_fact_start = opp_king_safety_fact_start
        self.mobility_fact_start = mobility_fact_start
        self.history_fact_start = history_fact_start
        self.max_depth_start = max_depth_start

        self.board_value_fact_mid = board_value_fact_mid
        self.attacked_pieces_fact_mid = attacked_pieces_fact_mid
        self.board_positions_fact_mid = board_positions_fact_mid
        self.opp_board_positions_fact_mid = opp_board_positions_fact_mid
        self.king_safety_fact_mid = king_safety_fact_mid
        self.opp_king_safety_fact_mid = opp_king_safety_fact_mid
        self.mobility_fact_mid = mobility_fact_mid
        self.history_fact_mid = history_fact_mid
        self.max_depth_mid = max_depth_mid

        self.board_value_fact_end = board_value_fact_end
        self.attacked_pieces_fact_end = attacked_pieces_fact_end
        self.board_positions_fact_end = board_positions_fact_end
        self.opp_board_positions_fact_end = opp_board_positions_fact_end
        self.king_safety_fact_end = king_safety_fact_end
        self.opp_king_safety_fact_end = opp_king_safety_fact_end
        self.mobility_fact_end = mobility_fact_end
        self.history_fact_end = history_fact_end
        self.max_depth_end = max_depth_end

        self.difficulty = difficulty
        self.evaluation_funcs_dict = self.get_evaluation_funcs_by_dif(2, self.difficulty)

        self.opening_book = self.import_opening_book(OPENING_BOOK_LOC)
        self.syzygy = self.import_syzygy(SYZYGY_LOC)
        
        self.time_limit = self.get_timeout_by_dif(difficulty)
        

    def get_move(self, board):
        super().get_move(board)

       
        self.game_status = 2
        evaluation_func = self.evaluate_board
        if board.fullmove_number <= OPENING_MAX_FULLMOVE_NUM:
            self.game_status = 1
            move = self.get_opening_move(board, self.opening_book)
            if not move is None:
                return move
        
        white_material = EvaluationLib.get_value_by_color(board, chess.WHITE, False)
        black_material = EvaluationLib.get_value_by_color(board, chess.BLACK, False)
        if white_material <= FINISHING_MAX_PIECES and black_material <= FINISHING_MAX_PIECES:
            self.game_status = 3
            
        pieces_counter_white = sum(len(board.pieces(piece_type, chess.WHITE)) for piece_type in chess.PIECE_TYPES)
        pieces_counter_black = sum(len(board.pieces(piece_type, chess.BLACK)) for piece_type in chess.PIECE_TYPES)
        
        if pieces_counter_white + pieces_counter_black <= 5:
            board.evaluation_func = self.get_dtz_value
            evaluation_func = self.get_dtz_value
        
        self.evaluation_funcs_dict = self.get_evaluation_funcs_by_dif(self.game_status, self.difficulty)

        return self.iterative_deepening(board, self.get_max_depth_by_game_status(self.game_status), evaluation_func)

    def submit_move(self, move):
        super().submit_move(move)


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

    def get_dtz_value(self, board, player):
        player_factor = 1 if board.turn == player else -1
        try:
            return player_factor * self.syzygy.probe_dtz(board)
        except KeyError:
            return float('-inf')


    def iterative_deepening(self, board, max_depth, evaluation_func):
        depth = 1
        self.counter=0

        start_time = int(time.time())
        end_time = start_time + self.time_limit
        current_time = start_time

        player = bool(board.turn)
        self.best_possible_result = self.get_best_possible_result(board, player)

        legal_moves = list(board.legal_moves)
        while current_time < end_time and depth <= max_depth:
            move_val_dict = {}

            best_value = float('-inf')
            best_move = legal_moves[0]

            for move in legal_moves:
                tmp_board = chess.Board(str(board.fen()))
                tmp_board.push(move)
                value = self.min_value(str(tmp_board.fen()), player, float('-inf'), float('inf'), depth - 1, end_time, evaluation_func)
                if value is False:
                    value = float('-inf')
                move_val_dict[move] = value
                if value == MAX_BOARD_VALUE:
                    return move
                if value > best_value:
                    best_value = value
                    best_move = move
            
            legal_moves.sort(key=move_val_dict.get, reverse=True)
            depth *= 2
            current_time = int(time.time())

        return best_move

    @lru_cache(maxsize=256)
    def min_value(self, board_fen, player, alpha, beta, depth, time_limit, evaluation_func):
        board = chess.Board(board_fen)
        v = float('inf')

        if board.is_game_over() or depth == 0:
            return evaluation_func(board, player)
        if int(time.time()) >= time_limit:
            return False

        for move in board.legal_moves:
            tmp_board = chess.Board(board_fen)
            tmp_board.push(move)
            
            deeper_val = self.max_value(str(tmp_board.fen()), player, alpha, beta, depth -1, time_limit, evaluation_func)
            if deeper_val is False:
                return False            
            v = min(v, deeper_val)  
            
            if v <= alpha:
                return v
            beta = min(beta, v)
        return v

    @lru_cache(maxsize=256)
    def max_value(self, board_fen, player, alpha, beta, depth, time_limit, evaluation_func):
        board = chess.Board(board_fen)
        v = float('-inf')

        if board.is_game_over() or depth == 0:
            return evaluation_func(board, player)
        if int(time.time()) >= time_limit:
            return False

        for move in board.legal_moves:
            tmp_board = chess.Board(board_fen)
            tmp_board.push(move)
            
            deeper_val = self.min_value(str(tmp_board.fen()), player, alpha, beta, depth -1, time_limit, evaluation_func)
            if deeper_val is False:
                return False
            v = max(v, deeper_val)
            
            if v >= beta:
                return v
            alpha = max(alpha, v)
        return v

    def evaluate_board(self, board, player):
        player_color = chess.WHITE if player else chess.BLACK
        self.counter+=1

        if board.is_game_over():
            result = Tools.get_board_result(board)
            if result is self.best_possible_result:
                return MAX_BOARD_VALUE
            if result is self.best_possible_result * -1:
                return -1 * MAX_BOARD_VALUE

        evaluation_val = 0
        for func, value in self.evaluation_funcs_dict.items():
            if value > 0:
                evaluation_val = evaluation_val + value * func(board, player_color)
        return evaluation_val

    def get_best_possible_result(self, board, player):
        if player and board.has_insufficient_material(chess.WHITE):
            return 0
        if not player and board.has_insufficient_material(chess.BLACK):
            return 0
        if player and not board.has_insufficient_material(chess.WHITE):
            return 1
        if not player and not board.has_insufficient_material(chess.BLACK):
            return -1

    def get_evaluation_funcs_by_dif(self, game_status, difficulty):
        factor_dict = self.get_factors_by_game_status(game_status)
        funcs_by_deg_of_dif = {
            1: {EvaluationLib.get_board_value: factor_dict.get("board_value")},
            2: {EvaluationLib.get_board_value: factor_dict.get("board_value"), EvaluationLib.get_attacked_pieces_value: factor_dict.get("attacked_pieces"), EvaluationLib.get_board_value_by_history: factor_dict.get("history")},
            3: {EvaluationLib.get_board_value: factor_dict.get("board_value"), EvaluationLib.get_attacked_pieces_value: factor_dict.get("attacked_pieces"), EvaluationLib.get_board_positions_value: factor_dict.get("board_position"), EvaluationLib.get_opp_board_positions_value: factor_dict.get("opp_board_position"), EvaluationLib.calculate_king_zone_safety: factor_dict.get("king_safety"), EvaluationLib.calculate_opp_king_zone_safety: factor_dict.get("opp_king_safety"), EvaluationLib.calculate_mobility_value: factor_dict.get("mobility")}
        }
        return funcs_by_deg_of_dif.get(difficulty)

    @staticmethod
    def get_timeout_by_dif(difficulty):
        time_limit = {
            1: 10,
            2: 20,
            3: 45
        }
        return time_limit.get(difficulty)

    def get_factors_by_game_status(self, game_status):
        return {
            1: {
                "board_value": self.board_value_fact_start,
                "attacked_pieces": self.attacked_pieces_fact_start,
                "board_position": self.board_positions_fact_start,
                "opp_board_position": self.opp_board_positions_fact_start,
                "king_safety": self.king_safety_fact_start,
                "opp_king_safety": self.opp_king_safety_fact_start,
                "mobility": self.mobility_fact_start,
                "history": self.history_fact_start
            },
            2: {
                "board_value": self.board_value_fact_mid,
                "attacked_pieces": self.attacked_pieces_fact_mid,
                "board_position": self.board_positions_fact_mid,
                "opp_board_position": self.opp_board_positions_fact_mid,
                "king_safety": self.king_safety_fact_mid,
                "opp_king_safety": self.opp_king_safety_fact_mid,
                "mobility": self.mobility_fact_mid,
                "history": self.history_fact_mid
            },
            3: {
                "board_value": self.board_value_fact_end,
                "attacked_pieces": self.attacked_pieces_fact_end,
                "board_position": self.board_positions_fact_end,
                "opp_board_position": self.opp_board_positions_fact_end,
                "king_safety": self.king_safety_fact_end,
                "opp_king_safety": self.opp_king_safety_fact_end,
                "mobility": self.mobility_fact_end,
                "history": self.history_fact_end
            }
        }[game_status]

    def get_max_depth_by_game_status(self, game_status):
        return {
            1: self.max_depth_start, 
            2: self.max_depth_mid,
            3: self.max_depth_end
        }[game_status]

    def import_opening_book(self, book_location):
        '''
        load an opening book
        raise an error if system cannot find the opening-book file
        '''
        if os.path.isfile(book_location):
            return chess.polyglot.open_reader(book_location)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), book_location)

    def import_syzygy(self, syzygy_location):
        '''
        load a syzygy tablebase
        raise an error if system cannot find the file
        '''
        if os.path.isdir(syzygy_location):
            return chess.syzygy.open_tablebase(syzygy_location)
        else:
            raise FileNotFoundError(
                errno.ENOENT, os.strerror(errno.ENOENT), SYZYGY_LOC)
