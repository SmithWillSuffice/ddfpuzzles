#!/usr/bin/env python3.6

from ddfpuzzles.puzzsolver import PuzzSolver

class JugFill(PuzzSolver):
    '''
    Given a two empty jugs with 3 and 5 litre capacities and a full
    jug with 8 litres, find a sequence of pours leaving four litres
    in the two largest jugs.
       
    Reference: <http://bayareapython.com/media/raymond-2018-holiday-party/puzzle.html#jug-filling-problem>
       
    Unlike Hettinger's version I cannot iterate through the game inside 
    the Puzzle.solve() because it exhausts the generator.  So instead my 
    Puzzle() class returns only the 'trail' set. 
       
    Then in __main__ here I print out the solution by creating a second 
    instance of the same game going in reverse with the goal as the 
    initial pos.
       
    Keyword args:
    
    start = <tuple> - alternative initial game position. Default = (0,0,8).
    
    Usage:
    
    >>> from pprint import pprint
    >>> puzz = JugFill()
    >>> pprint(puzz.solve())
    [(0, 0, 8),
     (0, 5, 3),
     (3, 2, 3),
     (0, 2, 6),
     (2, 0, 6),
     (2, 5, 1),
     (3, 4, 1),
     (0, 4, 4)]

    '''
    pos = (0, 0, 8)
    capacity = (3, 5, 8)
    goal = (0, 4, 4)
    
    def __init__(self,*args,**kwargs):
        if 'start' in kwargs: self.pos = kwargs['start']
        if args :
            self.pos = args[0]
        for x,y in zip(self.pos,self.capacity):
            assert x<=y, f'Bad init(), need jug quantities={self.pos} each to be less than their capacity = {self.capacity}'
        assert sum(self.pos)==sum(self.goal), f'Bad init(), need sum of jug  quantities=sum({self.pos})={sum(self.pos)} to be less than sum(goal)= {sum(self.goal)}'
            
    def __repr__(self):
        return '{}'.format(self.pos) 
    
    def canonical(self):
        return self.pos
    
    def isgoal(self):
        return self.goal == self.pos
    
    def __iter__(self):
        """Iterates over all possible moves from current 'pos' """
        for i in range(len(self.pos)):
            for j in range(len(self.pos)):
                if i==j: continue
                qty = min(self.pos[i], self.capacity[j] - self.pos[j])
                if not qty: continue
                dup = list(self.pos)
                dup[i] -= qty
                dup[j] += qty
                yield JugFill(tuple(dup))
    
if __name__ == '__main__':
    from pprint import pprint
    
    puzz = JugFill()
    print('Solution:')
    pprint(puzz.solve(),width=24)
    


#if __name__ == "__main__":
    #import doctest
    #doctest.testmod()
