'''
Generic puzzle solver framework

Reference:
<http://bayareapython.com/media/raymond-2018-holiday-party/puzzle.html#core-logic>

Copyright (c) 2019, Bijou Murray Smith

Licence:  GNU GPL.v.3, see: <https://www.gnu.org/licenses/gpl.txt>
'''
from collections import deque
import re

class PuzzSolver(deque):
    '''Generic discrete deterministic finite state puzzle solver.  A Puzzle instantiation inherited 
    from this class must have a current state 'pos' and an iterator defined in 
    an __iter__() function.  It must also implement a method canonical() which
    transforms a state 'pos' into a canonical form (equivalence class standard 
    representative), how you do this is up to you and depends on the particulars
    of your puzzle.
    
    For an example see,
    './nine_sliding_blocks/nine_sliding_blocks/.py'
    or 
    './jug_fill/jug_fill.py'
    
    Should work for any game/puzzle where a give state (or position 'pos') of 
    the game can be specified by a list or string, and a move is a discrete 
    transform of the state.
    
    Usage:
    
    You need to do something like the following at a minimum. A class derived 
    from puzzle with methods; isgoal(), canonical(), __iter__() 
    
    from ddfpuzzles.puzzsolver import PuzzSolver
    class YourGame(PuzzSolver):
       pos = #... initial state of the game
       
        def __init__(self,*args,**kwargs):
            # you could use a kwarg for setting a different initial pos
            if 'start' in kwargs: self.pos = kwargs['start']
            if args :
                self.pos = args[0]
            
       def isgoal(self):
          return #... true iff the current state is a solution
                 # could be a simple '==' match or a regexp match.
                 
       def canonical(self):
          # convert every position in the game to a standard equivalent form.
          
       def __iter__(self):
          # generates every possible move of the game from pos with yield 
          # statements.
          # This could be a VERY complicated algorithm, or a probabilistic 
          # heuristic search not guaranteed to find a solution, if so, 
          # isgoal() should then involve a 'closeness' satisficing type of 
          # match.
          # You might also want to raise a custom exception if no moves are 
          # possible, which might print "No solution exists." or 
          # f"Cannot move from position {pos}." an then exits.
       
    if __name__ == '__main__':
        from pprint import pprint
        puzz = YourGame()
        print('Solution:')
        pprint(puzz.solve())
        
    '''
    def solve(pos, depthFirst=False):
        '''Generic solver for a finite state discrete move puzzle or game.
        
        'pos': Puzzle the current instance of the Puzzle (same as the 
               traditional 'self' object.  So when calling solve() you do not 
               specify this argument.  
                
        'depthFirst': bool when False implements a Breadth-first walk through the 
                      state space of the game. 
        '''
        queue = deque([pos])
        trail = { pos.canonical() : None}
        load = queue.append if depthFirst else queue.appendleft
        endgame = None
        while not pos.isgoal():
            for m in pos:
                c = m.canonical()
                if c in trail:
                    continue
                trail[c] = pos
                load(m)
            pos = queue.pop()
            if pos.isgoal(): endgame = pos
        solution = deque()
        while endgame is not None:
            solution.appendleft(endgame)
            endgame = trail[endgame.canonical()]
        return list(solution)
        
    
#if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
