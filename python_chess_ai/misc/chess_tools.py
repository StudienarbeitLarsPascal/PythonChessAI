#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# This file provides different methods for basic chess calculations like board evaluation
#

import chess

PAWN_VALUE = 1
ROOK_VALUE = 5
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
QUEEN_VALUE = 9
KING_VALUE = 15


def get_legal_moves_uci(board):
    return list(map(board.uci, board.legal_moves))


# returns the value of a piece type for the given type
def assign_piece_value(piece_type):
    return {
        1: PAWN_VALUE,
        2: KNIGHT_VALUE,
        3: BISHOP_VALUE,
        4: ROOK_VALUE,
        5: QUEEN_VALUE,
        6: KING_VALUE
    }[piece_type]


# sums value of all pieces of given color multiplied with their value
def get_value_by_color(board, color):
    attacked_pieces_value = map(
        lambda piece_type: len(board.pieces(piece_type, color)) * assign_piece_value(piece_type), chess.PIECE_TYPES)
    return sum(attacked_pieces_value)


# calculates value of white pieces and subtracts value of black pieces => calculates board value
def get_board_value(board):
    white_value = get_value_by_color(board, chess.WHITE)
    black_value = get_value_by_color(board, chess.BLACK)

    return white_value - black_value


# calculates how many figures are attacked by given color and assigns a value for every attacked figure
def get_attacked_pieces_value_by_color(board, attacker_color, defender_color):
    # filters squares for attacked squares, on which a figure of defender is placed
    attacked_squares = filter(lambda square: board.is_attacked_by(attacker_color, square) and not board.piece_at(
        square) is None and board.piece_at(square).color is defender_color, chess.SQUARES)
    # maps piece type to attacked figure
    attacked_pieces = map(lambda square: board.piece_at(square).piece_type, attacked_squares)
    # maps piece value to attacked pieces
    value = map(assign_piece_value, attacked_pieces)
    # sums piece value of all attacked pieces
    return sum(value)


# calculates value of attacked black pieces and subtracts value of attacked white pieces => calculates attacked pieces value
def get_attacked_pieces_value(board):
    white_value = get_attacked_pieces_value_by_color(board, chess.WHITE, chess.BLACK)
    black_value = get_attacked_pieces_value_by_color(board, chess.BLACK, chess.WHITE)

    return white_value - black_value
