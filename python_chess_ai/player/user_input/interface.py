#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Interface for entering moves, output the board etc.
#

from abc import ABC, ABCMeta, abstractmethod


class UserInputInterface(ABC):
    __metaclass__ = ABCMeta

    def __init__(self):
        super().__init__()

    @abstractmethod
    def print_board(self, player_name, board):
        ...

    @abstractmethod
    def get_move(self, move):
        ...