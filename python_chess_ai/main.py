#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# This file is the main file which starts the chess program and calls the elementary methods
#
import sys, traceback
import argparse
from settings import terminal, gui
from chess_master import ChessMaster
from player import ai, api, dummy, user
from colorama import init

__version__ = "0.1-Alpha"

'''
values ai 1
'''
AO_MAX_DEPTH_START = 4
AO_BOARD_VALUE_FACTOR_START = 50
AO_ATTACKED_PIECES_FACTOR_START = 10
AO_BOARD_POSITIONS_FACTOR_START = 50
AO_OPP_BOARD_POSITIONS_FACTOR_START = 50
AO_KING_SAFETY_FACTOR_START = 5
AO_OPP_KING_SAFETY_FACTOR_START = 5
AO_MOBILITY_FACTOR_START = 4
AO_HISTORY_FACTOR_START = 1

AO_MAX_DEPTH_MID = 4
AO_BOARD_VALUE_FACTOR_MID = 50
AO_ATTACKED_PIECES_FACTOR_MID = 10
AO_BOARD_POSITIONS_FACTOR_MID = 25
AO_OPP_BOARD_POSITIONS_FACTOR_MID = 25
AO_KING_SAFETY_FACTOR_MID = 5
AO_OPP_KING_SAFETY_FACTOR_MID = 5
AO_MOBILITY_FACTOR_MID = 4
AO_HISTORY_FACTOR_MID = 0

AO_MAX_DEPTH_END = 10
AO_BOARD_VALUE_FACTOR_END = 50
AO_ATTACKED_PIECES_FACTOR_END = 20
AO_BOARD_POSITIONS_FACTOR_END = 10
AO_OPP_BOARD_POSITIONS_FACTOR_END = 10
AO_KING_SAFETY_FACTOR_END = 5
AO_OPP_KING_SAFETY_FACTOR_END = 10
AO_MOBILITY_FACTOR_END = 10
AO_HISTORY_FACTOR_END = 5

'''
values ai 2
'''
AT_MAX_DEPTH_START = 4
AT_BOARD_VALUE_FACTOR_START = 50
AT_ATTACKED_PIECES_FACTOR_START = 0
AT_BOARD_POSITIONS_FACTOR_START = 0
AT_OPP_BOARD_POSITIONS_FACTOR_START = 0
AT_KING_SAFETY_FACTOR_START = 0
AT_OPP_KING_SAFETY_FACTOR_START = 0
AT_MOBILITY_FACTOR_START = 0
AT_HISTORY_FACTOR_START = 0

AT_MAX_DEPTH_MID = 4
AT_BOARD_VALUE_FACTOR_MID = 50
AT_ATTACKED_PIECES_FACTOR_MID = 0
AT_BOARD_POSITIONS_FACTOR_MID = 0
AT_OPP_BOARD_POSITIONS_FACTOR_MID = 0
AT_KING_SAFETY_FACTOR_MID = 0
AT_OPP_KING_SAFETY_FACTOR_MID = 0
AT_MOBILITY_FACTOR_MID = 0
AT_HISTORY_FACTOR_MID = 0

AT_MAX_DEPTH_END = 0
AT_BOARD_VALUE_FACTOR_END = 50
AT_ATTACKED_PIECES_FACTOR_END = 0
AT_BOARD_POSITIONS_FACTOR_END = 0
AT_OPP_BOARD_POSITIONS_FACTOR_END = 0
AT_KING_SAFETY_FACTOR_END = 0
AT_OPP_KING_SAFETY_FACTOR_END = 0
AT_MOBILITY_FACTOR_END = 0
AT_HISTORY_FACTOR_END = 0


# usage argument parser: [-h] [-t | -g] [-p PLAYER PLAYER][-pT {User,AI,Player,Dummy} {User,AI,Player,Dummy}][-pD {0,1,2,3} {0,1,2,3}] [-v]
def intialize_parser():
    parser = argparse.ArgumentParser()
    ui_group = parser.add_mutually_exclusive_group()
    ui_group.add_argument("-t", "--terminal", help="starts the terminal ui", action="store_true")
    ui_group.add_argument("-g", "--gui", help="starts the GUI", action="store_true")

    player_name_type_group = parser.add_argument_group()
    player_name_type_group.add_argument("-p", "--player", nargs=2, help=argparse.SUPPRESS) # help="set name player 1 and 2"
    player_name_type_group.add_argument("-pT","--player_type", nargs=2, choices=["User","AI", "Player", "Dummy"], help=argparse.SUPPRESS) # help="enter player type for player 1 and 2"
    player_name_type_group.add_argument("-pD","--player_difficulty", nargs=2, type=int, choices=range(0,4), help=argparse.SUPPRESS) # help="enter ai difficulty for player 1 and 2, use 0 if you are not using ai"

    parser.add_argument("-v", "--version", help="print the version number and exit", action="store_true")
    return parser

def main(args):
    if (not (args.gui) and not (args.terminal) and not (args.version)):
        args.player=['AI1 White', 'AI2 Black']
        args.player_difficulty=[3, 3]
        args.player_type=['AI', 'AI']
        ui_status = 0
        start_chess_master(ui_status)
    elif args.terminal:
        ui_status = 1
        print("Start GUI")
    elif args.terminal:
        ui_status = 0
        start_chess_master(ui_status)
    elif args.version:
        print(__version__)

