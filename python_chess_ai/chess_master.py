#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# This file is responsible for the chess game itself, manages the chess board and asks the players for their move
#

import chess
import pandas as pd
import misc.tools as Tools

GAME_FINISHED_MESSAGE = "Game finished. You want a rematch? (Type 1 if yes)"
WRONG_INPUT_MESSAGE = "Wrong input. Please repeat."

HISTORY_FILE_LOC = "res/history.csv"


class ChessMaster:
    def start_chess_game(self, players):
        repeat = 1
        while repeat == 1:

            board = chess.Board()
            turn_list = list()
            while not board.is_game_over():
                current_player = players[int(not board.turn)]
                current_player.print_board(current_player.name, board)

                move = current_player.get_move(board)
                board.push(move)
                current_player.submit_move(move)
                print(board.fen())

                turn_list.append(board.fen().split(" ")[0])

            current_player = players[int(not board.turn)]
            current_player.print_board(current_player.name, board)
            # replace (gui/terminal) - current player win message? all players message?

            result = Tools.get_board_result(board)
            if result is 1:
                print("{} (White) has won".format(players[0].name))
            elif result is -1:
                print("{} (Black) has won".format(players[1].name))
            else:
                print("Draw")

            self.groom_board_history(board, turn_list)
            repeat = int(input(GAME_FINISHED_MESSAGE))

    def groom_board_history(self, final_board, turn_list):
        # Todo: replace victory status calculation with correct version (draw/player1/player2)
        victory_status = Tools.get_board_result(final_board)

        new_turn_dict = dict.fromkeys(turn_list, victory_status)
        # get existing board history
        history = pd.read_csv(HISTORY_FILE_LOC)
        history_dict = dict(zip(list(history.board), list(history.value)))
        # merge existing history with new boards and sum the victory states
        merged_history_dict = { k: new_turn_dict.get(k, 0) + history_dict.get(k, 0) for k in set(new_turn_dict) | set(history_dict) }
        merged_history = pd.DataFrame(list(merged_history_dict.items()), columns=['board','value'])
        # overwrite history csv with new, merged history
        merged_history.to_csv(HISTORY_FILE_LOC)

