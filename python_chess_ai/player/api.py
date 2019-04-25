#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Implementation of player interface for API given input
#

from player.interface import PlayerInterface


class Player(PlayerInterface):
    def __init__(self, num, name, ui_status, difficulty=None):
        super().__init__(num, name, ui_status, difficulty)

    def get_move(self, board):
        super().get_move(board)

    def submit_move(self, move):
        super().submit_move(move)