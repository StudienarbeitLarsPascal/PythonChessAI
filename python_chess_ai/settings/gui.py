#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# GUI implementation for settings interface
#

from python_chess_ai.settings.interface import SettingsInterface


class Settings(SettingsInterface):

    def get_player_type(self, player_num):
        super().get_player_type(player_num)

    def get_player_name(self, player_num):
        super().get_player_name(player_num)

    def get_difficulty(self, player_num):
        super().get_difficulty(player_num)