def start_chess_master(ui_status):
    try:
        settings_ui = ui_switcher(ui_status).Settings()
        player_settings = settings_ui.interrogate_settings(args.player, args.player_type, args.player_difficulty)
        players = []
        type = type_switcher(2)
        players.append(type.Player(player_settings[0].num, player_settings[0].name,ui_status, player_settings[0].difficulty, board_value_fact_start = AO_BOARD_VALUE_FACTOR_START, attacked_pieces_fact_start = AO_ATTACKED_PIECES_FACTOR_START, board_positions_fact_start = AO_BOARD_POSITIONS_FACTOR_START, opp_board_positions_fact_start = AO_OPP_BOARD_POSITIONS_FACTOR_START, king_safety_fact_start = AO_KING_SAFETY_FACTOR_START, opp_king_safety_fact_start = AO_OPP_KING_SAFETY_FACTOR_START, mobility_fact_start = AO_MOBILITY_FACTOR_START, history_fact_start = AO_HISTORY_FACTOR_START, max_depth_start = AO_MAX_DEPTH_START, board_value_fact_mid = AO_BOARD_VALUE_FACTOR_MID, attacked_pieces_fact_mid = AO_ATTACKED_PIECES_FACTOR_MID, board_positions_fact_mid = AO_BOARD_POSITIONS_FACTOR_MID, opp_board_positions_fact_mid = AO_OPP_BOARD_POSITIONS_FACTOR_MID, king_safety_fact_mid = AO_KING_SAFETY_FACTOR_MID, opp_king_safety_fact_mid = AO_OPP_KING_SAFETY_FACTOR_MID, mobility_fact_mid = AO_MOBILITY_FACTOR_MID, history_fact_mid = AO_HISTORY_FACTOR_MID, max_depth_mid = AO_MAX_DEPTH_MID, board_value_fact_end = AO_BOARD_VALUE_FACTOR_END, attacked_pieces_fact_end = AO_ATTACKED_PIECES_FACTOR_END, board_positions_fact_end = AO_BOARD_POSITIONS_FACTOR_END, opp_board_positions_fact_end = AO_OPP_BOARD_POSITIONS_FACTOR_END, king_safety_fact_end = AO_KING_SAFETY_FACTOR_END, opp_king_safety_fact_end = AO_OPP_KING_SAFETY_FACTOR_END, mobility_fact_end = AO_MOBILITY_FACTOR_END, history_fact_end = AO_HISTORY_FACTOR_END, max_depth_end = AO_MAX_DEPTH_END))
        players.append(type.Player(player_settings[1].num, player_settings[1].name,ui_status, player_settings[1].difficulty, board_value_fact_start = AT_BOARD_VALUE_FACTOR_START, attacked_pieces_fact_start = AT_ATTACKED_PIECES_FACTOR_START, board_positions_fact_start = AT_BOARD_POSITIONS_FACTOR_START, opp_board_positions_fact_start = AT_OPP_BOARD_POSITIONS_FACTOR_START, king_safety_fact_start = AT_KING_SAFETY_FACTOR_START, opp_king_safety_fact_start = AT_OPP_KING_SAFETY_FACTOR_START, mobility_fact_start = AT_MOBILITY_FACTOR_START, history_fact_start = AT_HISTORY_FACTOR_START, max_depth_start = AT_MAX_DEPTH_START, board_value_fact_mid = AT_BOARD_VALUE_FACTOR_MID, attacked_pieces_fact_mid = AT_ATTACKED_PIECES_FACTOR_MID, board_positions_fact_mid = AT_BOARD_POSITIONS_FACTOR_MID, opp_board_positions_fact_mid = AT_OPP_BOARD_POSITIONS_FACTOR_MID, king_safety_fact_mid = AT_KING_SAFETY_FACTOR_MID, opp_king_safety_fact_mid = AT_OPP_KING_SAFETY_FACTOR_MID, mobility_fact_mid = AT_MOBILITY_FACTOR_MID, history_fact_mid = AT_HISTORY_FACTOR_MID, max_depth_mid = AT_MAX_DEPTH_MID, board_value_fact_end = AT_BOARD_VALUE_FACTOR_END, attacked_pieces_fact_end = AT_ATTACKED_PIECES_FACTOR_END, board_positions_fact_end = AT_BOARD_POSITIONS_FACTOR_END, opp_board_positions_fact_end = AT_OPP_BOARD_POSITIONS_FACTOR_END, king_safety_fact_end = AT_KING_SAFETY_FACTOR_END, opp_king_safety_fact_end = AT_OPP_KING_SAFETY_FACTOR_END, mobility_fact_end = AT_MOBILITY_FACTOR_END, history_fact_end = AT_HISTORY_FACTOR_END, max_depth_end = AT_MAX_DEPTH_END))

        chess_master = ChessMaster()
        chess_master.start_chess_game(players)
    except KeyboardInterrupt:
        print("\nYou've quit the game.")
    except Exception:
        traceback.print_exc(file=sys.stdout)
    sys.exit(0)

def ui_switcher(ui_type):
    return {
        0: terminal,
        1: gui
    }[ui_type]

def type_switcher(player_type):
    return {
        1: user,
        2: ai,
        3: api,
        4: dummy,
        "User": user,
        "AI": ai,
        "Player": api,
        "Dummy": dummy
    }[player_type]

if __name__ == '__main__':
    parser = intialize_parser()
    args = parser.parse_args()
    main(args)