#!/bin/bash
# ToDo: Argumentparser to specify which player_type should play against which_player_type
for i in {1..500}
do
   python main.py -t --player DummLars DummPascal -pT Dummy Dummy -pD 0 0 <<<0
   echo $i
done
