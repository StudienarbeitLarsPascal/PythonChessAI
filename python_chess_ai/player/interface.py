#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Interface for chess players which provides functions for get the next move and output of the board etc.
#

from abc import ABC, ABCMeta, abstractmethod


class PlayerInterface(ABC):
    __metaclass__ = ABCMeta

    def __init__(self, num, name, ui_status, difficulty=None):
        super().__init__()
        self.num = num
        self.name = name
        self.ui_status = ui_status

    @abstractmethod
    def get_move(self, board):
        ...

    @abstractmethod
    def submit_move(self, move):
        ...

    @abstractmethod
    def print_board(self, player_name, board):
        ...
