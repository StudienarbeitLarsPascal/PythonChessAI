#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# This file is the main file which starts the chess programm and calls the elementary methods
#

from python_chess_ai.settings import terminal, gui
from python_chess_ai.chess_master import ChessMaster
from python_chess_ai.misc.tools import Tools
from python_chess_ai.player import ai, api, dummy, user

USER_INPUT_MESSAGE = "Enter 0 for terminal and 1 for GUI: "


def main():
    ui_status = Tools.check_legal_input_int(range(2), USER_INPUT_MESSAGE)
    settings_ui = ui_switcher.get(ui_status).Settings()

    player_settings = settings_ui.interrogate_settings()
    players = []
    for player_setting in player_settings:
        type = type_switcher.get(player_setting.type)
        players.append(type.Player(player_setting.num, player_setting.name, ui_status, player_setting.difficulty))

    chess_master = ChessMaster()
    chess_master.start_chess_game(players)

ui_switcher = {
        0: terminal,
        1: gui
}

type_switcher = {
    1: user,
    2: ai,
    3: api,
    4: dummy
}

main()