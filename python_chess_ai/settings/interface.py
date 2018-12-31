#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Interface for entering settings like player type, name etc.
#

from abc import ABC, ABCMeta, abstractmethod
from python_chess_ai.settings.player_settings import PlayerSettings


class SettingsInterface(ABC):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_player_type(self, player_num):
        ...

    @abstractmethod
    def get_player_name(self, player_num):
        ...

    @abstractmethod
    def get_difficulty(self, player_num):
        ...

    def interrogate_settings(self):
        """todo: find more elegant way?"""
        players = []
        for i in range(2):
            num = i+1
            name = self.get_player_name(num)
            player_type = self.get_player_type(num)

            difficulty = None
            if player_type == 2:
                difficulty = self.get_difficulty()

            new_player = PlayerSettings(num, name, player_type, difficulty)
            players.append(new_player)

        return players
