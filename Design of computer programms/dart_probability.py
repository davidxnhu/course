# Unit 5: Probability in the game of Darts

"""
In the game of darts, players throw darts at a board to score points.
The circular board has a 'bulls-eye' in the center and 20 slices
called sections, numbered 1 to 20, radiating out from the bulls-eye.
The board is also divided into concentric rings.  The bulls-eye has
two rings: an outer 'single' ring and an inner 'double' ring.  Each
section is divided into 4 rings: starting at the center we have a
thick single ring, a thin triple ring, another thick single ring, and
a thin double ring.  A ring/section combination is called a 'target';
they have names like 'S20', 'D20' and 'T20' for single, double, and
triple 20, respectively; these score 20, 40, and 60 points. The
bulls-eyes are named 'SB' and 'DB', worth 25 and 50 points
respectively. Illustration (png image): http://goo.gl/i7XJ9

There are several variants of darts play; in the game called '501',
each player throws three darts per turn, adding up points until they
total exactly 501. However, the final dart must be in a double ring.

Your first task is to write the function double_out(total), which will
output a list of 1 to 3 darts that add up to total, with the
restriction that the final dart is a double. See test_darts() for
examples. Return None if there is no list that achieves the total.

Often there are several ways to achieve a total.  You must return a
shortest possible list, but you have your choice of which one. For
example, for total=100, you can choose ['T20', 'D20'] or ['DB', 'DB']
but you cannot choose ['T20', 'D10', 'D10'].
"""

def test_darts():
    "Test the double_out function."
    assert double_out(170) == ['T20', 'T20', 'DB']
    assert double_out(171) == None
    assert double_out(100) in (['T20', 'D20'], ['DB', 'DB'])

"""
My strategy: I decided to choose the result that has the highest valued
target(s) first, e.g. always take T20 on the first dart if we can achieve
a solution that way.  If not, try T19 first, and so on. At first I thought
I would need three passes: first try to solve with one dart, then with two,
then with three.  But I realized that if we include 0 as a possible dart
value, and always try the 0 first, then we get the effect of having three
passes, but we only have to code one pass.  So I creted ordered_points as
a list of all possible scores that a single dart can achieve, with 0 first,
and then descending: [0, 60, 57, ..., 1].  I iterate dart1 and dart2 over
that; then dart3 must be whatever is left over to add up to total.  If
dart3 is a valid element of points, then we have a solution.  But the
solution, is a list of numbers, like [0, 60, 40]; we need to transform that
into a list of target names, like ['T20', 'D20'], we do that by defining name(d)
to get the name of a target that scores d.  When there are several choices,
we must choose a double for the last dart, but for the others I prefer the
easiest targets first: 'S' is easiest, then 'T', then 'D'.
"""

    
"""
It is easy enough to say "170 points? Easy! Just hit T20, T20, DB."
But, at least for me, it is much harder to actually execute the plan
and hit each target.  In this second half of the question, we
investigate what happens if the dart-thrower is not 100% accurate.

We will use a wrong (but still useful) model of inaccuracy. A player
has a single number from 0 to 1 that characterizes his/her miss rate.
If miss=0.0, that means the player hits the target every time.
But if miss is, say, 0.1, then the player misses the section s/he
is aiming at 10% of the time, and also (independently) misses the thin
double or triple ring 10% of the time. Where do the misses go?
Here's the model:

First, for ring accuracy.  If you aim for the triple ring, all the
misses go to a single ring (some to the inner one, some to the outer
one, but the model doesn't distinguish between these). If you aim for
the double ring (at the edge of the board), half the misses (e.g. 0.05
if miss=0.1) go to the single ring, and half off the board. (We will
agree to call the off-the-board 'target' by the name 'OFF'.) If you
aim for a thick single ring, it is about 5 times thicker than the thin
rings, so your miss ratio is reduced to 1/5th, and of these, half go to
the double ring and half to the triple.  So with miss=0.1, 0.01 will go
to each of the double and triple ring.  Finally, for the bulls-eyes. If
you aim for the single bull, 1/4 of your misses go to the double bull and
3/4 to the single ring.  If you aim for the double bull, it is tiny, so
your miss rate is tripled; of that, 2/3 goes to the single ring and 1/3
to the single bull ring.

Now, for section accuracy.  Half your miss rate goes one section clockwise
and half one section counter-clockwise from your target. The clockwise 
order of sections is:

    20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5

If you aim for the bull (single or double) and miss on rings, then the
section you end up on is equally possible among all 20 sections.  But
independent of that you can also miss on sections; again such a miss
is equally likely to go to any section and should be recorded as being
in the single ring.

You will need to build a model for these probabilities, and define the
function outcome(target, miss), which takes a target (like 'T20') and
a miss ration (like 0.1) and returns a dict of {target: probability}
pairs indicating the possible outcomes.  You will also define
best_target(miss) which, for a given miss ratio, returns the target 
with the highest expected score.

If you are very ambitious, you can try to find the optimal strategy for
accuracy-limited darts: given a state defined by your total score
needed and the number of darts remaining in your 3-dart turn, return
the target that minimizes the expected number of total 3-dart turns
(not the number of darts) required to reach the total.  This is harder
than Pig for several reasons: there are many outcomes, so the search space 
is large; also, it is always possible to miss a double, and thus there is
no guarantee that the game will end in a finite number of moves.
"""


