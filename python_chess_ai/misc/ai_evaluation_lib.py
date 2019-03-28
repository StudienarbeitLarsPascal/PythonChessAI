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
import numpy as np

PAWN_VALUE = 1
ROOK_VALUE = 5
KNIGHT_VALUE = 3
BISHOP_VALUE = 3
QUEEN_VALUE = 9
KING_VALUE = 15

PAWN_POSITION_MATRIX =      np.array(   [[0,0,0,0,0,0,0,0],
                                        [50,50,50,50,50,50,50,50],
                                        [10,10,20,30,30,20,10,10],
                                        [5,5,10,25,25,10,5,5],
                                        [0,0,0,20,20,0,0,0],
                                        [5,-5,-10,0,0,-10,-5,5],
                                        [5,10,10,-20,-20,10,10,5],
                                        [0,0,0,0,0,0,0,0]])

KNIGHT_POSITION_MATRIX =    np.array(   [[-50,-40,-30,-30,-30,-30,-40,-50],
                                        [-40,-20,0,0,0,0,-20,-40],
                                        [-30,0,10,15,15,10,0,-30],
                                        [-30,5,15,20,20,15,5,-30],
                                        [-30,0,15,20,20,15,0,-30],
                                        [-30,5,10,15,15,10,5,-30],
                                        [-40,-20,0,5,5,0,-20,-40],
                                        [-50,-40,-30,-30,-30,-30,-40,-50]])

BISHOP_POSITION_MATRIX =    np.array(   [[-20,-10,-10,-10,-10,-10,-10,-20],
                                        [-10,0,0,0,0,0,0,-10],
                                        [-10,0,5,10,10,5,0,-10],
                                        [-10,5,5,10,10,5,5,-10],
                                        [-10,0,10,10,10,10,0,-10],
                                        [-10,10,10,10,10,10,10,-10],
                                        [-10,5,0,0,0,0,5,-10],
                                        [-20,-10,-10,-10,-10,-10,-10,-20]])

ROOK_POSITION_MATRIX =      np.array(   [[0,0,0,0,0,0,0,0],
                                        [5,10,10,10,10,10,10,5],
                                        [-5,0,0,0,0,0,0,-5],
                                        [-5,0,0,0,0,0,0,-5],
                                        [-5,0,0,0,0,0,0,-5],
                                        [-5,0,0,0,0,0,0,-5],
                                        [-5,0,0,0,0,0,0,-5],
                                        [0,0,0,5,5,0,0,0]])

QUEEN_POSITION_MATRIX =     np.array(   [[-20,-10,-10,-5,-5,-10,-10,-20],
                                        [-10,0,0,0,0,0,0,-10],
                                        [-10,0,5,5,5,5,0,-10],
                                        [-5,0,5,5,5,5,0,-5],
                                        [0,0,5,5,5,5,0,-5],
                                        [-10,5,5,5,5,5,0,-10],
                                        [-10,0,5,0,0,0,0,-10],
                                        [-20,-10,-10,-5,-5,-10,-10,-20]])

KING_POSITION_MATRIX =      np.array(   [[-30,-40,-40,-50,-50,-40,-40,-30],
                                        [-30,-40,-40,-50,-50,-40,-40,-30],
                                        [-30,-40,-40,-50,-50,-40,-40,-30],
                                        [-30,-40,-40,-50,-50,-40,-40,-30],
                                        [-20,-30,-30,-40,-40,-30,-30,-20],
                                        [-10,-20,-20,-20,-20,-20,-20,-10],
                                        [20,20,0,0,0,0,20,20],
                                        [20,30,10,0,0,10,30,20]])

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


def get_board_value(board, color, count_king=True):
    '''
    calculates value of white pieces and subtracts value of black pieces => calculates board value
    returns positive number if given color has an advantage, negative if given color has a disadvantage
    '''
    white_value = get_value_by_color(board, chess.WHITE, count_king)
    black_value = get_value_by_color(board, chess.BLACK, count_king)

    return white_value - black_value if color is chess.WHITE else black_value - white_value


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


def get_attacked_pieces_value(board, color):
    '''
    calculates value of attacked black pieces and subtracts value of attacked white pieces => calculates attacked pieces value
    returns positive number if given color has an advantage, negative if given color has a disadvantage
    '''
    white_value = get_attacked_pieces_value_by_color(board, chess.WHITE, chess.BLACK)
    black_value = get_attacked_pieces_value_by_color(board, chess.BLACK, chess.WHITE)

    return white_value - black_value if color is chess.WHITE else black_value - white_value


def assign_piece_matrix(piece_type):
    '''
    returns the individual position matrix of the given piece type
    '''
    return {
        1: PAWN_POSITION_MATRIX,
        2: KNIGHT_POSITION_MATRIX,
        3: BISHOP_POSITION_MATRIX,
        4: ROOK_POSITION_MATRIX,
        5: QUEEN_POSITION_MATRIX,
        6: KING_POSITION_MATRIX
    }.get(piece_type, np.zeros((8,8)))


def get_position_value_by_square(board, rank, file, color):
    '''
    returns the value of the position of a piece by position matrix
    matrix is dependent on piece type and color
    '''
    piece_type = board.piece_type_at(chess.square(file, rank))
    piece_matrix = assign_piece_matrix(piece_type) if color == chess.WHITE else np.flip(assign_piece_matrix(piece_type))
    piece_pos_value = piece_matrix[rank,file]
    return piece_pos_value


