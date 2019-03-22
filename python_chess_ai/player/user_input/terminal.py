#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Terminal implementation for user_input interface
#

from player.user_input.interface import UserInputInterface
from misc.tools import Tools
from sty import ef, fg, bg, rs

FG_BLACK = fg(0, 0, 0)
FG_WHITE = fg(255, 255,255)
BG_BLACK = bg(222, 184, 135)
BG_WHITE = bg(211, 211, 211)
NUM_TO_ALPHABET = [" ","A", "B", "C", "D", "E", "F", "G", "H"]

ASK_FOR_MOVE_MESSAGE = "Possible Moves: {}\nEnter your move: "
WRONG_INPUT_MESSAGE = "Given move not in legal moves. Please repeat"
PLAYER_TURN_MESSAGE = "\n\nIt's {}'s turn: "


class UserInput(UserInputInterface):
    def __init__(self):
        super().__init__()

    def piece_switcher(self, piece):
        return {
            "K": u'\u2654',
            "Q": u'\u2655',
            "R": u'\u2656',
            "B": u'\u2657',
            "N": u'\u2658',
            "P": u'\u2659',
            "k": u'\u265A',
            "q": u'\u265B',
            "r": u'\u265C',
            "b": u'\u265D',
            "n": u'\u265E',
            "p": u'\u265F'
        }[piece]

    def create_board_matrix(self, board):
        board_fen = board.fen().split(" ")[0]
        board_matrix = []

        for row in board_fen.split("/"):
            line = []
            for character in row:
                if character.isdigit():
                    for empty in range(int(character)):
                        line.append(" ")
                else: 
                    line.append(character)
            board_matrix.append(line)
        return board_matrix

    def get_move(self, legal_moves):
        super().get_move(legal_moves)
        input_msg = ASK_FOR_MOVE_MESSAGE.format(legal_moves)
        move = Tools.check_legal_input_string(legal_moves,input_msg, WRONG_INPUT_MESSAGE)
        return move

    def print_alphabetical_description(self):
        for i in range(0,9):
            print(NUM_TO_ALPHABET[i].center(3), end='')
        print("\n", end='')
    
    def print_board(self, player_name, board):
        super().print_board(player_name, board)
        print(PLAYER_TURN_MESSAGE.format(player_name))

        board_fen = self.create_board_matrix(board)

        self.print_alphabetical_description()
        for row_index, row in enumerate(board_fen):
            print((str(row_index + 1)).center(3), end="")
            for field_index, chess_field in enumerate(row): 
                field_index = bool((field_index + 1) % 2) if row_index % 2 is 0 else bool(field_index % 2)
                colored_field = self.create_piece(chess_field, field_index)
                print(colored_field, end='')
            print((str(row_index + 1) + "\n").center(3), end="")
        self.print_alphabetical_description()

    def create_piece(self, character, field_index):
        chess_piece = str(self.piece_switcher(character)) if not (character == " ") else ""
        chess_piece_color = FG_BLACK if character.isupper() else FG_WHITE
        colored_chess_piece = chess_piece_color + chess_piece.center(3) + fg.rs
        background_color = BG_BLACK if field_index is False else BG_WHITE
        field = background_color + colored_chess_piece + bg.rs
        return field
