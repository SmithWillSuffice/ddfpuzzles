#!/usr/bin/env python3
'''Nine Sliding Blocks Square Puzzle - demo script for `puzzles.puzzle`

Provides:
   class NineBlocksPuzzle_ for solving a given game.

Teaching demo for Python puzzle module.  Provides a solver for a famous
sliding block puzzle with 9 blocks, one 2x2, six 2x1 and two 1x1 blocks 
arranged in a 5x4 grid, which leaves two 1x1 holes.

Goal is to get from some initial state to a state with the 2x2 block in the 
lower left corner.

Raymond Hettinger (see ref below) came up with a nice representation of the 
state and the solution.

State is a string of the block label (blocks '0' through '9', with the 2x2 
block having the label '1', and the holes labelled '0') in row order 
positions. So a state,

>>>
 1 1 2 2
 1 1 3 4
 0 0 3 4
 5 6 6 8
 5 7 7 9

has the 2x2 block in the upper left, and the two 1x1 blocks in the lower 
right-most cells, and string representation:

>>> pos = '112211343456685779'

A solution is any match to the regular expression,

>>> r'................1...'

since if the 2x2 block (label '1') covers the lower left corner, there is 
only one unique way it can do so.

References:
<http://bayareapython.com/media/raymond-2018-holiday-party/puzzle.html#sliding-block-puzzle>
<https://www.youtube.com/watch?v=lOWeCyOvRGk&t=352s>

General Theory
--------------
All Finite State Discrete Move puzzles have a solution unless they are blocked 
by some keyhole to an insoluble state that cannot be reversed out of, or if the 
initial state is in a region of state space disjoint by moves from the 
solution space.  In terms of a graph connecting states by moves we want the 
initial state to be connected to all valid solution states by at least 
one edge.

The solution algorithm uses two key general puzzle solving ideas that are 
almost generic for a Finite State Discrete Move Puzzle:

1.  Canonical states: some relabellings are equivalent, e.g. if we swap any 
    pair of the 2x1 blocks the state is unchanged.  We want to recognize such 
    states if they are encountered because a repeat of a canonical state 
    represents no progress.
    
2. Iterable moves: we want to be able to do breadth or depth searches through 
   all possible moves!!!  Although brute- force, this can be done in ugly or 
   elegant ways, and we want an elegant way.

   Think of the space explored as a tree growing branches (or roots) 
   downwards, with the initial state at the top.
   
   * Breadth first tries out all moves possible from given state before 
     exploring newly opened moves.  So we branch a lot, in fact maximally.  
     When a branch hits a previously accessed canonical state it is 
     terminated (removed from the search history).  The explored tree grows 
     flat, one level of branching at a time.
   * Depth first search tries new moves as soon as they are opened.  When a 
     previously accessed canonical state is reached they are deemed to hit a 
     dead end, and the search then must back track and try one of the 
     alternative branches of moves, the next higher branch above.  The 
     exploration tree thus grows as separate 'finger' one branch at a time, 
     deepest subbranches grow before primary sub-branches.

Copyright (c) 2019, Bijou Murray Smith

Licence: GNU GPL.v.3, see: <https://www.gnu.org/licenses/gpl.txt>
'''
from ddfpuzzles.puzzsolver import PuzzSolver
import re

