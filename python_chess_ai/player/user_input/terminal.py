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

ASK_FOR_MOVE_MESSAGE = "Possible Moves: {}\nEnter your move: "
WRONG_INPUT_MESSAGE = "Given move not in legal moves. Please repeat"
PLAYER_TURN_MESSAGE = "\n\nIt's {}'s turn: "


class UserInput(UserInputInterface):
    def __init__(self):
        super().__init__()

    piece_switcher = {
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
    }

    column_description = {
        0: " ",
        1: "A",
        2: "B",
        3: "C",
        4: "D",
        5: "E",
        6: "F",
        7: "G",
        8: "H"
    }

    def get_move(self, legal_moves):
        super().get_move(legal_moves)
        input_msg = ASK_FOR_MOVE_MESSAGE.format(legal_moves)
        move = Tools.check_legal_input_string(legal_moves,input_msg, WRONG_INPUT_MESSAGE)
        return move
    
    def print_board(self, player_name, board):
        super().print_board(player_name, board)
        print(PLAYER_TURN_MESSAGE.format(player_name))

        splitted_board = str(board).split("\n")
        field_number = 0
        row_counter = 1
        for row in splitted_board:
            if row_counter == 1:
                for i in range(0,9):
                    print(self.column_description.get(i).center(3), end='')
                print("\n", end='')
            splitted_row = row.split(" ")
            field_number = 0 if field_number %2 is 0 else 1
            column_counter = 1
            for chess_field in splitted_row:
                field_number += 1
                if column_counter == 1:
                    colored_field = " " + str(row_counter) + " " + self.create_piece(chess_field, field_number)  
                elif column_counter == 8:
                    colored_field = self.create_piece(chess_field, field_number) + " " + str(row_counter)
                else:
                    colored_field = self.create_piece(chess_field, field_number)
                print(colored_field, end='')
                column_counter += 1
            print("\n", end='')
            field_number += 1
            row_counter += 1
        for i in range(0,9):
            print(self.column_description.get(i).center(3), end='')
        print("\n")

    def create_piece(self, character, field):
        chess_piece = str(self.piece_switcher.get(character)) if not (character == ".") else ""
        chess_piece_color = FG_BLACK if character.isupper() else FG_WHITE
        colored_chess_piece = chess_piece_color + chess_piece.center(3) + fg.rs
        background_color = BG_BLACK if field %2 is 0 else BG_WHITE
        field = background_color + colored_chess_piece + bg.rs
        return field
