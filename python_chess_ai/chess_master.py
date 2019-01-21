#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# This file is responsible for the chess game itself, manages the chess board and asks the players for their move
#

import chess

GAME_FINISHED_MESSAGE = "Game finished. You want a rematch? (Type 1 if yes)"
WRONG_INPUT_MESSAGE = "Wrong input. Please repeat."


class ChessMaster:
    @staticmethod
    def start_chess_game(players):
        repeat = 1
        while repeat == 1:

            board = chess.Board()
            while not board.is_game_over():
                current_player = players[int(board.turn)]
                current_player.print_board(current_player.name, board)
                move = current_player.get_move(board)
                print(move)
                board.push(move)

                print(board)
                current_player.submit_move(move)

            repeat = int(input(GAME_FINISHED_MESSAGE))