def get_board_positions_value_by_color(board, color):
    '''
    returns summed value of all pieces and its positions of one color
    '''
    sum = 0
    for rank in range(0,8):
        for file in range(0,8):
            piece = board.piece_at(chess.square(file, rank))
            if (piece and piece.color == color):
                piece_pos_value = get_position_value_by_square(board, rank, file, color)
                sum += piece_pos_value
    return sum
        

def get_board_positions_value(board, color):
    '''
    calculates value of white pieces dependent on its position and subtracts value of black pieces dependent on its position
    returns positive number if given color has an advantage, negative if given color has a disadvantage
    '''
    white_value = get_board_positions_value_by_color(board, chess.WHITE) / 10
    black_value = get_board_positions_value_by_color(board, chess.BLACK) / 10

    return (white_value - black_value) if color is chess.WHITE else (black_value - white_value)


def get_piece_position(board, piece):
    '''
    returns position of given piece
    if piece exists multiple times it returns first to be found
    '''
    for rank in range(0,8):
        for file in range(0,8):
            if board.piece_at(chess.square(file, rank)) == piece:
                return rank, file


def calculate_king_zone(board, color):
    '''
    calculates king zone of king of given color with a
    width of 3 squares (1 to the left, 1 to the right of the king)
    height of 4 squares (3 to to the front of the king)
    '''
    king_zone = chess.SquareSet()
    king_rank, king_file = get_piece_position(board, chess.Piece(chess.KING, color))

    rank_range = range(0,4) if color == chess.WHITE else range(-3, 1)
    for rank_summand in rank_range:
        if (king_rank + rank_summand) in range(0, 8):
            for file_summand in range(-1, 2):
                if (king_file + file_summand) in range (0,8):
                    king_zone.add(chess.square(king_file + file_summand, king_rank + rank_summand))
    
    return king_zone

def get_attackers_by_squares(board, square_set, attacker_color):
    '''
    returns dictionary with all attackers of a given square set
    key = attacker, value = num of fields attacker is attacking
    '''
    attacker_dict = {}
    for square in square_set:
        attacker_square_set = board.attackers(attacker_color, square)
        for attacker_square in attacker_square_set:
            attacker_piece = board.piece_at(attacker_square)
            if not (attacker_piece.piece_type is chess.PAWN or attacker_piece.piece_type is chess.KING):
                attacker_dict[attacker_piece] = attacker_dict.get(attacker_piece, 0) + 1
    return attacker_dict

def get_king_attack_weight(piece_counter):
    '''
    returns a value dependent on the num of attackers
    '''
    return {
        0: 0,
        1: 0,
        2: 50,
        3: 75,
        4: 88,
        5: 94,
        6: 97,
        7: 99
    }.get(piece_counter)

def get_king_attack_constants(piece):
    '''
    returns the value of a piece type for the given type
    '''
    return {
        chess.KNIGHT: 20,
        chess.BISHOP: 20,
        chess.ROOK: 40,
        chess.QUEEN: 80
    }.get(piece, 0)

def calculate_king_zone_safety(board, color):
    '''
    calculates value for enemy pieces attacking own king zone
    uses num of attackers, piece type of attackers and num of attacked squares per piece
    '''
    attacker_color = chess.WHITE if color == chess.BLACK else chess.BLACK
    king_zone = calculate_king_zone(board, color)
    attackers = get_attackers_by_squares(board, king_zone, attacker_color)
    attack_weight = get_king_attack_weight(len(attackers))
    value_of_attack = 0
    for attacker in attackers:
        value_of_attack += get_king_attack_constants(attacker.piece_type)
    
    return (value_of_attack * attack_weight) / 100

def calculate_opp_king_zone_safety(board, color):
    '''
    calculates value for own pieces attacking enemy king zone
    uses num of attackers, piece type of attackers and num of attacked squares per piece
    '''
    opp_color = chess.WHITE if color is chess.BLACK else chess.BLACK
    return calculate_king_zone_safety(board, opp_color)


def get_num_of_legal_moves_by_color(board, color):
    '''
    returns number of legal moves for given color
    if given color is not the color to make the next move, the average for all possible moves of opponent is returned
    '''
    player = chess.WHITE if bool(board.turn) else chess.BLACK
    if player == color:
        return len(list(board.legal_moves))
    else:
        overall_legal_moves = 0
        for action in board.legal_moves:
            tmp_board = chess.Board(str(board.fen()))
            tmp_board.push(action)
            overall_legal_moves += len(list(tmp_board.legal_moves))
        return overall_legal_moves / len(list(board.legal_moves))


def calculate_mobility_value(board, color):
    '''
    returns mobility value (num of possible moves)
    returns positive number if given color has an advantage, negative if given color has a disadvantage
    '''
    white_value = get_num_of_legal_moves_by_color(board, chess.WHITE)
    black_value = get_num_of_legal_moves_by_color(board, chess.BLACK)

    return (white_value - black_value) if color is chess.WHITE else (black_value - white_value)


def get_board_value_by_history(board, color):
    '''
    check history file if board has stored given board
    returns value of the board in case it does
    otherwise it returns 0
    '''
    dataset = pd.read_csv(HISTORY_FILE_LOC)
    row = dataset.loc[dataset['board'] == board.fen().split(" ")[0]]
    value = row['value'].item() if len(row['value']) == 1 else 0
    return value if color is chess.WHITE else -1*value