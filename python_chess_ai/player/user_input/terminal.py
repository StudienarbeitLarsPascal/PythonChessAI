#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Terminal implementation for user_input interface
#
from player.user_input.interface import UserInputInterface
import sys
from colorama import init
import misc.tools as Tools
from sty import ef, fg, bg, rs
from colorama import Fore, Back, Style

FG_BLACK = fg(0)
FG_WHITE = fg(255)
BG_BLACK = bg(137)
BG_WHITE = bg(248)

FG_BLACK_WIN = Fore.BLACK
FG_WHITE_WIN = Fore.RED
BG_BLACK_WIN = Back.YELLOW
BG_WHITE_WIN = Back.GREEN
NUM_TO_ALPHABET = [" ","a", "b", "c", "d", "e", "f", "g", "h"]

ASK_FOR_MOVE_MESSAGE = "Possible Moves: {}\nEnter your move: "
WRONG_INPUT_MESSAGE = "Given move not in legal moves. Please repeat"
PLAYER_TURN_MESSAGE = "\n\nIt's {}'s turn: "

class UserInput(UserInputInterface):
    def __init__(self):
        super().__init__()
        self.need_win_support = self.ensure_windows_compability()
        
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
        }.get(piece, piece)

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
        board_matrix = self.create_board_matrix(board)
        self.print_alphabetical_description()
        for row_index, row in enumerate(board_matrix):
            print((str(8 - row_index)).center(3), end="")
            for field_index, field in enumerate(row):
                field_is_dark = bool((field_index + row_index)% 2)
                colored_field = self.create_piece(field, field_is_dark) if not self.need_win_support else self.create_piece_win(field, field_is_dark)
                print(colored_field, end='')
            print((str(8 - row_index)).center(3))
        self.print_alphabetical_description()

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

    def create_piece(self, character, field_is_dark):
        chess_piece = character
        chess_piece_color = FG_WHITE if character.isupper() else FG_BLACK
        colored_chess_piece = chess_piece_color + chess_piece.center(3) + fg.rs
        background_color = BG_BLACK if field_is_dark is False else BG_WHITE
        field = background_color + colored_chess_piece + bg.rs
        return field

    def create_piece_win(self, character, field_is_dark):
        chess_piece = character
        chess_piece_color = FG_WHITE_WIN if character.isupper() else FG_BLACK_WIN
        colored_chess_piece = chess_piece_color + chess_piece.center(3)
        background_color = BG_BLACK_WIN if field_is_dark is False else BG_WHITE_WIN
        field = background_color + colored_chess_piece
        return field

    def os_is_windows(self):
        return {
            'linux' : False,
            'linux1' : False,
            'linux2' : False,
            'darwin' : False,
            'win32' : True
        }.get(sys.platform, False)

    def ensure_windows_compability(self):
        os_windows = self.os_is_windows()
        if os_windows:
            init(autoreset=True)
        return os_windows