class NineBlocksPuzzle(PuzzSolver):
    '''.. _NineBlocksPuzzle:
    
    NineBlocksPuzzle inherited from Puzzle is an iterable which when iterated 
    goes through all possible moves of the game in the current state.  The member 
    'pos' is the current state of the game.
    
    Attributes:
    
    pos 
       -- Starting position of the game.
    
    goal 
       -- regular expression which any valid solution must match.
    
    b_equiv 
       -- string translation dict for transforming an arbitrary 'pos' into 
       a canonical form..
    
    block 
       -- set of tuples of the form ('place', 'move') specifying disallowed 
       moves of any holes in the given 'place' on the game grid.
    
    Usage:
    
       >>> from nine_block_puzzle import NineBlocksPuzzle
       >>> from pprint import pprint
       >>> pprint(NineBlocksPuzzle().solve())
    
    Notes:
    
    Puzzle implements a general solve() function which uses the iterator to 
    search either Breadth-first or Depth-first to find a valid solution. To do so 
    the inheriting child class (here NineBlocksPuzzle ) must implement an isgoal() 
    method returning True iff the current state is a solution.
    
    See the module documentation for an overview.  This class starts from a 
    game position:
    
    | 1122
    | 1133
    | 4500
    | 6788
    | 6799
    
    represented by the string 
    
    >>> pos = '112211343456685779'
    
    The goal is a regular expression, and we'd expect:
    
    >>> re.match(goal,'22222222222222222221') is not None
    False
    >>> re.match(goal,'22222222222222221xx1') is not None
    True
    
    '''
    pos = '11221133450067886799'
    b_equivs = str.maketrans('38975','22264')
    goal = re.compile(r'.'*16+'1'+'.'*3)
    
    def __init__(self,*args,**kwargs):
        if 'start' in kwargs: self.pos = kwargs['start']
        if args :
            self.pos = args[0]
        assert len(self.pos)==20, f'Bad init(), need string of len=20, your\'s was {self.pos} len={len(self.pos)}'
        for x in self.pos:
            assert int(x)<=9 and int(x)>=0, f'Bad init(), game state must be a string of single digits, your\'s is pos = {self.pos}'
            
    def __repr__(self):
        ans = '\n'
        p = self.pos.replace('0', '.')
        for i in [0, 4, 8, 12, 16]:
            ans = ans + p[i:i+4] + '\n'
        return ans
    
    def isgoal(self):
        return self.goal.search(self.pos) != None
    
    def canonical(self):
        '''
        The member 'b_equivs' is a dictionary specifying a transform of 
        letters for a substitution pattern.  So if 
        
        >>> b_equivs = str.maketrans('45678','33229')
        
        then we are saying '4' and '5' are equivalent to '3',
        '6' and '7' are equivalent to '2', and '8' is equivalent to'9'
        This means we can eliminate all '4','5','6','7','8' from any state.
        So a canonical form of the general position, 
    
        >>> x = '23230081111944556767'
        
        would be
        
        >>> canonical(x) -> '23230091111933332222'
        
        Basically a '3' is a generic vertical 2x1 block, and a '2' is a 
        generic horizontal 1x2 block.
        '''
        return self.pos.translate(self.b_equivs)
    
    """The 'block' set defines moves that are not allowed.  The first of a tuple
    to be checked against 'block' should be a position in the 'pos' grid 
    currently free, a '0' position, the only such positions blocked are around 
    the circumference, so these are, going around clockwise: 
    0,1,2,3,7,11,15,19,18,17,16,12,8,4.
    A move right|left along a row is a +1|-1 shift along the 'pos' string.
    A move up|down a column is a -4|+4 shift along the 'pos' string.
    In our grid the 0,1,2,3 row is top, so if a '0' is in any of these 
    positions they cannot go up, so a -4 move is not allowed,
    sly. a '0' in any place along the 0,4,8,12 (leftmost)edge cannot move 
    left, so a -1 move is disallowed for these.  All the other blocked moves 
    are listed in the set 'block'. 
    """
    block: set = { (0,-4), (1,-4), (2,-4), (3,-4),
                (16,4), (17,4), (18,4), (19,4),
                (0,-1), (4,-1), (8,-1), (12,-1), (16,-1),
                (3,1), (7,1), (11,1), (15,1), (19,1) }
    
    def __iter__(self):
        """
        Lists all possible moves from current state 'pos' returned as a new Puzzle.
        
        The algorithm here is to imagine moving the '0' labels (holes).  A hole has 4 
        adjacent cells it can shift to unless it is at a corner or edge.
        
        After blocking disallowed moves for the pair of current holes '0', we retrieve 
        the label 'piece' of the block at one of the possible adjacent places a '0' could 
        move.  If this is also a '0' we ignore and go to the next adjacent place available 
        for the hole. A possible move is added to the Puzzle iterable. 
        """
        dsone = self.pos.find('0')
        dstwo = self.pos.find('0', dsone+1)
        for dest in [dsone, dstwo]:
            for adj in [-4, -1, 1, 4]:
                if (dest, adj) in self.block: continue
                piece = self.pos[dest+adj]
                if piece == '0': continue
                #print('In __iter__ evaluating at piece =',piece)
                newmove = self.pos.replace(piece, '0')
                for i in range(len(self.pos)):
                    if 0 <= i+adj < len(self.pos) and self.pos[i+adj]==piece:
                        newmove = newmove[:i] + piece + newmove[i+1:]
                if newmove.count('0') != 2: continue
                #print('   yielding newmove = %s' % newmove )
                yield NineBlocksPuzzle(newmove)
                
#-----------------------------------------------
if __name__ == '__main__':
    from pprint import pprint
    
    puzz = NineBlocksPuzzle()
    soln_steps = puzz.solve()
    print('Solution:')
    pprint(soln_steps)
    


#if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
