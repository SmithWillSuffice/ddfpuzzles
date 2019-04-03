from dffpuzzles.jug_fill import JugFill
import pytest 

class TestJugFill(object):
    
    def test_startgame(self):
        puzz =  JugFill()
        expected = (0,0,8)
        assert puzz.pos == expected
        
    def test_startalt(self):
        puzz =  JugFill((1,2,5))
        expected = (1,2,5)
        assert puzz.pos == expected
        
    def test_overcapacity(self):
        with pytest.raises(AssertionError):
            puzz =  JugFill((4,4,0))
            
    def test_undercapacity(self):
        with pytest.raises(AssertionError):
            puzz =  JugFill((1,1,1))
            
    def test_endgames(self):
        puzz = JugFill()
        soln = puzz.solve()
        print(soln)
        expected = [(0, 0, 8), (0, 5, 3), (3, 2, 3), (0, 2, 6), (2, 0, 6), (2, 5, 1), (3, 4, 1), (0, 4, 4)]
        for s,e in zip(list(soln),expected):
            assert repr(s)==repr(e)
