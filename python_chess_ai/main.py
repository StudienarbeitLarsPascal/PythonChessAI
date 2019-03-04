#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# This file is the main file which starts the chess program and calls the elementary methods
#

import argparse
from settings import terminal, gui
from chess_master import ChessMaster
from player import ai, api, dummy, user

# usage argument parser: [-h][-t | -g][-v]
parser = argparse.ArgumentParser()
ui_group = parser.add_mutually_exclusive_group()
ui_group.add_argument("-t", "--terminal", help="starts the terminal ui", action="store_true")
ui_group.add_argument("-g", "--gui", help="starts the GUI", action="store_true")
parser.add_argument("-v", "--version", help="print the version number and exit", action="store_true")
args = parser.parse_args()

def main():
    if args.terminal or (not (args.terminal) and not (args.gui)):
        ui_status = 0
    elif args.terminal:
        ui_status = 1
    elif args.version:
        print("ToDo Version")

    settings_ui = get_ui(ui_status).Settings()
    player_settings = settings_ui.interrogate_settings()
    players = []
    for player_setting in player_settings:
        type = get_player_by_type(player_setting.type)
        players.append(type.Player(player_setting.num, player_setting.name, ui_status, player_setting.difficulty))

    chess_master = ChessMaster()
    chess_master.start_chess_game(players)

def get_ui(ui_status):
    ui_switcher = {
        0: terminal,
        1: gui
    }
    return ui_switcher.get(ui_status)

def get_player_by_type(type):
    type_switcher = {
        1: user,
        2: ai,
        3: api,
        4: dummy
    }
    return type_switcher.get(type)

if __name__ == '__main__':
    main()