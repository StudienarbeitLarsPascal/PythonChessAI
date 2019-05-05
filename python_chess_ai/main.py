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

# usage argument parser: [-h] [-t | -g] [-p PLAYER PLAYER][-pT {User,AI,Player,Dummy} {User,AI,Player,Dummy}][-pD {0,1,2,3} {0,1,2,3}] [-v]
def intialize_parser():
    parser = argparse.ArgumentParser()
    ui_group = parser.add_mutually_exclusive_group()
    ui_group.add_argument("-s", "--settings", help="set the player settings", action="store_true")
    ui_group.add_argument("-g", "--gui", help="starts the GUI", action="store_true")

    player_name_type_group = parser.add_argument_group()
    player_name_type_group.add_argument("-p", "--player", nargs=2, help=argparse.SUPPRESS) # help="set name player 1 and 2"
    player_name_type_group.add_argument("-pT","--player_type", nargs=2, choices=["User","AI", "Player", "Dummy"], help=argparse.SUPPRESS) # help="enter player type for player 1 and 2"
    player_name_type_group.add_argument("-pD","--player_difficulty", nargs=2, type=int, choices=range(0,4), help=argparse.SUPPRESS) # help="enter ai difficulty for player 1 and 2, use 0 if you are not using ai"

    parser.add_argument("-v", "--version", help="print the version number and exit", action="store_true")
    return parser

def main(args):
    if (not (args.gui) and not (args.settings) and not (args.version)):
        args.player=['Player', 'AI']
        args.player_difficulty=[0, 3]
        args.player_type=['User', 'AI']
        ui_status = 0
        start_chess_master(ui_status)
    elif args.gui:
        ui_status = 1
        print("Start GUI")
    elif args.settings:
        ui_status = 0
        start_chess_master(ui_status)
    elif args.version:
        print(__version__)

def start_chess_master(ui_status):
    try:
        settings_ui = ui_switcher(ui_status).Settings()
        player_settings = settings_ui.interrogate_settings(args.player, args.player_type, args.player_difficulty)
        players = []
        for player_setting in player_settings:
            type = type_switcher(player_setting.type)
            players.append(type.Player(player_setting.num, player_setting.name,ui_status, player_setting.difficulty))

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