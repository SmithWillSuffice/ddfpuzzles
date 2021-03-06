from ddfpuzzles.nine_sliding_blocks import NineBlocksPuzzle
import pytest

class TestNineBlocks(object):
    
    def test_startgame(self):
        puzz1 =  NineBlocksPuzzle()
        expected1 = '\n1122\n1133\n45..\n6788\n6799\n'
        puzz2 =  NineBlocksPuzzle('11331122458867996700')
        expected2 = '\n1133\n1122\n4588\n6799\n67..\n'
        assert repr(puzz1) == expected1 
        assert repr(puzz2) == expected2
        
    def test_endgames(self):
        puzz1 = NineBlocksPuzzle()
        soln1 = puzz1.solve()
        expected1 = '\n7633\n7622\n..54\n1199\n1188\n'
        puzz2 = NineBlocksPuzzle('11331122458867996700')
        soln2 = puzz2.solve()
        expected2 = '\n7622\n7633\n..54\n1199\n1188\n'
        assert repr(soln1[-1]) == expected1
        assert repr(soln2[-1]) == expected2

    def test_outsized(self):
        with pytest.raises(AssertionError):
            puzz =  NineBlocksPuzzle('1'*21)
            
    def test_pos_lett(self):
        with pytest.raises(ValueError):
            puzz =  NineBlocksPuzzle('1ab31122458867996700')
            
    def test_pos_sym(self):
        with pytest.raises(ValueError):
            puzz =  NineBlocksPuzzle('1_311224588679967700')
            
    def test_pos_dot(self):
        with pytest.raises(ValueError):
            puzz =  NineBlocksPuzzle('1.311224588679967700')
            
