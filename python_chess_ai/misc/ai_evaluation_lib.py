#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# This file provides different methods for basic chess calculations like board evaluation
#

import chess
import pandas as pd

PAWN_VALUE = 1
ROOK_VALUE = 5
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
QUEEN_VALUE = 9
KING_VALUE = 15

HISTORY_FILE_LOC = "res/history.csv"


def assign_piece_value(piece_type, count_king=True):
    '''
    returns the value of a piece type for the given type
    '''
    if count_king:
        return {
            1: PAWN_VALUE,
            2: KNIGHT_VALUE,
            3: BISHOP_VALUE,
            4: ROOK_VALUE,
            5: QUEEN_VALUE,
            6: KING_VALUE
        }.get(piece_type, 0)
    else:
        return {
            1: PAWN_VALUE,
            2: KNIGHT_VALUE,
            3: BISHOP_VALUE,
            4: ROOK_VALUE,
            5: QUEEN_VALUE,
            6: 0
        }.get(piece_type, 0)


def get_value_by_color(board, color, count_king=True):
    '''
    sums value of all pieces of given color multiplied with their value
    '''
    attacked_pieces_value = map(
        lambda piece_type: len(board.pieces(piece_type, color)) * assign_piece_value(piece_type, count_king), chess.PIECE_TYPES)
    return sum(attacked_pieces_value)


def get_board_value(board, count_king=True):
    '''
    calculates value of white pieces and subtracts value of black pieces => calculates board value
    returns positive number if white has an advantage, negative number in case black has
    '''
    white_value = get_value_by_color(board, chess.WHITE, count_king)
    black_value = get_value_by_color(board, chess.BLACK, count_king)

    return white_value - black_value


def get_attacked_pieces_value_by_color(board, attacker_color, defender_color):
    '''
    calculates how many figures are attacked by given color and assigns a value for every attacked figure
    '''
    # filters squares for attacked squares, on which a figure of defender is placed
    attacked_squares = filter(lambda square: board.is_attacked_by(attacker_color, square) and not board.piece_at(
        square) is None and board.piece_at(square).color is defender_color, chess.SQUARES)
    # maps piece type to attacked figure
    attacked_pieces = map(lambda square: board.piece_at(square).piece_type, attacked_squares)
    # maps piece value to attacked pieces
    value = map(assign_piece_value, attacked_pieces)
    # sums piece value of all attacked pieces
    return sum(value)


def get_attacked_pieces_value(board):
    '''
    calculates value of attacked black pieces and subtracts value of attacked white pieces => calculates attacked pieces value
    '''
    white_value = get_attacked_pieces_value_by_color(board, chess.WHITE, chess.BLACK)
    black_value = get_attacked_pieces_value_by_color(board, chess.BLACK, chess.WHITE)

    return white_value - black_value


def get_board_value_by_history(board):
    '''
    check history file if board has stored given board
    returns value of the board in case it does
    otherwise it returns 0
    '''
    dataset = pd.read_csv(HISTORY_FILE_LOC)
    row = dataset.loc[dataset['board'] == board.fen().split(" ")[0]]
    value = row['value'].item() if len(row['value']) == 1 else 0
    return value