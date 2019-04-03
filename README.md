# ddfpuzzles &middot; [![Testing Status](https://img.shields.io/badge/tests-11%20passed-brightgreen.svg)](https://img.shields.io/badge/tests-11%20passed-brightgreen.svg) [![GitHub license](https://img.shields.io/badge/license-GPL.v.3-brightgreen.svg)](https://img.shields.io/badge/license-GPL.v.3-brightgreen.svg)
> puzzles, sliding blocks, jug filling

Generic discrete deterministic finite state puzzle solver.

### Provides
Python3 module `puzzsolver.py`. Supplies the class `PuzzSolver` which has a `solve()` method.

### Usage
Place the module `puzzsolver.py` in a subdirectory named `./ddfpuzzles/` somewhere in one of your `PYTHONPATH` directories.  Optionally copy the two examples `jug_fill.py` and `nine_sliding_blocks.py` into this directory as well.

Given any discrete state finite move game, if you know what defines a valid move, then you should be able to write a class derived from `PuzzSolver` with an `__iter()__` method which runs through all possible single step moves available given the current game state, it should `yield` the state of the game after such a valid move.  

The `puzzsolver` module should then be able to solve the game for you, by returning a list of valid moves which go from the start of the game to the goal (end state) of the game.  For this to work you also need to define a member function `canonical()` for your class which converts the current game state into a canonical form (a representative of an equivalence class of game states), and you will need at least one other member function `isgoal()` which should return `True` of the current state of the game is a solution.

For more details please read the docstrings in the modules.

## Example
```shell
>>> from ddfpuzzles.nine_sliding_blocks import NineBlocksPuzzle
>>> puzz = NineBlocksPuzzle()
>>> from pprint import pprint
>>> pprint(puzz.solve())
[(0, 0, 8),
 (0, 5, 3),
 (3, 2, 3),
 (0, 2, 6),
 (2, 0, 6),
 (2, 5, 1),
 (3, 4, 1),
 (0, 4, 4)]

```
The interpretation is you start with three jugs, they have capacities (3,5,8) litres respectively. 8 litres of water is in the large jug.  Each move either empties one jug completely into another if possible without overflow, or uses water in one jug to completely fill another.  The goal is to get 4 liters in two of the jugs.  The output above shows a sequence of valid moves to get this done.  The first move uses the large jug to completely fill the middle jug.  The second move uses the middle jug to completely fill the small jug.

See the two examples `jug_fill.py` and `nine_sliding_blocks.py`.  These were adapted from Raymond Hettinger's talk which you can see here: [http://bayareapython.com/media/raymond-2018-holiday-party/puzzle.html](http://bayareapython.com/media/raymond-2018-holiday-party/puzzle.html)


### Requirements
If you have a working Python3 installed the code should work fine.


## Tests

Install a version of pytest appropriate for your system, e.g.,:
```shell
$ sudo apt-get install python3-pytest
```

To run the tests:
```shell
$ cd <path to ddfpuzzles>
$ py.test-3
```

## Other Ideas

After writing the two examples, `jug_fill.py` and `nine_slding_blocks.py` I was thinking about solving a game of Hex-a-hop.  For simple Hex-a-hop grids where the tiles are one of two types, either permanent or disappear after hopping on them it might not be too hard. But the advanced levels involving further types of booster tiles could get tricky.

It might be possible to adapt the basic solver in the module `puzzsolver.py` to solve continuous state problems where a "close enough" goal can be defined.  Search heuristics could then be used to explore the game space instead of iterating through all possible moves.  This would have to be a completley different project.

## Licensing

GNU GPL.v.3, see, [https://www.gnu.org/licenses/gpl.txt](https://www.gnu.org/licenses/gpl.txt)

