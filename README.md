# SortingBallColors

This is a repository for a personal project where I try to make the game 'Sorting balls by color'. This game will mostly be done through a state representation in python and could be expanded upon visually. The goal is to make an efficient solver.

## Game explanation

### Start

The game starts with a number of ball colors N and a number of tubes N+2. There are four balls of each color and they are randomly placed in each of the first N tubes until all of them are full. 

### Goal

The goal of the game is to have all balls sorted by color. So you should only have 1 color in each tube. Which tube each color is in doesn't matter. 

### Rules

You can do this by moving the balls around, but there are some strict rules.

- No tube can ever have more than 4 balls in it
- You can only move a ball to a tube where the top ball is of the same color or to an empty tube