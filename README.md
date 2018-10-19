# PythonChessAI

## Description

This project is in the context of a study project for a scientific approach for developing a chess AI. Therefore we will evaluate needed technologies, realize our project and document our used technologies and theoretical backgrounds as well as the implementation itself. Finally we will evaluate our results on the basis of our defined requirements and criteria.

This repository is for developing a python chess AI. Based on the python-chess library it should be able to use different algorithms for calculating the best moves.

Therefore it will start with moves from an opening book. Then it will calculate every possible move and will evaluate the board value. Possibly it will combine this with values for attacked figures and a game history (matched with Wins and Loses of these games).

## Functional Requirements

This AI has following functional requirements:

- User can choose game mode (Player vs. AI; AI vs. AI; _(Optional)_ Trainer (Monte Carlo); _(Optional)_ API vs. AI)
- _(Optional)_ User can choose difficulty
- _(Optional)_ User can communicate with backend over GUI
- User can start game 
- User can enter move 
- Board can be printed as ASCII code 
- User can end the game
- AI uses opening book for first _x_ moves
- AI calculate best possible move by iterative deepening (board value & _(Optional)_ attacked figures)
- _(Optional)_ Match can be recorded for creating a match history
- _(Optional)_ AI combines iterative deepening with game history
- _(Optional)_ AI can be connected to chess.com or similar chess game website for getting an ELO rating assigned

## Non-Functional Requirements

This AI has following non-functional requirements: 
 
- Structured implementation 
- "Easy-to-understand" code
- Visible usage of covered techniques
- Easy evaluation process
- Easy extendable
- High transparency
- _(Optional)_ Public chess software as opponent to rate the intelligence

## Organization

This project will be organized with splitting the tasks in different Issues and assigning those between the developmen team. 

To use the issues feature of GitHub more effectively and better plan and track or progress, we are going to use the ZenHub plugin. This allows us to organize all the issues in pipelines and create an overview on all our tasks.
To use this everyone has to download the Browser extension for either Chrome or Firefox. As soon as the plugin is installed you can switch to the ZenHub Board of our repository.