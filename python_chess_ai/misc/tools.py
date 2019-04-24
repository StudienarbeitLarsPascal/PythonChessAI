#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# This file provides different basic functions needed in several parts of this program
#

import chess

WRONG_INPUT_MESSAGE = "Wrong input given. Please repeat."


def check_legal_input_string(legal_array, ask_for_input_msg, wrong_input_msg=WRONG_INPUT_MESSAGE):
    user_input = input(ask_for_input_msg)
    while user_input not in legal_array:
        print(wrong_input_msg)
        user_input = input(ask_for_input_msg)
    return user_input

def check_legal_input_int(legal_array, ask_for_input_msg, wrong_input_msg=WRONG_INPUT_MESSAGE):
    user_input = input(ask_for_input_msg)
    while not (user_input.isdigit() and int(user_input) in legal_array):
        print(wrong_input_msg)
        user_input = input(ask_for_input_msg)
    return int(user_input)

def get_key_with_max_val(key_val_dict):
    max_key = list(key_val_dict.keys())[0]
    max_val = list(key_val_dict.values())[0]
    for key, val in key_val_dict.items():
        if val > max_val:
            max_key = key
            max_val = val
    return max_key

def get_board_result(board):
    if board.is_variant_loss():
        return -1 if board.turn == chess.WHITE else 1
    elif board.is_variant_win():
        return 1 if board.turn == chess.WHITE else -1
    elif board.is_variant_draw():
        return 0

    # Checkmate.
    if board.is_checkmate():
        return -1 if board.turn == chess.WHITE else 1

    # Draw claimed.
    if board.can_claim_draw():
        return 0

    # Seventyfive-move rule or fivefold repetition.
    if board.is_seventyfive_moves() or board.is_fivefold_repetition():
        return 0

    # Insufficient material.
    if board.is_insufficient_material():
        return 0

    # Stalemate.
    if not any(board.generate_legal_moves()):
        return 0
    
    return 0
