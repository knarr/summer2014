#file: zoo.py
#A collection of transition structures with value iteration in place

from transitionStructure import *
from valueIterator import *
from specification import *

#### LITTMAN'S HALLWAY ####
def hallway(n, p, worth):
    #n: length of hallway in the safe direction
    #p: probability of hitting wall even in safe direction
    
    #Set up the transition structure
    ts = TransitionStructure()
    ts.addAction('start','sit',{'start': 1})
    ts.addAction('start','a',{'wall': 1})
    ts.addAction('wall','a',{'goal': 1})
    ts.addAction('goal','a',{'done': 1})
    ts.addAction('done','a',{'done': 1})
    ts.addAction('start','b',{0: 1})
    ts.addAction(0, 'a', {'wall': p, 1: 1-p})
    ts.addAction(n, 'a', {'goal': 1})
    for k in range(1, n):
        ts.addAction(k, 'a', {k+1: 1})
    
    #And the reward function
    G = lambda st: 1 if st == 'goal' else 0
    W = lambda st: 1 if st == 'wall' else 0
    S = lambda st: 1 if st == 'start' else 0
    rfs = combineReward(G, W, S)
    
    vi = ValueIterator(ts, rfs, worth)
    return vi


#### TWO WAY LITTMAN's HALLWAY ####
def twohallway(n, p, worth):
    #n: length of hallway in the safe direction
    #p: probability of hitting wall even in safe direction
    
    #Set up the transition structure
    ts = TransitionStructure()
    ts.addAction('start','sit',{'start': 1})
    ts.addAction('start','a',{'wall': 1})
    ts.addAction('wall', 'z',{'start': 1})
    ts.addAction('wall','a',{'goal': 1})
    ts.addAction('goal','z',{'wall': 1})
    ts.addAction('goal','a',{'goal': 1})
    ts.addAction('start','b',{0: 1})
    ts.addAction(0, 'y', {'start': 1})
    ts.addAction(0, 'a', {'wall': p, 1: 1-p})
    ts.addAction(1, 'z', {0: 1})
    ts.addAction(n, 'a', {'goal': 1})
    ts.addAction('goal', 'y', {n: 1})
    for k in range(1, n):
        ts.addAction(k, 'a', {k+1: 1})
        ts.addAction(k+1, 'z', {k: 1})
    
    #And the reward function
    G = lambda st: 1 if st == 'goal' else 0
    W = lambda st: 1 if st == 'wall' else 0
    S = lambda st: 1 if st == 'start' else 0
    rfs = combineReward(G, W, S)
    
    vi = ValueIterator(ts, rfs, worth)
    return vi

#### CHOICE OF RATIOS ####
def ratioChoice(worth):
    ts = TransitionStructure({
        ('start','x','x0A'): 1, ('start','y','y0A'): 1, ('start','z','z0A'): 1,
        ('x0A', 'x', 'x1B'): 1, ('y0A','y','y1B'): 1, ('z0A','z','z1B'): 1,
        ('x1B', 'x', 'x2' ): 1, ('y1B','y','y2B'): 1, ('z1B','z','z2A'): 1,
        ('x2' , 'x', 'x3' ): 1, ('y2B','y','y3B'): 1, ('z2A','z','z3A'): 1,
        ('x3' , 'x', 'x4A'): 1, ('y3B','y','y4A'): 1, ('z3A','z','z4A'): 1,
        ('x4A', 'x', 'x5B'): 1, ('y4A','y','y5B'): 1, ('z4A','z','z5B'): 1,
        ('x5B', 'x', 'end'): 1, ('y5B','y','end'): 1, ('z5B','z','end'): 1,
        ('end', 'sit', 'end'): 1
    })
    A = lambda st: 1 if st.endswith('A') else 0
    B = lambda st: 1 if st.endswith('B') else 0
    rfs = combineReward(A, B)
    return ValueIterator(ts, rfs, worth)
