#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file is part of the python-chess-ai.
# Copyright (C) 2018 Lars Dittert <lars.dittert@de.ibm.com> and Pascal Schroeder <pascal.schroeder@de.ibm.com>
#
# Interface for entering settings like player type, name etc.
#

class PlayerSettings():
    def __init__(self, num, name, type, difficulty=None):
        self.num = num
        self.name = name
        self.type = type
        self.difficulty = difficulty