from collections import defaultdict

MULTIPLIES=('S','D','T')
POINTS=('1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20')

possible_plays=[a+b for a in MULTIPLIES for b in POINTS]

possible_plays+=['SB','DB']

def double_out(score):
    path=shortest_path_search((score,3,'_'),successors,is_goal)
    return path_actions(path) if path else None #state is (score,remaining darts in a turn)


def successors(state):
    remaining,i,_=state
    result={}
    if i>=1:
        for play in possible_plays:
            new_state=(remaining-cost(play),i-1,play)
            result[new_state]=play
    return result

def is_goal(state):
    remaining,_,play=state
    if remaining==0 and play[0]=='D':
        return True
    else:
        return False

def cost(play):
    if play=='OFF':
        return 0
    
    if play[0]=='S':
        multiplier=1
    elif play[0]=='D':
        multiplier=2
    else:
        multiplier=3

    point=play[1:]
    if point is not 'B':
        play_point=int(point)
    else:
        play_point=25

    return play_point*multiplier

def shortest_path_search(start, successors, is_goal):
    """Find the shortest path from start state to a state
    such that is_goal(state) is true."""
    if is_goal(start):
        return [start]
    explored = set() # set of states we have visited
    frontier = [ [start] ] # ordered list of paths we have blazed
    while frontier:
        path = frontier.pop(0)
        s = path[-1]
        for (state, action) in successors(s).items():
            if state not in explored:
                explored.add(state)
                path2 = path + [action, state]
                if is_goal(state):
                    return path2
                    #results.append(path2)
                else:
                    frontier.append(path2)
    return []

def path_actions(path):
    "Return a list of actions in this path."
    return path[1::2]

#print shortest_path_search((100,3,'_'),successors,is_goal)

def outcome(target,miss):
    result=defaultdict(float)
    for (ring,Pring) in ring_outcome(target,miss):
        for (sect,Psect) in sect_outcome(target,miss):
            if ring=='S' and sect =='B':
                for s in SECTIONS:
                    result[Target(ring,s)]+=Pring*Psect/20.
            else:
                result[Target(ring,sect)]+=Pring*Psect
    return dict(result.items())


def ring_outcome(target,miss):
    hit=1-miss
    l=target[0]
    if target=='SB':
        return[('SB',hit),('DB',miss/4.),('S',miss*3/4.)]
    elif target=='DB':
        miss=min(miss*3.,1.0)
        hit=1-miss
        return[('DB',hit),('SB',miss/3.),('S',miss*2/3.)]
    elif l=='T':
        return [('T',hit),('S',1-hit)]
    elif l=='D':
        return [('D',hit),('S',miss/2.),('OFF',miss/2.)]
    elif l=='S':
        miss=miss/5.
        hit=1-miss
        return [('S',hit),('T',miss/2.),('D',miss/2.)]

SECTIONS="20 1 18 4 13 6 10 15 2 17 3 19 7 16 8 11 14 9 12 5".split()

def sect_outcome(target,miss):
    hit=1.-miss
    if target=='SB' or target=='DB':
        misses=[]
        for s in SECTIONS:
            misses+=[(s,miss/20.)]
        return misses+[('B',hit)]
    else:
        i=SECTIONS.index(target[1:])
        length=len(SECTIONS)
        misses=[(SECTIONS[(i-1)%length],miss/2.),(SECTIONS[(i+1)%length],miss/2.)]
        return misses+[(target[1:],hit)]
    
def Target(ring,sect):
    if ring=='OFF':
        return 'OFF'
    elif ring in ('SB','DB'):
        return ring if sect=='B' else 'S'+sect
    else:
        return ring+sect

def best_target(miss):
    def expected_score(target):        
        plays=outcome(target,miss)
        return sum(cost(play)*plays[play] for play in plays)

    return max(possible_plays,key=expected_score)

#print sect_outcome('SB',0.2)
#print Target('OFF','2')
#print outcome('T20',0.1)

print best_target(0.4)
